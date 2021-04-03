# unit tests for search.py
import unittest

import tasstuff.any.search as search

class test_Node(unittest.TestCase):

    def test_constructor_default(self):
        tst  = search.Node()

        self.assertEqual([], tst.flags)
        self.assertEqual([], tst.neighbors)

class test_Vertex(unittest.TestCase):

    def test_constructor_default(self):
        l = search.Node()
        r = search.Node()
        
        tst = search.Vertex(l, r)

        self.assertIs(tst.left, l)
        self.assertIs(tst.right, r)
        self.assertEqual(tst.cost, 1.0)

    def test_constructor_args(self):
        l = search.Node()
        r = search.Node()
        
        tst = search.Vertex(l, r, 1.0)

        self.assertIs(tst.left, l)
        self.assertIs(tst.right, r)
        self.assertEqual(tst.cost, 1.0)
    
    def test_traverse(self):
        # setup.
        l   = search.Node()
        r   = search.Node()
        err = search.Node()

        swp = search.Vertex(l, r, 6.18)

        # left-to-right
        tst = swp.traverse(l)
        self.assertIs(tst[0], r)
        self.assertEqual(tst[1], 6.18)

        # right to left
        tst = swp.traverse(r)
        self.assertIs(tst[0], l)
        self.assertEqual(tst[1], 6.18)

        # error
        self.assertRaises(ValueError, swp.traverse, err)

class test_Graph(unittest.TestCase):

    def test_constructor_default(self):
        tst = search.Graph()

        self.assertEquals(tst.contents, [])