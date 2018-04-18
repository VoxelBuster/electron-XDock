class GUIAnimator():
    def __init__(self, frames):
        self.maxFrames = frames
        self.reverse = False
        self.loop = False
        self.freeze = False
        self.currentFrame = 0
        self.frozenFrame = 0

    def advance(self):
        if self.reverse:
            self.currentFrame -= 1
            if self.currentFrame < 0:
                if self.loop:
                    self.currentFrame = self.maxFrames - 1
                else:
                    self.currentFrame += 1
        else:
            self.currentFrame += 1
        if self.currentFrame >= self.maxFrames - 1:
            if self.loop:
                self.currentFrame = 0
            else:
                self.currentFrame -= 1
        if not self.freeze:
            self.frozenFrame = self.currentFrame
            return self.currentFrame
        else:
            return self.frozenFrame

    def setFrame(self, i):
        if i >= self.maxFrames:
            return self.currentFrame
        self.currentFrame = i
        if not self.freeze:
            self.frozenFrame = self.currentFrame
        return self.currentFrame

    def setReverse(self, flag):
        self.reverse = flag

    def setFrozen(self, flag):
        self.freeze = flag

    def getCurrentFrame(self):
        if not self.freeze:
            return self.currentFrame
        else:
            return self.frozenFrame

    def reset(self):
        self.freeze = False
        self.reverse = False
        self.currentFrame = 0
        self.frozenFrame = 0

    def getLoop(self):
        return self.loop

    def getReverse(self):
        return self.reverse
