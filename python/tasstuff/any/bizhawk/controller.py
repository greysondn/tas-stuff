class Input():
    def __init__(self, name):
        self.name     = name
        self.held     = False
    
    def reset(self):
        pass

    def update(self):
        if (not self.held):
            self.reset()
    
    def hold(self):
        self.held = True
    
    def release(self):
        self.held = False

class InputGroup(Input):
    def __init__(self, name):
        super().__init__(name)
        self.children = []
    
    def reset(self):
        # children should manage themselves here
        super().reset()

    def update(self):
        super().update()

        for child in self.children:
            child.update()

    def hold(self):
        super().hold()

        for child in self.children:
            child.hold()
    
    def release(self):
        super().release()

        for child in self.children:
            child.release()
    
    def add(self, child):
        self.children.append(child)


class Button(Input):
    def __init__(self, name, onString, offString="."):
        super().__init__(name)

        self.pressed = False
        self.onStr   = onString
        self.offStr  = offString
    
    def reset(self):
        self.pressed = False
    
    def press(self):
        self.pressed = True
    
    def hold(self):
        super().hold()
        self.pressed = True
    
    def release(self):
        super().release()
        self.pressed = False
    
    def __repr__(self):
        ret = self.offStr

        if self.pressed:
            ret = self.onStr

        return ret

class AnalogInput(Input):
    def __init__(self, name, minVal, maxVal, center = 0):
        super().__init__(name)

        self.min     = minVal
        self.max     = maxVal
        self.center  = center
        self.current = center

    def __repr__(self):
        return str(float(self.current))

    def reset(self):
        super().reset()
        self.current = self.center

    def press(self, value):
        # we clamp it.
        val = value
        
        if (val > self.max):
            val = self.max
        
        if (val < self.min):
            val = self.min
        
        self.current = float(val)

class Joystick(InputGroup):
    def __init__(self, name, minX, maxX, minY, maxY, centerX=0, centerY=0):
        super().__init__(name)
        
        self.x    = AnalogInput(f"{name}_X", minX, maxX, centerX)
        self.y    = AnalogInput(f"{name}_Y", minY, maxY, centerY)

        self.add(self.x)
        self.add(self.y)
    
    def __repr__(self):
        return f"{self.x.current},{self.y.current}"
    
    def press(self, x, y):
        self.x.press(x)
        self.y.press(y)

class SnesConsole(InputGroup):
    def __init__(self, name="SNES Console"):
        super().__init__(name)

        self.reset = Button("Reset", "r")
        self.power = Button("Power", "P")

        self.add(self.reset)
        self.add(self.power)
    
    def __repr__(self):
        return (str(self.reset) + str(self.power))

class SnesMouse(InputGroup):
    def __init__(self, name="SNES Mouse"):
        super().__init__(name)

        self.x = AnalogInput(f"{name}_X", -127, 127)
        self.y = AnalogInput(f"{name}_Y", -127, 127)
        self.l = Button(f"{name}_L", "l")
        self.r = Button(f"{name}_R", "r")

        self.add(self.x)
        self.add(self.y)
        self.add(self.l)
        self.add(self.r)
    
    def __repr__(self):
        ret = ""
        ret = ret + str(int(self.x.current)).rjust(5, " ") + ","
        ret = ret + str(int(self.y.current)).rjust(5, " ") + ","
        ret = ret + str(self.l)
        ret = ret + str(self.r)
        return ret

# snes inputs
#    | mouse        | controller
# |rP|   -2,    4,lr|UDLRsSYBXAlr|
class SnesController(InputGroup):
    def __init__(self, name="SNES Controller"):
        super().__init__(name)

        self.up     = Button(   f"{name}_up",  "U")
        self.down   = Button( f"{name}_down",  "D")
        self.left   = Button( f"{name}_left",  "L")
        self.right  = Button(f"{name}_right", "R")

        self.select = Button(f"{name}_select", "s")
        self.start  = Button( f"{name}_start", "S")

        self.y      = Button(f"{name}_y",  "Y")
        self.b      = Button(f"{name}_b",  "B")
        self.x      = Button(f"{name}_x",  "X")
        self.a      = Button(f"{name}_a",  "A")
        self.l      = Button(f"{name}_l",  "l")
        self.r      = Button(f"{name}_r",  "r")

        self.add(self.up)
        self.add(self.down)
        self.add(self.left)
        self.add(self.right)
        self.add(self.select)
        self.add(self.start)
        self.add(self.y)
        self.add(self.b)
        self.add(self.x)
        self.add(self.a)
        self.add(self.l)
        self.add(self.r) 
    
    def __repr__(self):
        ret = ""
        ret = ret + f"{self.up}{self.down}{self.left}{self.right}"
        ret = ret + f"{self.select}{self.start}"
        ret = ret + f"{self.y}{self.b}{self.x}{self.a}{self.l}{self.r}"
        return ret