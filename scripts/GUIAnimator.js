function GUIAnimator(frames) {
    this.maxFrames = frames;
    this.advance = function() {
       if (reverse) {
           currentFrame--;
           if (currentFrame < 0) {
               if (loop) {
                   currentFrame = maxFrames - 1;
               } else {
                   currentFrame++;
               }
           }
       } else {
           currentFrame++;
           if (currentFrame >= maxFrames - 1) {
               if (loop) {
                   currentFrame = 0;
               } else {
                   currentFrame--;
               }
           }
       }
       if (!freeze) {
           frozenFrame = currentFrame;
           return currentFrame;
       } else {
           return frozenFrame;
       }
   }

   this.setFrame = function(i) {
       if (i >= maxFrames) {
           return currentFrame;
       }
       currentFrame = i;
       if (!freeze) {
           frozenFrame = currentFrame;
       }
       return currentFrame;
   }

    this.setReverse = function(flag) {
        this.reverse = flag;
    }

    this.setFrozen = function(flag) {
        this.freeze = flag;
    }

    this.getCurrentFrame = function() {
        if (!freeze) {
            return currentFrame;
        } else {
            return frozenFrame;
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