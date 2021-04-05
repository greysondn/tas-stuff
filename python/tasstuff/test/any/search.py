# unit tests for search.py
import unittest

import tasstuff.any.search as search

class test_Node(unittest.TestCase):

    def test_constructor_default(self):
        tst  = search.Node()

        self.assertEqual([], tst.flags)
        self.assertEqual([], tst.edges)

    def test_addNeighbor(self):
        tst = search.Node()

        nxt = search.Node()
        mir = search.Node()

        # no mirror
        tst.addNeighbor(nxt,4.2,False)

        self.assertIs(tst.edges[0].left, tst)
        self.assertIs(tst.edges[0].right, nxt)
        self.assertEquals(tst.edges[0].cost, 4.2)
        self.assertEquals(len(tst.edges), 1)
        self.assertEquals(len(nxt.edges), 0)

        # mirror now
        tst.addNeighbor(mir)

        self.assertIs(tst.edges[1].left, tst)
        self.assertIs(tst.edges[1].right, mir)
        self.assertEquals(tst.edges[1].cost, 1.0)
        self.assertEquals(len(tst.edges), 2)

        self.assertIs(mir.edges[0].left, mir)
        self.assertIs(mir.edges[0].right, tst)
        self.assertEquals(mir.edges[0].cost, 1.0)
        self.assertEquals(len(mir.edges), 1)
    
    def test_hasNeighbor(self):
        tst = search.Node()
        nbr = search.Node()
        nop = search.Node()

        tst.addNeighbor(nbr, 1.0, False)
        
        self.assertTrue(tst.hasNeighbor(nbr))
        self.assertFalse(tst.hasNeighbor(nop))
    
    def test_getConnectingEdge(self):
        tst = search.Node()
        nbr = search.Node()
        nop = search.Node()

        tst.addNeighbor(nbr, 1.0, False)

        shouldBe = tst.edges[0]

        self.assertIs(tst.getConnectingEdge(nbr), shouldBe)
        self.assertIs(tst.getConnectingEdge(nop), None)
    
    def test_addFlag(self):
        tst = search.Node()

        self.assertEquals(len(tst.flags), 0)
        
        tst.addFlag("test")
        self.assertEquals(len(tst.flags), 1)
        self.assertEquals(tst.flags[0], "test")

        tst.addFlag("test")
        self.assertEquals(len(tst.flags), 1)

    def test_hasFlag(self):
        tst = search.Node()

        self.assertFalse(tst.hasFlag("test"))
        tst.addFlag("test")
        self.assertTrue(tst.hasFlag("test"))

    def test_removeFlag(self):
        tst = search.Node()

        tst.addFlag("test")
        tst.removeFlag("test")
        self.assertFalse(tst.hasFlag("test"))

    def test_resetFlags(self):
        tst = search.Node()

        tst.addFlag("test")
        tst.resetFlags()
        self.assertFalse(tst.hasFlag("test"))



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

class test_path(unittest.TestCase):

    def test_constructor_default(self):
        node = search.Node()
        tst  = search.Path(node)

        self.assertEquals(tst.cost, 0)
        self.assertIs(tst.start, node)
        self.assertIs(tst.end, node)
        self.assertEquals(len(tst.nodes), 1)
        self.assertIs(tst.nodes[0], node)
        self.assertFalse(tst.failed)

    def test_moveto(self):
        start = search.Node()
        end   = search.Node()
        nope  = search.Node()

        start.addNeighbor(end, 2.3)

        tst = search.Path(start)

        self.assertTrue(tst.moveto(end))

        self.assertEquals(tst.cost, 2.3)
        self.assertEquals(len(tst.nodes), 2)
        self.assertIs(tst.end, end)
        self.assertIs(tst.start, start)
        self.assertFalse(tst.failed)

        self.assertFalse(tst.moveto(nope))

        self.assertEquals(tst.cost, 2.3)
        self.assertEquals(len(tst.nodes), 2)
        self.assertIs(tst.end, end)
        self.assertIs(tst.start, start)
        self.assertTrue(tst.failed)



class test_Graph(unittest.TestCase):

    def test_constructor_default(self):
        tst = search.Graph()

        self.assertEquals(tst.contents, [])

class test_Node2D(unittest.TestCase):

    def test_constructor_default(self):
        tst = search.Node2D()

        # test parent
        self.assertEqual([], tst.flags)
        self.assertEqual([], tst.edges)

        # test new properties
        self.assertEqual(-1, tst.x)
        self.assertEqual(-1, tst.y)

class testGraph2D(unittest.TestCase):

    def test_constructor_default(self):
        tst = search.Graph2D(3, 3)

        # parent
        self.assertEquals(len(tst.contents), 9)

        # self
        self.assertEquals(tst.width,  3)
        self.assertEquals(tst.height, 3)

        self.assertEquals(len(tst.grid), 3)
        self.assertEquals(len(tst.grid[0]), 3)
        self.assertEquals(len(tst.grid[1]), 3)
        self.assertEquals(len(tst.grid[2]), 3)

        # okay, the connections for link cardinals?
        self.assertTrue(tst.grid[0][0].hasNeighbor(tst.grid[0][1]))
        self.assertTrue(tst.grid[0][0].hasNeighbor(tst.grid[1][0]))

        self.assertTrue(tst.grid[1][0].hasNeighbor(tst.grid[0][0]))
        self.assertTrue(tst.grid[1][0].hasNeighbor(tst.grid[1][1]))
        self.assertTrue(tst.grid[1][0].hasNeighbor(tst.grid[2][0]))

        self.assertTrue(tst.grid[2][0].hasNeighbor(tst.grid[1][0]))
        self.assertTrue(tst.grid[2][0].hasNeighbor(tst.grid[2][1]))

        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[0][1]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[1][0]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[1][2]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[2][1]))
        self.assertFalse(tst.grid[1][1].hasNeighbor(tst.grid[0][0]))
        self.assertFalse(tst.grid[1][1].hasNeighbor(tst.grid[0][2]))
        self.assertFalse(tst.grid[1][1].hasNeighbor(tst.grid[1][1]))
        self.assertFalse(tst.grid[1][1].hasNeighbor(tst.grid[2][0]))
        self.assertFalse(tst.grid[1][1].hasNeighbor(tst.grid[2][2]))
        # I got bored of writing, call me when it breaks.

    def test_constructor_diagonals(self):
        tst = search.Graph2D(3, 3, True, True)

        # we'll just skip straight to the short test for this
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[0][1]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[1][0]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[1][2]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[2][1]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[0][0]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[0][2]))
        self.assertFalse(tst.grid[1][1].hasNeighbor(tst.grid[1][1]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[2][0]))
        self.assertTrue(tst.grid[1][1].hasNeighbor(tst.grid[2][2]))

    def test_constructor_sizes(self):
        tst=search.Graph2D(1,2)

        self.assertEquals(len(tst.grid), 1)
        self.assertEquals(len(tst.grid[0]), 2)
