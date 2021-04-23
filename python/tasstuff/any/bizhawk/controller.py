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

class AnalogInput():
    def __init__(self, name, minVal, maxVal, center = 0):
        self.held    = False
        self.name    = name
        self.min     = minVal
        self.max     = maxVal
        self.center  = center
        self.current = center

    def __repr__(self):
        return str(float(self.current))

    def hold(self):
        self.held = True

    def release(self):
        self.held = False

    def update(self):
        if (not self.held):
            self.current = self.center

    def press(self, value):
        # we clamp it.
        val = value
        
        if (val > self.max):
            val = self.max
        
        if (val < self.min):
            val = self.min
        
        self.current = float(val)
        