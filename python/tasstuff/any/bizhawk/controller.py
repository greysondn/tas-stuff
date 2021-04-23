class Button():
    def __init__(self, name, onString, offString="."):
        self.pressed = False
        self.held    = False
        self.name    = name
        self.onStr   = onString
        self.offStr  = offString
    
    def update(self):
        if (self.pressed):
            if (not self.held):
                self.pressed = False
    
    def press(self):
        self.pressed = True
    
    def hold(self):
        self.pressed = True
        self.held    = True
    
    def release(self):
        self.pressed = False
        self.held    = False
    
    def __repr__(self):
        ret = self.offStr

        if self.pressed:
            ret = self.onStr

        return ret

