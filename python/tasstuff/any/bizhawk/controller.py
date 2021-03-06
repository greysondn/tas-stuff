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

    def fromMnemonic(self, mnemonic):
        # from a bizhawk mnemonic
        #
        # this assumes that:
        #
        # - singular inputs will override this to handle button presses
        #
        # - small input groups will override this to read their own mnemonics
        #   without bars surrounding it
        #
        # - full inputs will override this to read the mnemonics with bars in
        #   and around them
        # 
        # Bizhawk *technically* doesn't require specific characters for
        # mnemonics according to its documentation. I've not tested this, but
        # it is something to be aware of as overrides are written or if you try
        # to analyze them 
        self.release()

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

    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)

        if ("." == mnemonic):
            self.reset()
        else:
            self.press()

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

    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)

        self.press(float(mnemonic))

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

    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)

        raise NotImplementedError("No need for joysticks yet, so this isn't implemented, sorry!")

class SnesConsole(InputGroup):
    def __init__(self, name="SNES Console"):
        super().__init__(name)

        self.resetBttn = Button("Reset", "r")
        self.power     = Button("Power", "P")

        self.add(self.resetBttn)
        self.add(self.power)
    
    def __repr__(self):
        return (str(self.resetBttn) + str(self.power))

    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)

        # buttons
        self.resetBttn.fromMnemonic(mnemonic[0])
        self.power.fromMnemonic(mnemonic[1])

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

    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)

        msegs = mnemonic.split(",")

        # analogs
        self.x.fromMnemonic(msegs[0])
        self.y.fromMnemonic(msegs[1])

        # buttons
        self.l.fromMnemonic(msegs[2][0])
        self.r.fromMnemonic(msegs[2][1])

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

    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)

        # buttons, buttons, oh my the buttons
        self.up.fromMnemonic(    mnemonic[ 0])
        self.down.fromMnemonic(  mnemonic[ 1])
        self.left.fromMnemonic(  mnemonic[ 2])
        self.right.fromMnemonic( mnemonic[ 3])
        self.select.fromMnemonic(mnemonic[ 4])
        self.start.fromMnemonic( mnemonic[ 5])
        self.y.fromMnemonic(     mnemonic[ 6])
        self.b.fromMnemonic(     mnemonic[ 7])
        self.x.fromMnemonic(     mnemonic[ 8])
        self.a.fromMnemonic(     mnemonic[ 9])
        self.l.fromMnemonic(     mnemonic[10])
        self.r.fromMnemonic(     mnemonic[11])


# specifically, the controller group needed for mario paint
class SnesPreset_MarioPaint(InputGroup):
    def __init__(self, name="Mario Paint Controls"):
        super().__init__(name)

        self.console = SnesConsole()
        self.p1      = SnesMouse("Player 1")
        self.p2      = SnesController("Player 2")

        self.add(self.console)
        self.add(self.p1)
        self.add(self.p2)

        # the nouse needs bounds tweaked specifically for Mario Paint
        self.p1.x.max =  10
        self.p1.x.min = -10
        self.p1.y.max =  10
        self.p1.y.min = -10


        # and now for the misery
        # we alias an insane number of properties right here
        self.power     = self.console.power
        self.resetBttn = self.console.resetBttn

        self.mL = self.p1.l
        self.mR = self.p1.r
        self.mX = self.p1.x
        self.mY = self.p1.y

        self.up     = self.p2.up
        self.down   = self.p2.down
        self.left   = self.p2.left
        self.right  = self.p2.right
        self.select = self.p2.select
        self.start  = self.p2.start
        self.y      = self.p2.y
        self.b      = self.p2.b
        self.x      = self.p2.x
        self.a      = self.p2.a
        self.l      = self.p2.l
        self.r      = self.p2.r
    
    # from a bizhawk mnemonic string, that is
    def fromMnemonic(self, mnemonic):
        super().fromMnemonic(mnemonic)
        self.reset()
        
        mSegs = mnemonic.split("|")
        
        self.console.fromMnemonic(mSegs[1])
        self.p1.fromMnemonic(     mSegs[2])
        self.p2.fromMnemonic(     mSegs[3])


    # I think this part is cool, though
    def __repr__(self):
        return f"|{self.console}|{self.p1}|{self.p2}|"