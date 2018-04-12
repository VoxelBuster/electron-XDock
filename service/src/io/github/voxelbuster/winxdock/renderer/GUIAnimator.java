package io.github.voxelbuster.winxdock.renderer;

/**
 * A thing that does animation math.
 */
public class GUIAnimator {
    private int maxFrames = 0;
    private int currentFrame = 0, frozenFrame = 0;
    private boolean loop = true, reverse = false, freeze = false;

    /**
     * Creates a new animator with the given number of frames.
     * @param frames
     */
    public GUIAnimator(int frames) {
        this.maxFrames = frames;
    }

    /**
     * Advances and returns the frame based on whether or not the animation is reversed or looped.
     * @return currentFrame
     */
    public int advance() {
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

    public int setFrame(int i) {
        if (i >= maxFrames) {
            return currentFrame;
        }
        currentFrame = i;
        if (!freeze) {
            frozenFrame = currentFrame;
        }
        return currentFrame;
    }

    /**
     * Sets whether or not the animation should play backwards.
     * @param flag
     */
    public void setReverse(boolean flag) {
        this.reverse = flag;
    }

    /**
     * Sets whether or not the animation should be allowed to advance.
     * @param flag
     */
    public void setFrozen(boolean flag) {
        this.freeze = flag;
    }

    public int getCurrentFrame() {
        if (!freeze) {
            return currentFrame;
        } else {
            return frozenFrame;
        }
    }

    /**
     * <pre>
     * Unfreezes and sets the current frame to zero. Clears being reversed.
     * The same as running:
     *
     * setFrozen(false);
     * setReverse(false);
     * setFrame(0);
     * </pre>
     */
    public void reset() {
        setFrozen(false);
        setReverse(false);
        setFrame(0);
    }

    /**
     * Sets if the animator will loop.
     * True by default.
     * @param loop
     */
    public void setLoop(boolean loop) {
        this.loop = loop;
    }

    public boolean getLoop() {
        return loop;
    }

    public boolean getReverse() {
        return reverse;
    }
}
