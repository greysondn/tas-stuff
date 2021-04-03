class Node2D():
    """
    A single location in the search graph.
    """    
    def __init__(self):
        self.x       = -1
        self.y       = -1
        self.target  = False
        self.checked = False
        self.north   = None
        self.east    = None
        self.west    = None
        self.south   = None

class Graph2D():
    """
    A basic search graph.
    """    
    def __init__(self, width, height):
        self.contents = []
        
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