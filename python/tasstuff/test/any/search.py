# unit tests for search.py
import unittest

import tasstuff.any.search as search

class test_Node(unittest.TestCase):

    def test_constructor_default(self):
        tst  = search.Node()

        self.assertEqual([], tst.flags)
        self.assertEqual([], tst.neighbors)

    def test_addNeighbor(self):
        tst = search.Node()

        nxt = search.Node()
        mir = search.Node()

        # no mirror
        tst.addNeighbor(nxt,4.2,False)

        self.assertIs(tst.neighbors[0].left, tst)
        self.assertIs(tst.neighbors[0].right, nxt)
        self.assertEquals(tst.neighbors[0].cost, 4.2)
        self.assertEquals(len(tst.neighbors), 1)
        self.assertEquals(len(nxt.neighbors), 0)

        # mirror now
        tst.addNeighbor(mir)

        self.assertIs(tst.neighbors[1].left, tst)
        self.assertIs(tst.neighbors[1].right, mir)
        self.assertEquals(tst.neighbors[1].cost, 1.0)
        self.assertEquals(len(tst.neighbors), 2)

        self.assertIs(mir.neighbors[0].left, mir)
        self.assertIs(mir.neighbors[0].right, tst)
        self.assertEquals(mir.neighbors[0].cost, 1.0)
        self.assertEquals(len(mir.neighbors), 1)

class test_Edge(unittest.TestCase):

    def test_constructor_default(self):
        l = search.Node()
        r = search.Node()
        
        tst = search.Edge(l, r)

        self.assertIs(tst.left, l)
        self.assertIs(tst.right, r)
        self.assertEqual(tst.cost, 1.0)

    def test_constructor_args(self):
        l = search.Node()
        r = search.Node()
        
        tst = search.Edge(l, r, 1.0)

        self.assertIs(tst.left, l)
        self.assertIs(tst.right, r)
        self.assertEqual(tst.cost, 1.0)
    
    def test_traverse(self):
        # setup.
        l   = search.Node()
        r   = search.Node()
        err = search.Node()

        swp = search.Edge(l, r, 6.18)

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

class test_Node2D(unittest.TestCase):

    def test_constructor_default(self):
        tst = search.Node2D()

        # test parent
        self.assertEqual([], tst.flags)
        self.assertEqual([], tst.neighbors)

        # test new properties
        self.assertEqual(-1, tst.x)
        self.assertEqual(-1, tst.y)