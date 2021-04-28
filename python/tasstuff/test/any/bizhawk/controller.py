import unittest

import tasstuff.any.bizhawk.controller as controller

class Test_Input(unittest.TestCase):
    # there are no default args for constructor

    def test_constructor_args(self):
        tst = controller.Input("test")

        self.assertEqual(tst.name, "test")
        self.assertEqual(tst.held, False)

    def test_reset(self):
        # it does nothing. Just run it to make the thing happy.
        tst = controller.Input("test")

        tst.reset()

    def test_hold(self):
        tst = controller.Input("test")

        tst.hold()

        self.assertEqual(tst.held, True)
    
    def test_release(self):
        tst = controller.Input("test")

        tst.hold()
        tst.release()

        self.assertEqual(tst.held, False)

    def test_update(self):
        tst = controller.Input("test")

        # there's actually no output specific here
        # just run both versions of update so it's covered
        tst.update()
        tst.hold()
        tst.update()
        tst.release()
        tst.update()

class Test_InputGroup(unittest.TestCase):

    def create_group(self):
        ret = controller.InputGroup("test")
        but = controller.Input("test")
        ret.add(but)

        return ret

    # there is no defaulted constructor

    def test_constructor_args(self):
        tst = self.create_group()

        # the test group has a single child
        self.assertEqual(len(tst.children), 1)

    def test_add(self):
        tst = self.create_group()

        but = controller.Input("test")
        tst.add(but)

        self.assertIs(but, tst.children[1])

    # the rest of this I'm just running to make happy
    def test_lazy(self):
        tst = self.create_group()

        tst.reset()
        tst.update()
        tst.hold()
        tst.release()

class Test_Button(unittest.TestCase):

    def test_constructor_default(self):
        tst = controller.Button("NAME", "ONSTRING")

        self.assertEqual(tst.pressed, False)
        self.assertEqual(tst.held, False)
        self.assertEqual(tst.name, "NAME")
        self.assertEqual(tst.onStr, "ONSTRING")
        self.assertEqual(tst.offStr, ".")
    
    def test_constructor_args(self):
         tst = controller.Button("NAME", "ONSTRING", "OFFSTRING")
         
         self.assertEqual(tst.offStr, "OFFSTRING")

    def test_press(self):
        tst = controller.Button("testButton", "T")

        tst.press()

        self.assertEqual(tst.pressed, True)
    
    def test_hold(self):
        tst = controller.Button("testButton", "T")

        tst.hold()

        self.assertEqual(tst.pressed, True)
        self.assertEqual(tst.held, True)

    def test_release(self):
        tst = controller.Button("testButton", "T")

        tst.hold()
        tst.release()

        self.assertEqual(tst.pressed, False)
        self.assertEqual(tst.held, False)

    def test_update(self):
        tst = controller.Button("testButton", "T")

        # does update release pressed buttons?
        tst.press()
        tst.update()

        self.assertEqual(tst.pressed, False)

        # does update observe held status?
        tst.hold()
        tst.update()

        self.assertEqual(tst.pressed, True)
        self.assertEqual(tst.held, True)

    def test_repr(self):
        tst = controller.Button("testButton", "T")

        # unpressed
        self.assertEqual(str(tst), ".")

        # pressed
        tst.press()
        self.assertEqual(str(tst), "T")


class Test_AnalogInput(unittest.TestCase):

    def test_constructor_default(self):
        tst = controller.AnalogInput("test", -12, 12)

        self.assertEqual(tst.held, False)
        self.assertEqual(tst.name, "test")
        self.assertEqual(tst.min, -12.0)
        self.assertEqual(tst.max, 12.0)
        self.assertEqual(tst.center, 0.0)
        self.assertEqual(tst.current, 0.0)

    def test_constructor_args(self):
        tst = controller.AnalogInput("test", -12, 12, 9)

        self.assertEqual(tst.center, 9.0)
        self.assertEqual(tst.current, 9.0)

    def test_press(self):
        tst = controller.AnalogInput("Mouse X", -10, 10)

        # within bound
        tst.press(8)
        self.assertEqual(tst.current, 8.0)

        # out of bounds
        tst.press(-8675309)
        self.assertEqual(tst.current, -10.0)

        # again, other way
        tst.press(42)
        self.assertEqual(tst.current, 10.0)

    def test_hold(self):
        tst = controller.AnalogInput("Mouse X", -10, 10)
        
        tst.hold()

        self.assertEqual(tst.held, True)

    def test_release(self):
        tst = controller.AnalogInput("Mouse X", -10, 10)
        
        tst.hold()
        tst.release()

        self.assertEqual(tst.held, False)

    def test_update(self):
        tst = controller.AnalogInput("Mouse X", -10, 10)

        # not held
        tst.press(3.14)
        tst.update()
        self.assertEqual(tst.current, 0.0)

        # held
        tst.press(3.14)
        tst.hold()
        tst.update()
        self.assertEqual(tst.current, 3.14)

        # and now release
        tst.release()
        tst.update()
        self.assertEqual(tst.current, 0)

    def test_repr(self):
        tst = controller.AnalogInput("Mouse X", -10, 10)
        tst.press(6.28)

        self.assertEqual(str(tst), "6.28")

class Test_Joystick(unittest.TestCase):
    # there's not really anything to test in the constructor
    def test_constructor_lazy(self):
        controller.Joystick("test", -10, 10, -10, 10)
    
    def test_press(self):
        tst = controller.Joystick("test", -10, 10, -10, 10)

        tst.press(-3, 3)

        self.assertEqual(tst.x.current, -3)
        self.assertEqual(tst.y.current,  3)
    
    def test_repr(self):
        tst = controller.Joystick("test", -10, 10, -10, 10)

        tst.press(-4, 5)

        self.assertEqual(str(tst), "-4.0,5.0")

    def test_fromMnemonic(self):
        # literally just to raise the error, honestly, for coverage sake
        tst = controller.Joystick("test", -10, 10, -10, 10)

        with self.assertRaises(NotImplementedError):
             tst.fromMneumonic("the input here is irrelevant due to error")

class Test_SnesConsole(unittest.TestCase):
    # still not testing constructors, just going to jump to the next thing
    def test_repr(self):
        tst = controller.SnesConsole()

        # this is actually strictly defined so
        # unpressed
        self.assertEqual(str(tst), "..")

        # pressed
        tst.power.press()
        tst.resetBttn.press()

        self.assertEqual(str(tst), "rP")

class Test_SnesMouse(unittest.TestCase):
    # still not testing constructors, just going to jump to the next thing
    def test_repr(self):
        tst = controller.SnesMouse()

        # this is actually strictly defined so
        # unpressed
        self.assertEqual(str(tst), "    0,    0,..")

        # pressed
        tst.x.press(-2)
        tst.y.press(3)
        tst.l.press()
        tst.r.press()

        self.assertEqual(str(tst), "   -2,    3,lr")

class Test_SnesController(unittest.TestCase):
    # still not testing constructors, you know.
    def test_repr(self):
        tst = controller.SnesController()

        # this is actually strictly defined so...
        # unpressed
        self.assertEqual(str(tst), "............")

        # pressed
        tst.up.press()
        tst.down.press()
        tst.left.press()
        tst.right.press()
        tst.select.press()
        tst.start.press()
        tst.y.press()
        tst.b.press()
        tst.x.press()
        tst.a.press()
        tst.l.press()
        tst.r.press()

        self.assertEqual(str(tst), "UDLRsSYBXAlr")

class Test_SnesMarioPaintControllerGroup(unittest.TestCase):
    # won't test this constructor either
    def test_repr(self):
        tst = controller.SnesPreset_MarioPaint()

        # unpressed
        self.assertEqual(str(tst), "|..|    0,    0,..|............|")

        # pressed
        tst.power.press()
        tst.resetBttn.press()

        tst.mL.press()
        tst.mR.press()
        tst.mX.press(-4)
        tst.mY.press(8)

        tst.up.press()
        tst.down.press()
        tst.left.press()
        tst.right.press()
        tst.select.press()
        tst.start.press()
        tst.y.press()
        tst.b.press()
        tst.x.press()
        tst.a.press()
        tst.l.press()
        tst.r.press()

        self.assertEqual(str(tst), "|rP|   -4,    8,lr|UDLRsSYBXAlr|")

    def test_fromMnemonic(self):
        # the general premise for this test is that if I use the default
        # symbols, then the mnemonic I give it should match repr(self) after.
        #
        # this may be a faulty premise.
        tst = controller.SnesPreset_MarioPaint()

        m1 = "|rP|   -4,    8,lr|UDLRsSYBXAlr|"
        tst.fromMnemonic(m1)
        self.assertEqual(str(tst), m1)

        m2 = "|.P|    0,    0,l.|UD.Rs.YB.Al.|"
        tst.fromMnemonic(m2)
        self.assertEqual(str(tst), m2)

        m3 = "|..|    0,    0,..|............|"
        tst.fromMnemonic(m3)
        self.assertEqual(str(tst), m3)