# constants
FLAG_TARGET  = "flag.target"
FLAG_CHECKED = "flag.checked"

# "and all the rest"
class Node():
    """
    A single location in a search graph
    """
    def __init__(self):
        self.flags = []
        self.edges = []
        self.cost  = 0

    def addNeighbor(self, neighbor, cost=1.0, mirror=True):
        swp = Edge(self, neighbor, float(cost))
        self.edges.append(swp)

        if (mirror):
            neighbor.addNeighbor(self, cost, False)
    
    def hasNeighbor(self, neighbor):
        ret = False

        for edge in self.edges:
            if (edge.traverse(self)[0] is neighbor):
                ret = True
        
        return ret

    def getConnectingEdge(self, neighbor):
        ret = None
        
        for edge in self.edges:
            if (edge.traverse(self)[0] is neighbor):
                ret = edge

        return ret
    
    def addFlag(self, flag):
        if (flag not in self.flags):
            self.flags.append(flag)
    
    def hasFlag(self, flag):
        ret = False

        if (flag in self.flags):
            ret = True

        return ret

    def removeFlag(self, flag):
        if (self.hasFlag(flag)):
            self.flags.remove(flag)

    def resetFlags(self):
        self.flags = []

    
class Edge():
    """
    A single connection in a search graph
    """
    def __init__(self, left, right, cost=1.0):
        """Creates a link between two nodes.

        "Left" and "right" are arbitrary names here. They don't indicate
        anything meaningful, they just give us a consistent way to tell one Node
        from the other in a connection.

        Args:
            left (Node):
                One of the two Nodes to connect. Defaults to None.
            right (Node):
                One of the two Nodes to connect. Defaults to None.
            cost (float, optional):
                How much it "costs" to traverse this link. Typically this is
                the actual distance between nodes, or the resource cost to move
                between them. Defaults to 1.0.
        """
        self.left  = left
        self.right = right
        self.cost  = cost
    
    def traverse(self, start):
        end = None
        
        if (start is self.left):
            end = self.right
        elif (start is self.right):
            end = self.left
        else:
            raise ValueError("No match for start in edge!")
        
        return end, self.cost

class Path():
    # represents a series of nodes that are connected, start to end
    def __init__(self, start):
        self.cost   = 0
        self.start  = start
        self.end    = start
        self.nodes  = [start]
        self.failed = False
    
    def moveto(self, node):
        if (not self.failed):
            if (self.nodes[-1].hasNeighbor(node)):
                # has link to next
                self.cost = self.cost + self.end.getConnectingEdge(node).cost
                self.nodes.append(node)
                self.end  = node
                
            else:
                # does not have link to next
                self.failed = True
        
        return not self.failed

class Graph():
    # very barebones graph
    def __init__(self):
        self.contents = []

    def resetSearch(self):
        for node in self.contents:
            node.removeFlag("___checked")
            node.cost = float("inf")

    def findClosestFlaggedTo(self, flag, node):
        ret = None

        self.resetSearch()

        if (node in self.contents):
            stopSearching = False
            
            node.cost = 0
            toSearch = [node]

            while (not stopSearching):
                    
                # get cheapest from the toSearch stack
                swp = toSearch[0]

                for node in toSearch:
                    if node.cost < swp.cost:
                        swp = node
                
                toSearch.remove(swp)

                if not(swp.hasFlag("___checked")):
                    # peek in on the neighbors
                    for edge in swp.edges:
                        # update costs
                        costGuess = swp.cost + edge.cost
                        nxt = edge.traverse(swp)[0]
                        if (nxt.cost > costGuess):
                            nxt.cost = costGuess
                
                        # add any unchecked neighbors to the search array
                        if (not nxt.hasFlag("___checked")):
                            toSearch.append(nxt)
                    
                    # give swap the checked flag so it won't be checked twice
                    swp.addFlag("___checked")

                # end conditions
                if (swp.hasFlag(flag)):
                    # found a target
                    stopSearching = True
                    ret = swp
                elif (0 == len(toSearch)):
                    # no more connections to search
                    stopSearching = True
                    ret = None

        return ret 

class Node2D(Node):
    """
    A single location in the search graph.
    """
    def __init__(self):
        # parent constructor
        super().__init__()

        # extra properties
        self.x         = -1
        self.y         = -1

class Graph2D(Graph):
    """
    A basic search graph. Has some extension to help with 2 dimensional work.
    """
    def __init__(self, width, height, cardinalNeighbors=True, 
                 diagonalNeighbors=False):
        """Create a simple 2D search graph.

        The operating assumption is that this maps to some kind of 2D grid map -
        tiles, pixels, something like that.

        Args:
            width (uint):
                width in nodes to make the graph
            height (uint):
                height in nodes to make the graph
            cardinalNeighbors (bool, optional):
                Whether to link the north, south, east, and west node to each
                other. Defaults to True.
            diagonalNeighbors (bool, optional):
                Whether to link the northeast, northwest, southeast, and
                southwest nodes to each other. Defaults to False.
        """        
        # parent constructor first
        super().__init__()

        # extra properties related to being a 2d map
        self.width  = width
        self.height = height

        self.grid = [] # the contents laid out in a coordinate grid

        # build the basic graph first
        for x in range(width):
            xSwp = []
            for y in range(height):
                # need to work with the node just a bit as we add it
                nSwp = Node()

                # make node aware of its own position
                nSwp.x = x
                nSwp.y = y

                # add node to row
                xSwp.append(nSwp)

                # add node to base contents
                self.contents.append(nSwp)

            # add row to graph
            self.grid.append(xSwp)

        # connect neighbors
        if (cardinalNeighbors):
            self.connectCardinals()

        if (diagonalNeighbors):
            self.connectDiagonals()

    def connectCardinals(self):
        """
        Connect nodes in this graph to their cardinal neighbors. North, south,
        east, and west.
        """
        for x in range (self.width):
            for y in range (self.height):
                # west
                if (x > 0):
                    self.grid[x][y].addNeighbor(self.grid[x-1][y])
                # north
                if (y > 0):
                    self.grid[x][y].addNeighbor(self.grid[x][y-1])
                # east
                if (x < self.width - 1):
                    self.grid[x][y].addNeighbor(self.grid[x+1][y])
                # south
                if (y < self.height - 1):
                    self.grid[x][y].addNeighbor(self.grid[x][y+1])
    
    def connectDiagonals(self):
        """
        Connect nodes in this graph to their diagonal neighbors. Northeast,
        northwest, southeast, southwest.
        """
        for x in range (self.width):
            for y in range (self.height):
                # northwest
                if ((x > 0) and (y > 0)):
                    self.grid[x][y].addNeighbor(self.grid[x-1][y-1])
                # northeast
                if ((x < self.width - 1) and (y > 0)):
                    self.grid[x][y].addNeighbor(self.grid[x+1][y-1])
                # southwest
                if ((x > 0) and (y < self.height - 1)):
                    self.grid[x][y].addNeighbor(self.grid[x-1][y+1])
                # southeast
                if ((x < self.width - 1) and (y < self.height - 1)):
                    self.grid[x][y].addNeighbor(self.grid[x+1][y+1])