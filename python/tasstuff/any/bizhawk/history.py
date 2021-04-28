class PianoRollEntry():
    # at the end of the day, this is just a frame and a set of inputs
    def __init__(self, inpt="", frame=-1):
        self.input = inpt
        self.frame = frame

class PianoRoll():
    def __init__(self):
        # this is a little more complex, I think
        self.frames = []
        self.currentFrame = 0
    
    def addFrame(self, inpt):
        swp = PianoRollEntry(inpt, self.currentFrame)
        self.frames.append(swp)
        self.currentFrame = self.currentFrame + 1