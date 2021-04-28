import unittest

import tasstuff.any.bizhawk.history as history

class TestPianoRollEntry(unittest.TestCase):
    def test_constructor_default(self):
        tst = history.PianoRollEntry()
        
        self.assertEqual(tst.input, "")
        self.assertEqual(tst.frame, -1)

    def test_constructor_args(self):
        tst = history.PianoRollEntry(input="test input", frame=42)

        self.assertEqual(tst.input, "test input")
        self.assertEqual(tst.frame, 42)