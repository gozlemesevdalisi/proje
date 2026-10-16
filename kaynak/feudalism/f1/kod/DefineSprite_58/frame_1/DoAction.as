this.onEnterFrame = function()
{
   var _loc4_ = _root.getBytesLoaded() / _root.getBytesTotal();
   this.bar._xscale = _loc4_ * 100;
   this.percent_txt.text = Math.floor(_loc4_ * 100) + " %";
   if(_loc4_ >= 1)
   {
      _parent.nextFrame();
   }
};
