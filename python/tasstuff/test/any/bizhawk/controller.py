import unittest

import tasstuff.any.bizhawk.controller as controller

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