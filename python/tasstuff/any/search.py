# constants
FLAG_TARGET  = "flag.target"
FLAG_CHECKED = "flag.checked"

# "and all the rest"
class Node():
    """
    A single location in a search graph
    """
    def __init__(self):
        self.flags     = []
        self.neighbors = []

class Vertex():
    """
    A single connection in a search graph
    """
    def __init__(self, left, right, cost=1.0):
        """Creates a vertex.

        "Left" and "right" are arbitrary names here. They don't indicate
        anything meaningful, they just give us a consistent way to tell one Node
        from the other in a vertex.

        Args:
            left (Node):
                One of the two Nodes to connect. Defaults to None.
            right (Node):
                One of the two Nodes to connect. Defaults to None.
            cost (float, optional):
                How much it "costs" to traverse this vertex. Typically this is
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
            raise ValueError("No match for start in vertex!")
        
        return end, self.cost

class Graph():
    # very barebones graph
    def __init__(self):
        self.contents = []

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

class Graph2D():
    """
    A basic search graph.
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
        self.contents = []
        
        # build the basic graph first
        for x in range(width):
            xSwp = []
            for y in range(height):
                xSwp.append(Node())
            self.contents.append(xSwp)
        
        for x in range(width):
            for y in range(height):
                self.contents[x][y].x = x
                self.contents[x][y].y = y
        
        for x in range(1, width):
            for y in range(height):
                self.contents[x][y].west = self.contents[x-1][y]
        
        for x in range(width-1):
            for y in range(height):
                self.contents[x][y].east = self.contents[x+1][y]
                
        for y in range(1, height):
            for x in range(width):
                self.contents[x][y].north = self.contents[x][y-1]
                
        for y in range(height - 1):
            for x in range(width):
                self.contents[x][y].south = self.contents[x][y+1]
    
    def resetSearch(self):
        for column in self.contents:
            for cell in column:
                cell.checked = False
    
    def findClosestTargetTo(self, x, y, unsetTarget=True):
        self.resetSearch()
    
        searchList = [self.contents[int(x)][int(y)]]
        found    = False
        retX     = 0
        retY     = 0
        
        continueSearching = True
        
        #  the actual search over the mesh
        while (continueSearching):
            # get the first node off the searchlist, check it.
            swp = searchList.pop(0)
            
            if (not swp.checked):
                swp.checked = True
                
                if (swp.target):
                    # found a target
                    found = True
                    retX  = swp.x
                    retY  = swp.y
                    
                    if (unsetTarget):
                        swp.target = False
                else:
                    # didn't find a target
                    # no issue, just add the neighbors to the search list
                    # the order they're added actually does matter a little
                    # slightly influences the direction we're more likely to
                    # move in which accrues more and more over long distances
                    if ((swp.north is not None) and (not swp.north.checked)):
                        searchList.append(swp.north)
                    if ((swp.west is not None) and (not swp.west.checked)):
                        searchList.append(swp.west)
                    if ((swp.east is not None) and (not swp.east.checked)):
                        searchList.append(swp.east)
                    if ((swp.south is not None) and (not swp.south.checked)):
                        searchList.append(swp.south)
            
            # loop halt conditions
            if (found):
                continueSearching = False
            elif (0 == len(searchList)):
                continueSearching = False
            else:
                continueSearching = True
        
        # return
        return (found, retX, retY)