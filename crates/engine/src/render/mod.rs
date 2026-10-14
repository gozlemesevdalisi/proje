//! Grafik kartında çizim.
//!
//! - Ağlar ([`crate::tessellate::Mesh`]) bir kez yüklenir ([`Renderer::upload`]), her karede
//!   yalnızca dönüşümleriyle çizilir.
//! - Kenar yumuşatma 4 örneklemeli MSAA ile yapılır.
//! - Renkler sRGB uzayında karışır: hedef doku "sRGB" değil, düz `Unorm` biçimindedir.
//! - Her çizime Flash'taki gibi bir renk dönüşümü ([`ColorTransform`]) verilebilir: saydamlık,
//!   renklendirme, gün saati ışığı.

mod paints;

use std::collections::HashMap;
use std::fmt;
use std::sync::Arc;

use bytemuck::{Pod, Zeroable};
use glam::{Affine2, UVec2, Vec2};
use wgpu::util::DeviceExt;

use crate::color::Color;
use crate::image::RgbaImage;
use crate::paint::RAMP_WIDTH;
use crate::tessellate::{Mesh, MeshVertex};
use crate::viewport::Viewport;

use paints::{GpuPaint, PaintTable, affine_rows};

/// Kenar yumuşatmadaki örnek sayısı.
pub const SAMPLE_COUNT: u32 = 4;

/// Mantıksal alanın dışında kalan şeritlerin rengi.
pub const LETTERBOX_COLOR: Color = Color::rgba(0.055, 0.047, 0.04, 1.0);

/// Ekransız çizimde kullanılan doku biçimi.
pub const IMAGE_FORMAT: wgpu::TextureFormat = wgpu::TextureFormat::Rgba8Unorm;

#[derive(Debug)]
pub enum RenderError {
    NoAdapter(String),
    Device(String),
    Readback(String),
}

impl fmt::Display for RenderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RenderError::NoAdapter(e) => write!(f, "uygun grafik kartı bulunamadı: {e}"),
            RenderError::Device(e) => write!(f, "grafik kartı açılamadı: {e}"),
            RenderError::Readback(e) => write!(f, "çizilen resim okunamadı: {e}"),
        }
    }
}

impl std::error::Error for RenderError {}

/// Renk dönüşümü: `sonuç = renk × mul + add` (düz renk üzerinde, bileşen bileşen).
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct ColorTransform {
    pub mul: [f32; 4],
    pub add: [f32; 4],
}

impl ColorTransform {
    pub const IDENTITY: ColorTransform = ColorTransform {
        mul: [1.0; 4],
        add: [0.0; 4],
    };

    /// Yalnızca saydamlığı değiştiren dönüşüm.
    pub fn alpha(a: f32) -> Self {
        ColorTransform {
            mul: [1.0, 1.0, 1.0, a],
            add: [0.0; 4],
        }
    }

    /// Rengi verilen renkle çarpar (gün saati ışığı, gölgede kalma).
    pub fn multiply(c: Color) -> Self {
        ColorTransform {
            mul: [c.r, c.g, c.b, c.a],
            add: [0.0; 4],
        }
    }

    /// İki dönüşümü art arda uygular: önce `self`, sonra `then`.
    pub fn then(self, then: ColorTransform) -> Self {
        let mut out = ColorTransform::IDENTITY;
        for i in 0..4 {
            out.mul[i] = self.mul[i] * then.mul[i];
            out.add[i] = self.add[i] * then.mul[i] + then.add[i];
        }
        out
    }
}

/// Gölgelendiricideki örnek (instance) bilgisi (64 bayt).
#[repr(C)]
#[derive(Clone, Copy, Debug, Pod, Zeroable)]
struct GpuInstance {
    t0: [f32; 4],
    t1: [f32; 4],
    mul: [f32; 4],
    add: [f32; 4],
}

impl GpuInstance {
    fn new(transform: Affine2, color: ColorTransform) -> Self {
        let (t0, t1) = affine_rows(transform);
        GpuInstance {
            t0,
            t1,
            mul: color.mul,
            add: color.add,
        }
    }
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Pod, Zeroable)]
struct GpuView {
    row0: [f32; 4],
    row1: [f32; 4],
    ramp: [f32; 4],
}

struct GpuMeshData {
    buffers: Option<(wgpu::Buffer, wgpu::Buffer)>,
    index_count: u32,
}

/// Grafik kartına yüklenmiş ağ. Kopyalaması ucuzdur; son kopyası düşünce bellekten silinir.
#[derive(Clone)]
pub struct GpuMesh(Arc<GpuMeshData>);

impl GpuMesh {
    pub fn triangle_count(&self) -> u32 {
        self.0.index_count / 3
    }
}

impl fmt::Debug for GpuMesh {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "GpuMesh({} üçgen)", self.triangle_count())
    }
}

/// Bir karede çizilecekler, çizim sırasıyla.
#[derive(Clone, Debug)]
pub struct DrawList {
    /// Mantıksal alanın arka plan rengi.
    pub clear: Color,
    items: Vec<(GpuMesh, GpuInstance)>,
}

impl DrawList {
    pub fn new(clear: Color) -> Self {
        DrawList {
            clear,
            items: Vec::new(),
        }
    }

    pub fn draw(&mut self, mesh: &GpuMesh, transform: Affine2) {
        self.draw_with(mesh, transform, ColorTransform::IDENTITY);
    }

    pub fn draw_with(&mut self, mesh: &GpuMesh, transform: Affine2, color: ColorTransform) {
        if mesh.0.index_count > 0 {
            self.items
                .push((mesh.clone(), GpuInstance::new(transform, color)));
        }
    }

    pub fn len(&self) -> usize {
        self.items.len()
    }

    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }
}

struct MsaaTarget {
    format: wgpu::TextureFormat,
    size: UVec2,
    view: wgpu::TextureView,
}

pub struct Renderer {
    device: wgpu::Device,
    queue: wgpu::Queue,
    info: wgpu::AdapterInfo,
    shader: wgpu::ShaderModule,
    pipeline_layout: wgpu::PipelineLayout,
    bind_group_layout: wgpu::BindGroupLayout,
    pipelines: HashMap<wgpu::TextureFormat, wgpu::RenderPipeline>,
    sampler: wgpu::Sampler,
    view_buffer: wgpu::Buffer,
    paints: PaintTable,
    paint_buffer: wgpu::Buffer,
    paint_capacity: usize,
    ramp_texture: wgpu::Texture,
    ramp_capacity: u32,
    bind_group: wgpu::BindGroup,
    instance_buffer: wgpu::Buffer,
    instance_capacity: usize,
    msaa: Option<MsaaTarget>,
    background: GpuMesh,
}

impl Renderer {
    /// Ekransız çizim için grafik kartını kendisi açar (testler ve resim çıktısı).
    pub fn headless() -> Result<Self, RenderError> {
        let instance =
            wgpu::Instance::new(wgpu::InstanceDescriptor::new_without_display_handle_from_env());
        let adapter = request_adapter(&instance, None)?;
        Self::from_adapter(&adapter)
    }

    /// Verilen grafik kartı için cihaz açar.
    pub fn from_adapter(adapter: &wgpu::Adapter) -> Result<Self, RenderError> {
        let (device, queue) = pollster::block_on(adapter.request_device(&wgpu::DeviceDescriptor {
            label: Some("motor"),
            required_features: wgpu::Features::empty(),
            required_limits: wgpu::Limits::default(),
            memory_hints: wgpu::MemoryHints::Performance,
            ..Default::default()
        }))
        .map_err(|e| RenderError::Device(e.to_string()))?;
        Ok(Self::new(device, queue, adapter.get_info()))
    }

    fn new(device: wgpu::Device, queue: wgpu::Queue, info: wgpu::AdapterInfo) -> Self {
        let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
            label: Some("vektör gölgelendirici"),
            source: wgpu::ShaderSource::Wgsl(include_str!("shader.wgsl").into()),
        });
        let bind_group_layout = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
            label: Some("vektör bağlama düzeni"),
            entries: &[
                wgpu::BindGroupLayoutEntry {
                    binding: 0,
                    visibility: wgpu::ShaderStages::VERTEX_FRAGMENT,
                    ty: wgpu::BindingType::Buffer {
                        ty: wgpu::BufferBindingType::Uniform,
                        has_dynamic_offset: false,
                        min_binding_size: None,
                    },
                    count: None,
                },
                wgpu::BindGroupLayoutEntry {
                    binding: 1,
                    visibility: wgpu::ShaderStages::FRAGMENT,
                    ty: wgpu::BindingType::Buffer {
                        ty: wgpu::BufferBindingType::Storage { read_only: true },
                        has_dynamic_offset: false,
                        min_binding_size: None,
                    },
                    count: None,
                },
                wgpu::BindGroupLayoutEntry {
                    binding: 2,
                    visibility: wgpu::ShaderStages::FRAGMENT,
                    ty: wgpu::BindingType::Texture {
                        sample_type: wgpu::TextureSampleType::Float { filterable: true },
                        view_dimension: wgpu::TextureViewDimension::D2,
                        multisampled: false,
                    },
                    count: None,
                },
                wgpu::BindGroupLayoutEntry {
                    binding: 3,
                    visibility: wgpu::ShaderStages::FRAGMENT,
                    ty: wgpu::BindingType::Sampler(wgpu::SamplerBindingType::Filtering),
                    count: None,
                },
            ],
        });
        let pipeline_layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
            label: Some("vektör boru hattı düzeni"),
            bind_group_layouts: &[Some(&bind_group_layout)],
            immediate_size: 0,
        });
        let sampler = device.create_sampler(&wgpu::SamplerDescriptor {
            label: Some("rampa örnekleyici"),
            address_mode_u: wgpu::AddressMode::ClampToEdge,
            address_mode_v: wgpu::AddressMode::ClampToEdge,
            mag_filter: wgpu::FilterMode::Linear,
            min_filter: wgpu::FilterMode::Linear,
            ..Default::default()
        });
        let view_buffer = device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("görünüm"),
            size: std::mem::size_of::<GpuView>() as u64,
            usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let paint_capacity = 256;
        let paint_buffer = create_paint_buffer(&device, paint_capacity);
        let ramp_capacity = 64;
        let ramp_texture = create_ramp_texture(&device, ramp_capacity);
        let bind_group = create_bind_group(
            &device,
            &bind_group_layout,
            &view_buffer,
            &paint_buffer,
            &ramp_texture,
            &sampler,
        );
        let instance_capacity = 1024;
        let instance_buffer = create_instance_buffer(&device, instance_capacity);
        let mut renderer = Renderer {
            device,
            queue,
            info,
            shader,
            pipeline_layout,
            bind_group_layout,
            pipelines: HashMap::new(),
            sampler,
            view_buffer,
            paints: PaintTable::default(),
            paint_buffer,
            paint_capacity,
            ramp_texture,
            ramp_capacity,
            bind_group,
            instance_buffer,
            instance_capacity,
            msaa: None,
            background: GpuMesh(Arc::new(GpuMeshData {
                buffers: None,
                index_count: 0,
            })),
        };
        renderer.background = renderer.upload(&unit_square());
        renderer
    }

    pub fn device(&self) -> &wgpu::Device {
        &self.device
    }

    pub fn queue(&self) -> &wgpu::Queue {
        &self.queue
    }

    pub fn adapter_info(&self) -> &wgpu::AdapterInfo {
        &self.info
    }

    /// Ağı grafik kartına yükler.
    pub fn upload(&mut self, mesh: &Mesh) -> GpuMesh {
        if mesh.is_empty() {
            return GpuMesh(Arc::new(GpuMeshData {
                buffers: None,
                index_count: 0,
            }));
        }
        let global: Vec<u32> = mesh.paints.iter().map(|p| self.paints.intern(p)).collect();
        let vertices: Vec<MeshVertex> = mesh
            .vertices
            .iter()
            .map(|v| MeshVertex {
                position: v.position,
                paint: global[v.paint as usize],
            })
            .collect();
        let vb = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("ağ köşeleri"),
                contents: bytemuck::cast_slice(&vertices),
                usage: wgpu::BufferUsages::VERTEX,
            });
        let ib = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("ağ üçgenleri"),
                contents: bytemuck::cast_slice(&mesh.indices),
                usage: wgpu::BufferUsages::INDEX,
            });
        GpuMesh(Arc::new(GpuMeshData {
            buffers: Some((vb, ib)),
            index_count: mesh.indices.len() as u32,
        }))
    }

    fn pipeline(&mut self, format: wgpu::TextureFormat) -> &wgpu::RenderPipeline {
        let device = &self.device;
        let shader = &self.shader;
        let layout = &self.pipeline_layout;
        self.pipelines.entry(format).or_insert_with(|| {
            device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
                label: Some("vektör boru hattı"),
                layout: Some(layout),
                vertex: wgpu::VertexState {
                    module: shader,
                    entry_point: Some("vs_main"),
                    compilation_options: Default::default(),
                    buffers: &[
                        Some(wgpu::VertexBufferLayout {
                            array_stride: std::mem::size_of::<MeshVertex>() as u64,
                            step_mode: wgpu::VertexStepMode::Vertex,
                            attributes: &wgpu::vertex_attr_array![0 => Float32x2, 1 => Uint32],
                        }),
                        Some(wgpu::VertexBufferLayout {
                            array_stride: std::mem::size_of::<GpuInstance>() as u64,
                            step_mode: wgpu::VertexStepMode::Instance,
                            attributes: &wgpu::vertex_attr_array![
                                2 => Float32x4, 3 => Float32x4, 4 => Float32x4, 5 => Float32x4
                            ],
                        }),
                    ],
                },
                primitive: wgpu::PrimitiveState {
                    topology: wgpu::PrimitiveTopology::TriangleList,
                    cull_mode: None,
                    ..Default::default()
                },
                depth_stencil: None,
                multisample: wgpu::MultisampleState {
                    count: SAMPLE_COUNT,
                    mask: !0,
                    alpha_to_coverage_enabled: false,
                },
                fragment: Some(wgpu::FragmentState {
                    module: shader,
                    entry_point: Some("fs_main"),
                    compilation_options: Default::default(),
                    targets: &[Some(wgpu::ColorTargetState {
                        format,
                        blend: Some(wgpu::BlendState::PREMULTIPLIED_ALPHA_BLENDING),
                        write_mask: wgpu::ColorWrites::ALL,
                    })],
                }),
                multiview_mask: None,
                cache: None,
            })
        })
    }

    /// Boya tablosundaki yenilikleri grafik kartına gönderir.
    fn flush_paints(&mut self) {
        if !self.paints.dirty {
            return;
        }
        let mut rebind = false;
        if self.paints.records.len() > self.paint_capacity {
            while self.paint_capacity < self.paints.records.len() {
                self.paint_capacity *= 2;
            }
            self.paint_buffer = create_paint_buffer(&self.device, self.paint_capacity);
            rebind = true;
        }
        let rows = self.paints.ramp_rows().max(1);
        if rows > self.ramp_capacity {
            while self.ramp_capacity < rows {
                self.ramp_capacity *= 2;
            }
            self.ramp_texture = create_ramp_texture(&self.device, self.ramp_capacity);
            rebind = true;
        }
        self.queue.write_buffer(
            &self.paint_buffer,
            0,
            bytemuck::cast_slice(&self.paints.records),
        );
        if !self.paints.ramps.is_empty() {
            self.queue.write_texture(
                wgpu::TexelCopyTextureInfo {
                    texture: &self.ramp_texture,
                    mip_level: 0,
                    origin: wgpu::Origin3d::ZERO,
                    aspect: wgpu::TextureAspect::All,
                },
                bytemuck::cast_slice(&self.paints.ramps),
                wgpu::TexelCopyBufferLayout {
                    offset: 0,
                    bytes_per_row: Some((RAMP_WIDTH * 4) as u32),
                    rows_per_image: None,
                },
                wgpu::Extent3d {
                    width: RAMP_WIDTH as u32,
                    height: self.paints.ramp_rows(),
                    depth_or_array_layers: 1,
                },
            );
        }
        if rebind {
            self.bind_group = create_bind_group(
                &self.device,
                &self.bind_group_layout,
                &self.view_buffer,
                &self.paint_buffer,
                &self.ramp_texture,
                &self.sampler,
            );
        }
        self.paints.dirty = false;
    }

    fn msaa_view(&mut self, format: wgpu::TextureFormat, size: UVec2) -> wgpu::TextureView {
        if let Some(m) = &self.msaa
            && m.format == format
            && m.size == size
        {
            return m.view.clone();
        }
        let texture = self.device.create_texture(&wgpu::TextureDescriptor {
            label: Some("MSAA hedefi"),
            size: wgpu::Extent3d {
                width: size.x,
                height: size.y,
                depth_or_array_layers: 1,
            },
            mip_level_count: 1,
            sample_count: SAMPLE_COUNT,
            dimension: wgpu::TextureDimension::D2,
            format,
            usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
            view_formats: &[],
        });
        let view = texture.create_view(&wgpu::TextureViewDescriptor::default());
        self.msaa = Some(MsaaTarget {
            format,
            size,
            view: view.clone(),
        });
        view
    }

    /// Çizim listesini hedef dokuya çizer. `format`, hedef görünümün biçimidir ve "sRGB"
    /// olmamalıdır (renkler sRGB uzayında karışsın diye).
    pub fn render(
        &mut self,
        target: &wgpu::TextureView,
        format: wgpu::TextureFormat,
        viewport: &Viewport,
        list: &DrawList,
    ) {
        let size = viewport.physical;
        if size.x == 0 || size.y == 0 {
            return;
        }
        // Arka plan, mantıksal alanı kaplayan bir kare olarak listenin başına eklenir.
        let mut items = Vec::with_capacity(list.items.len() + 1);
        if list.clear.a > 0.0 {
            let bg = GpuInstance::new(
                Affine2::from_scale(viewport.logical),
                ColorTransform::multiply(list.clear),
            );
            items.push((self.background.clone(), bg));
        }
        items.extend(list.items.iter().cloned());

        self.flush_paints();
        if items.len() > self.instance_capacity {
            while self.instance_capacity < items.len() {
                self.instance_capacity *= 2;
            }
            self.instance_buffer = create_instance_buffer(&self.device, self.instance_capacity);
        }
        let instances: Vec<GpuInstance> = items.iter().map(|(_, i)| *i).collect();
        self.queue
            .write_buffer(&self.instance_buffer, 0, bytemuck::cast_slice(&instances));
        let (row0, row1) = affine_rows(viewport.clip_transform());
        let view = GpuView {
            row0,
            row1,
            ramp: [self.ramp_capacity as f32, 0.0, 0.0, 0.0],
        };
        self.queue
            .write_buffer(&self.view_buffer, 0, bytemuck::bytes_of(&view));

        let msaa = self.msaa_view(format, size);
        self.pipeline(format);
        let Some(pipeline) = self.pipelines.get(&format) else {
            return;
        };
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("çizim"),
            });
        {
            let bar = LETTERBOX_COLOR;
            let mut pass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
                label: Some("vektör geçişi"),
                color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                    view: &msaa,
                    depth_slice: None,
                    resolve_target: Some(target),
                    ops: wgpu::Operations {
                        load: wgpu::LoadOp::Clear(wgpu::Color {
                            r: f64::from(bar.r),
                            g: f64::from(bar.g),
                            b: f64::from(bar.b),
                            a: f64::from(bar.a),
                        }),
                        store: wgpu::StoreOp::Discard,
                    },
                })],
                depth_stencil_attachment: None,
                timestamp_writes: None,
                occlusion_query_set: None,
                multiview_mask: None,
            });
            // Mantıksal alanın dışına taşan çizimler (ör. paralaks katmanları) kırpılır.
            let (origin, extent) = viewport.content_rect();
            let x0 = origin.x.floor().max(0.0) as u32;
            let y0 = origin.y.floor().max(0.0) as u32;
            let x1 = ((origin.x + extent.x).ceil() as u32).min(size.x);
            let y1 = ((origin.y + extent.y).ceil() as u32).min(size.y);
            pass.set_scissor_rect(
                x0,
                y0,
                x1.saturating_sub(x0).max(1),
                y1.saturating_sub(y0).max(1),
            );
            pass.set_pipeline(pipeline);
            pass.set_bind_group(0, &self.bind_group, &[]);
            pass.set_vertex_buffer(1, self.instance_buffer.slice(..));
            for (i, (mesh, _)) in items.iter().enumerate() {
                let Some((vb, ib)) = &mesh.0.buffers else {
                    continue;
                };
                pass.set_vertex_buffer(0, vb.slice(..));
                pass.set_index_buffer(ib.slice(..), wgpu::IndexFormat::Uint32);
                let i = i as u32;
                pass.draw_indexed(0..mesh.0.index_count, 0, i..i + 1);
            }
        }
        self.queue.submit([encoder.finish()]);
    }

    /// Çizim listesini ekransız bir resme çizer.
    pub fn render_to_image(
        &mut self,
        viewport: &Viewport,
        list: &DrawList,
    ) -> Result<RgbaImage, RenderError> {
        let size = viewport.physical;
        let texture = self.device.create_texture(&wgpu::TextureDescriptor {
            label: Some("ekransız hedef"),
            size: wgpu::Extent3d {
                width: size.x,
                height: size.y,
                depth_or_array_layers: 1,
            },
            mip_level_count: 1,
            sample_count: 1,
            dimension: wgpu::TextureDimension::D2,
            format: IMAGE_FORMAT,
            usage: wgpu::TextureUsages::RENDER_ATTACHMENT | wgpu::TextureUsages::COPY_SRC,
            view_formats: &[],
        });
        let view = texture.create_view(&wgpu::TextureViewDescriptor::default());
        self.render(&view, IMAGE_FORMAT, viewport, list);

        let unpadded = size.x * 4;
        let padded = unpadded.div_ceil(wgpu::COPY_BYTES_PER_ROW_ALIGNMENT)
            * wgpu::COPY_BYTES_PER_ROW_ALIGNMENT;
        let buffer = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("okuma"),
            size: u64::from(padded) * u64::from(size.y),
            usage: wgpu::BufferUsages::COPY_DST | wgpu::BufferUsages::MAP_READ,
            mapped_at_creation: false,
        });
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("okuma"),
            });
        encoder.copy_texture_to_buffer(
            wgpu::TexelCopyTextureInfo {
                texture: &texture,
                mip_level: 0,
                origin: wgpu::Origin3d::ZERO,
                aspect: wgpu::TextureAspect::All,
            },
            wgpu::TexelCopyBufferInfo {
                buffer: &buffer,
                layout: wgpu::TexelCopyBufferLayout {
                    offset: 0,
                    bytes_per_row: Some(padded),
                    rows_per_image: None,
                },
            },
            wgpu::Extent3d {
                width: size.x,
                height: size.y,
                depth_or_array_layers: 1,
            },
        );
        let index = self.queue.submit([encoder.finish()]);
        let (tx, rx) = std::sync::mpsc::channel();
        buffer.map_async(wgpu::MapMode::Read, .., move |r| {
            let _ = tx.send(r);
        });
        self.device
            .poll(wgpu::PollType::Wait {
                submission_index: Some(index),
                timeout: None,
            })
            .map_err(|e| RenderError::Readback(e.to_string()))?;
        rx.recv()
            .map_err(|e| RenderError::Readback(e.to_string()))?
            .map_err(|e| RenderError::Readback(e.to_string()))?;
        let mut image = RgbaImage::new(size.x, size.y);
        {
            let mapped = buffer
                .get_mapped_range(..)
                .map_err(|e| RenderError::Readback(e.to_string()))?;
            for y in 0..size.y as usize {
                let src = &mapped[y * padded as usize..y * padded as usize + unpadded as usize];
                let dst = &mut image.data[y * unpadded as usize..(y + 1) * unpadded as usize];
                dst.copy_from_slice(src);
            }
        }
        buffer.unmap();
        unpremultiply(&mut image);
        Ok(image)
    }
}

/// Grafik kartı seçer: önce gerçek bir kart, yoksa yazılımla çalışan yedek kart.
pub fn request_adapter(
    instance: &wgpu::Instance,
    surface: Option<&wgpu::Surface<'_>>,
) -> Result<wgpu::Adapter, RenderError> {
    let first = pollster::block_on(instance.request_adapter(&wgpu::RequestAdapterOptions {
        power_preference: wgpu::PowerPreference::HighPerformance,
        force_fallback_adapter: false,
        compatible_surface: surface,
        apply_limit_buckets: false,
    }));
    match first {
        Ok(a) => Ok(a),
        Err(e) => pollster::block_on(instance.request_adapter(&wgpu::RequestAdapterOptions {
            power_preference: wgpu::PowerPreference::HighPerformance,
            force_fallback_adapter: true,
            compatible_surface: surface,
            apply_limit_buckets: false,
        }))
        .map_err(|e2| RenderError::NoAdapter(format!("{e}; yedek kart: {e2}"))),
    }
}

fn unpremultiply(image: &mut RgbaImage) {
    for px in image.data.chunks_exact_mut(4) {
        let a = px[3];
        if a == 0 || a == 255 {
            continue;
        }
        for c in &mut px[..3] {
            *c = ((u32::from(*c) * 255 + u32::from(a) / 2) / u32::from(a)).min(255) as u8;
        }
    }
}

fn unit_square() -> Mesh {
    let v = |x: f32, y: f32| MeshVertex {
        position: Vec2::new(x, y).into(),
        paint: 0,
    };
    Mesh {
        vertices: vec![v(0.0, 0.0), v(1.0, 0.0), v(1.0, 1.0), v(0.0, 1.0)],
        indices: vec![0, 1, 2, 0, 2, 3],
        paints: vec![crate::paint::Paint::Solid(Color::WHITE)],
    }
}

fn create_paint_buffer(device: &wgpu::Device, capacity: usize) -> wgpu::Buffer {
    device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("boya tablosu"),
        size: (capacity * std::mem::size_of::<GpuPaint>()) as u64,
        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    })
}

fn create_ramp_texture(device: &wgpu::Device, rows: u32) -> wgpu::Texture {
    device.create_texture(&wgpu::TextureDescriptor {
        label: Some("degrade rampaları"),
        size: wgpu::Extent3d {
            width: RAMP_WIDTH as u32,
            height: rows,
            depth_or_array_layers: 1,
        },
        mip_level_count: 1,
        sample_count: 1,
        dimension: wgpu::TextureDimension::D2,
        format: wgpu::TextureFormat::Rgba8Unorm,
        usage: wgpu::TextureUsages::TEXTURE_BINDING | wgpu::TextureUsages::COPY_DST,
        view_formats: &[],
    })
}

fn create_instance_buffer(device: &wgpu::Device, capacity: usize) -> wgpu::Buffer {
    device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("örnekler"),
        size: (capacity * std::mem::size_of::<GpuInstance>()) as u64,
        usage: wgpu::BufferUsages::VERTEX | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    })
}

fn create_bind_group(
    device: &wgpu::Device,
    layout: &wgpu::BindGroupLayout,
    view: &wgpu::Buffer,
    paints: &wgpu::Buffer,
    ramps: &wgpu::Texture,
    sampler: &wgpu::Sampler,
) -> wgpu::BindGroup {
    let ramp_view = ramps.create_view(&wgpu::TextureViewDescriptor::default());
    device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("vektör bağlama"),
        layout,
        entries: &[
            wgpu::BindGroupEntry {
                binding: 0,
                resource: view.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 1,
                resource: paints.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 2,
                resource: wgpu::BindingResource::TextureView(&ramp_view),
            },
            wgpu::BindGroupEntry {
                binding: 3,
                resource: wgpu::BindingResource::Sampler(sampler),
            },
        ],
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn color_transform_composition() {
        let a = ColorTransform::alpha(0.5);
        let b = ColorTransform {
            mul: [0.5, 1.0, 1.0, 1.0],
            add: [0.1, 0.0, 0.0, 0.0],
        };
        let c = a.then(b);
        assert_eq!(c.mul, [0.5, 1.0, 1.0, 0.5]);
        assert_eq!(c.add, [0.1, 0.0, 0.0, 0.0]);
        assert_eq!(ColorTransform::IDENTITY.then(a), a);
    }

    #[test]
    fn unpremultiply_restores_color() {
        let mut img = RgbaImage::filled(1, 1, [64, 32, 0, 128]);
        unpremultiply(&mut img);
        assert_eq!(img.pixel(0, 0), [128, 64, 0, 128]);
    }
}
