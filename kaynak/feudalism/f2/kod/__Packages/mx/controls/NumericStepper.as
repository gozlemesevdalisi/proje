class mx.controls.NumericStepper extends mx.core.UIComponent
{
   var StepTrack_mc;
   var __height;
   var __maxChars;
   var __set__visible;
   var __width;
   var _parent;
   var _visible;
   var boundingBox_mc;
   var createClassObject;
   var createObject;
   var dispatchEvent;
   var enabled;
   var focusTextField;
   var inputField;
   var nextButton_mc;
   var owner;
   var prevButton_mc;
   var setSize;
   var tabChildren;
   var tabEnabled;
   static var symbolName = "NumericStepper";
   static var symbolOwner = mx.controls.NumericStepper;
   static var version = "2.0.2.126";
   var className = "NumericStepper";
   var upArrowUp = "StepUpArrowUp";
   var upArrowDown = "StepUpArrowDown";
   var upArrowOver = "StepUpArrowOver";
   var upArrowDisabled = "StepUpArrowDisabled";
   var downArrowUp = "StepDownArrowUp";
   var downArrowDown = "StepDownArrowDown";
   var downArrowOver = "StepDownArrowOver";
   var downArrowDisabled = "StepDownArrowDisabled";
   var skinIDUpArrow = 10;
   var skinIDDownArrow = 11;
   var skinIDInput = 9;
   var initializing = true;
   var __visible = true;
   var __minimum = 0;
   var __maximum = 10;
   var __stepSize = 1;
   var __value = 0;
   var __nextValue = 0;
   var __previousValue = 0;
   var clipParameters = {minimum:1,maximum:1,stepSize:1,value:1,maxChars:1};
   static var mergedClipParameters = mx.core.UIObject.mergeClipParameters(mx.controls.NumericStepper.prototype.clipParameters,mx.core.UIComponent.prototype.clipParameters);
   function NumericStepper()
   {
      super();
   }
   function init()
   {
      super.init();
      this.boundingBox_mc._visible = false;
      this.boundingBox_mc._width = this.boundingBox_mc._height = 0;
      this._visible = false;
      this.tabEnabled = false;
      this.tabChildren = true;
   }
   function setVisible(x, noEvent)
   {
      super.setVisible(x,noEvent);
      if(this.initializing)
      {
         this.__visible = x;
      }
   }
   function layoutControl()
   {
      this.nextButton_mc._x = this.__width - this.nextButton_mc.__width;
      this.nextButton_mc._y = 0;
      this.prevButton_mc._x = this.__width - this.prevButton_mc.__width;
      this.prevButton_mc._y = this.__height - this.prevButton_mc.__height;
      this.inputField.setSize(this.__width - this.nextButton_mc.__width,this.__height);
      this.StepTrack_mc._width = Math.max(this.nextButton_mc.__width,this.prevButton_mc.__width);
      this.StepTrack_mc._x = this.__width - this.StepTrack_mc._width;
      this.StepTrack_mc._height = this.__height - (this.nextButton_mc._height + this.prevButton_mc._height);
      this.StepTrack_mc._y = this.nextButton_mc.__height;
   }
   function createChildren()
   {
      super.createChildren();
      this.addAsset("nextButton_mc",this.skinIDUpArrow);
      this.addAsset("prevButton_mc",this.skinIDDownArrow);
      this.addAsset("inputField",this.skinIDInput);
      this.focusTextField = this.inputField.label;
      this.createObject("StepTrack","StepTrack_mc",2);
      this.size();
   }
   function draw()
   {
      this.prevButton_mc.enabled = this.enabled;
      this.nextButton_mc.enabled = this.enabled;
      this.inputField.enabled = this.enabled;
      this.size();
      this.initializing = false;
      this.visible = this.__visible;
   }
   function size()
   {
      var _loc2_ = this.calcMinHeight();
      var _loc3_ = this.calcMinWidth();
      if(this.__height < _loc2_)
      {
         this.setSize(this.__width,_loc2_);
      }
      if(this.__width < _loc3_)
      {
         this.setSize(_loc3_,this.__height);
      }
      this.layoutControl();
   }
   function calcMinHeight()
   {
      return 22;
   }
   function calcMinWidth()
   {
      return 40;
   }
   function addAsset(id, skinID)
   {
      var _loc2_ = new Object();
      _loc2_.styleName = this;
      var _loc5_;
      var _loc3_;
      var _loc4_;
      if(skinID == 10)
      {
         _loc2_.falseUpSkin = this.upArrowUp;
         _loc2_.falseOverSkin = this.upArrowOver;
         _loc2_.falseDownSkin = this.upArrowDown;
         _loc2_.falseDisabledSkin = this.upArrowDisabled;
         this.createClassObject(mx.controls.SimpleButton,id,skinID,_loc2_);
         _loc5_ = this.nextButton_mc;
         _loc5_.tabEnabled = false;
         _loc5_.styleName = this;
         _loc5_._x = this.__width - _loc5_.__width;
         _loc5_._y = 0;
         _loc5_.owner = this;
         _loc5_.autoRepeat = true;
         _loc5_.clickHandler = function()
         {
            Selection.setSelection(0,0);
         };
         _loc5_.buttonDownHandler = function()
         {
            this.owner.buttonPress(this);
         };
      }
      else if(skinID == 11)
      {
         _loc2_.falseUpSkin = this.downArrowUp;
         _loc2_.falseOverSkin = this.downArrowOver;
         _loc2_.falseDownSkin = this.downArrowDown;
         _loc2_.falseDisabledSkin = this.downArrowDisabled;
         this.createClassObject(mx.controls.SimpleButton,id,skinID,_loc2_);
         _loc3_ = this.prevButton_mc;
         _loc3_.tabEnabled = false;
         _loc3_.styleName = this;
         _loc3_._x = this.__width - _loc3_.__width;
         _loc3_._y = this.__height - _loc3_.__height;
         _loc3_.owner = this;
         _loc3_.autoRepeat = true;
         _loc3_.clickHandler = function()
         {
            Selection.setSelection(0,0);
         };
         _loc3_.buttonDownHandler = function()
         {
            this.owner.buttonPress(this);
         };
      }
      else if(skinID == 9)
      {
         this.createClassObject(mx.controls.TextInput,id,skinID);
         _loc4_ = this.inputField;
         _loc4_.styleName = this;
         _loc4_.setSize(this.__width - this.nextButton_mc.__width,this.__height);
         _loc4_.restrict = "0-9\\-\\.\\,";
         _loc4_.maxChars = this.__maxChars;
         _loc4_.text = this.value;
         _loc4_.onSetFocus = function()
         {
            this._parent.onSetFocus();
         };
         _loc4_.onKillFocus = function()
         {
            this._parent.onKillFocus();
         };
         _loc4_.drawFocus = function(b)
         {
            this._parent.drawFocus(b);
         };
         _loc4_.onKeyDown = function()
         {
            this._parent.onFieldKeyDown();
         };
      }
   }
   function setFocus()
   {
      Selection.setFocus(this.inputField);
   }
   function onKillFocus()
   {
      mx.managers.SystemManager.form.focusManager.defaultPushButtonEnabled = true;
      super.onKillFocus();
      Key.removeListener(this.inputField);
      var _loc3_;
      if(Number(this.inputField.text) != this.value)
      {
         _loc3_ = this.checkValidValue(Number(this.inputField.text));
         this.inputField.text = _loc3_;
         this.value = _loc3_;
         this.dispatchEvent({type:"change"});
      }
   }
   function onSetFocus()
   {
      super.onSetFocus();
      Key.addListener(this.inputField);
      mx.managers.SystemManager.form.focusManager.defaultPushButtonEnabled = false;
   }
   function onFieldKeyDown()
   {
      var _loc2_ = this.value;
      var _loc3_;
      switch(Key.getCode())
      {
         case 40:
            _loc3_ = this.value - this.stepSize;
            this.value = _loc3_;
            if(_loc2_ != this.value)
            {
               this.dispatchEvent({type:"change"});
            }
            break;
         case 38:
            _loc3_ = this.stepSize + this.value;
            this.value = _loc3_;
            if(_loc2_ != this.value)
            {
               this.dispatchEvent({type:"change"});
            }
            break;
         case 36:
            this.inputField.text = this.minimum;
            this.value = this.minimum;
            if(_loc2_ != this.value)
            {
               this.dispatchEvent({type:"change"});
            }
            break;
         case 35:
            this.inputField.text = this.maximum;
            this.value = this.maximum;
            if(_loc2_ != this.value)
            {
               this.dispatchEvent({type:"change"});
            }
            break;
         case 13:
            this.value = Number(this.inputField.text);
            if(_loc2_ != this.value)
            {
               this.dispatchEvent({type:"change"});
            }
         default:
            return;
      }
   }
   function get nextValue()
   {
      if(this.checkRange(this.value + this.stepSize))
      {
         this.__nextValue = this.value + this.stepSize;
         return this.__nextValue;
      }
   }
   function get previousValue()
   {
      if(this.checkRange(this.__value - this.stepSize))
      {
         this.__previousValue = this.value - this.stepSize;
         return this.__previousValue;
      }
   }
   function set maxChars(num)
   {
      this.__maxChars = num;
      this.inputField.maxChars = this.__maxChars;
   }
   function get maxChars()
   {
      return this.__maxChars;
   }
   function get value()
   {
      return this.__value;
   }
   function set value(v)
   {
      var _loc2_ = this.checkValidValue(v);
      if(_loc2_ == this.__value)
      {
         return;
      }
      this.inputField.text = this.__value = _loc2_;
   }
   function get minimum()
   {
      return this.__minimum;
   }
   function set minimum(v)
   {
      this.__minimum = v;
   }
   function get maximum()
   {
      return this.__maximum;
   }
   function set maximum(v)
   {
      this.__maximum = v;
   }
   function get stepSize()
   {
      return this.__stepSize;
   }
   function set stepSize(v)
   {
      this.__stepSize = v;
   }
   function onFocus()
   {
   }
   function buttonPress(button)
   {
      var _loc2_ = this.value;
      if(button._name == "nextButton_mc")
      {
         this.value += this.stepSize;
      }
      else
      {
         this.value -= this.stepSize;
      }
      if(_loc2_ != this.value)
      {
         this.dispatchEvent({type:"change"});
         Selection.setSelection(0,0);
      }
   }
   function checkRange(v)
   {
      return v >= this.minimum and v <= this.maximum;
   }
   function checkValidValue(val)
   {
      var _loc7_ = val / this.stepSize;
      var _loc9_ = Math.floor(_loc7_);
      var _loc2_ = this.stepSize;
      var _loc6_ = this.minimum;
      var _loc5_ = this.maximum;
      var _loc8_;
      var _loc4_;
      if(val > _loc6_ and val < _loc5_)
      {
         if(_loc7_ - _loc9_ == 0)
         {
            return val;
         }
         _loc8_ = Math.floor(val / _loc2_);
         _loc4_ = _loc8_ * _loc2_;
         if(val - _loc4_ >= _loc2_ / 2 && _loc5_ >= _loc4_ + _loc2_ && _loc6_ <= _loc4_ - _loc2_ || val + _loc2_ == _loc5_ && _loc5_ - _loc4_ - _loc2_ > 1e-14)
         {
            _loc4_ += _loc2_;
         }
         return _loc4_;
      }
      if(val >= _loc5_)
      {
         return _loc5_;
      }
      return _loc6_;
   }
   function onLabelChanged(o)
   {
      var _loc2_ = this.checkValidValue(Number(o.text));
      o.text = _loc2_;
      this.value = _loc2_;
   }
   function get tabIndex()
   {
      return this.inputField.tabIndex;
   }
   function set tabIndex(w)
   {
      this.inputField.tabIndex = w;
   }
}
