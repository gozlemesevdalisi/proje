function onEnterFrame()
{
   var _loc5_;
   if(!loaded)
   {
      _loc5_ = _root.getBytesLoaded() / _root.getBytesTotal();
      if(_loc5_ >= 1)
      {
         if(firstframe)
         {
            _parent.nextFrame();
         }
         else
         {
            this.play();
            bar._x = initX;
         }
         loaded = true;
      }
      else
      {
         bar._x = initX + (_loc5_ - 1) * bar._width;
      }
   }
   var _loc6_ = getTimer() - time;
   timeAccum += _loc6_;
   var _loc4_;
   while(timeAccum >= FRAME_TIME)
   {
      _loc4_ = 0;
      while(_loc4_ < timeClips.length)
      {
         if(timeClips[_loc4_]._currentframe < timeClips[_loc4_]._totalframes)
         {
            timeClips[_loc4_].nextFrame();
         }
         else
         {
            timeClips[_loc4_].gotoAndStop(1);
         }
         _loc4_ = _loc4_ + 1;
      }
      if(loaded && _currentframe < _totalframes)
      {
         nextFrame();
      }
      timeAccum -= FRAME_TIME;
   }
   time += _loc6_;
   firstframe = false;
}
stop();
var initX = bar._x;
var time = getTimer();
var FRAME_TIME = 33.333333333333336;
var timeAccum = 0;
var firstframe = true;
var loaded = false;
timeClips = [bargfx,tank.mc0,tank.mc1,tank.mc2,tank.mc3,tank.mc4,tank.mc4.mc0,tank.mc4.mc1,tank.mc4.mc0.mc0,tank.mc4.mc0.mc0.mc0.mc0,tank.mc4.mc0.mc0.mc0.mc1,tank.mc4.mc0.mc0.mc0.mc2,tank.mc4.mc0.mc0.mc0.mc3,tank.mc4.mc0.mc0.mc1,tank.mc4.mc0.mc0.mc2,tank.mc5.mc0];
var i = 0;
while(i < timeClips.length)
{
   timeClips[i].stop();
   i++;
}
