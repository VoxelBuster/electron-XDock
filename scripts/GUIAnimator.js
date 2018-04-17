function GUIAnimator(frames) {
    this.maxFrames = frames;
    this.reverse = false;
    this.loop = false;
    this.freeze = false;
    this.currentFrame = 0;
    this.frozenFrame = 0;
    this.advance = function() {
       if (this.reverse) {
           this.currentFrame--;
           if (this.currentFrame < 0) {
               if (this.loop) {
                   this.currentFrame = this.maxFrames - 1;
               } else {
                   this.currentFrame++;
               }
           }
       } else {
           this.currentFrame++;
           if (this.currentFrame >= this.maxFrames - 1) {
               if (this.loop) {
                   this.currentFrame = 0;
               } else {
                   this.currentFrame--;
               }
           }
       }
       if (!this.freeze) {
           this.frozenFrame = this.currentFrame;
           return this.currentFrame;
       } else {
           return this.frozenFrame;
       }
   }

   this.setFrame = function(i) {
       if (i >= this.maxFrames) {
           return this.currentFrame;
       }
       this.currentFrame = i;
       if (!this.freeze) {
           this.frozenFrame = this.currentFrame;
       }
       return this.currentFrame;
   }

    this.setReverse = function(flag) {
        this.reverse = flag;
    }

    this.setFrozen = function(flag) {
        this.freeze = flag;
    }

    this.getCurrentFrame = function() {
        if (!this.freeze) {
            return this.currentFrame;
        } else {
            return this.frozenFrame;
        }
    }

    this.reset = function() {
        this.freeze = false;
        this.reverse = false;
        this.currentFrame = 0;
        this.frozenFrame = 0;
    }

    this.getLoop = function() {
        return loop;
    }

    this.getReverse = function() {
        return reverse;
    }
}
GUIAnimator.prototype.maxFrames = 1;
GUIAnimator.prototype.currentFrame = 0;
GUIAnimator.prototype.frozenFrame = 0;
GUIAnimator.prototype.loop = false;
GUIAnimator.prototype.reverse = false;
GUIAnimator.freeze = false;

module.exports.GUIAnimator = GUIAnimator;
