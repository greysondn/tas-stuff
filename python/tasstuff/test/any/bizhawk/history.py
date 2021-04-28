import unittest

import tasstuff.any.bizhawk.history as history

class Test_PianoRollEntry(unittest.TestCase):
    def test_constructor_default(self):
        tst = history.PianoRollEntry()
        
        self.assertEqual(tst.input, "")
        self.assertEqual(tst.frame, -1)

    def test_constructor_args(self):
        tst = history.PianoRollEntry(inpt="test input", frame=42)

        self.assertEqual(tst.input, "test input")
        self.assertEqual(tst.frame, 42)

class Test_PianoRoll(unittest.TestCase):
    def test_constructor_default(self):
        tst = history.PianoRoll()
        
        self.assertEqual(len(tst.frames), 0)
        self.assertEqual(tst.currentFrame, 0)
    
    def test_addFrame(self):
        tst = history.PianoRoll()

        tst.addFrame("|test|input|here|")

        self.assertEqual(len(tst.frames), 1)
        self.assertEqual(tst.currentFrame, 1)
        self.assertEqual(tst.frames[0].input, "|test|input|here|")