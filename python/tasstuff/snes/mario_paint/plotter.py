import math
import tasstuff.snes.mario_paint.constants as mp

from PIL import Image
from tasstuff.any.search import Graph
from tasstuff.any.search import Graph2D
from tasstuff.any.search import Node2D
from tasstuff.any.search import Edge

# define edges for Mario Paint
class MPaintEdge(Edge):
    def __init__(self, left, right):
        # parent
        super().__init__(left, right)

# define a node for Mario Paint
class MPaintNode(Node2D):
    def __init__(self):
        # parent
        super().__init__(MPaintEdge)

        # which screen/dialogue/etc this node is from
        self.screen = "UNSET"

# define a graph for Mario Paint.
class MPaintGraph(Graph):
    def __init__(self):
        # parent
        super().__init__()

        # the individual screens
        # for now, I'm ignoring the offscreen portion.




# My column width is set at 80, if you'd like to display this without wrapping.
# ~greysondn
class Plotter:
    def __init__(self):
        # coordinates
        self.x = 0
        self.y = 0

        # offsets
        # only used when plotting
        # from a source image
        self.offsetX = 0
        self.offsetY = 0

        # whether the pen is currently in contact with the paper
        self.down = False
        
        # whether the right mouse is currently down
        self.rightdown = False
        
        # a buffer pool for instructions to output
        self.buffer = []
        
        # how deep our terminal's scrollback is, for max output length.
        # my windows CMD seems to go to about 8000. YMMV.
        self.scrollback = 5000

    # helper, set offsets with one function
    def setOffsets(self, x, y):
        self.offsetX = int(x)
        self.offsetY = int(y)

    # helper, clamp value into range
    def clamp(self, value, rMin, rMax):
        ret = value
        
        if (ret > rMax):
            ret = rMax
            
        if (ret < rMin):
            ret = rMin
        
        return ret

    # helper - generate the max delta possible this frame for
    # the given data
    def getMaxDelta(self, current, target):
        # It's about what you'd expect
        ret      = 0
        distance = math.sqrt(pow((current - target), 2))
        
        if (0 == distance):
            # we're already there!
            ret = 0
        else:
            # oh, well, now we can do more interesting things
            if (distance >= 10):
                # 10 is the maximum meaningful speed anyway
                ret = 10
            else:
                # by rule, distance and speed should match here
                ret = distance
        
            # check the sign!
            if (target < current):
                ret = ret * -1
                
        return ret

    # change internal coordinates to the ones given
    def jump(self, newX, newY):
        # clamp those, don't trust anyone!
        targetX = self.clamp(newX, mp.SCREEN_MIN_X, mp.SCREEN_MAX_X)
        targetY = self.clamp(newY, mp.SCREEN_MIN_Y, mp.SCREEN_MAX_Y)
        
        # right, now change them
        self.x = targetX
        self.y = targetY

    # drop pen
    def penDown(self):
         self.down = True

    # lift pen
    def penUp(self):
        self.down = False

    # right up and down
    def rightUp(self):
        self.rightdown = False
    
    def rightDown(self):
        self.rightdown = True

    # move relative to current position
    def plotRelative(self, xDelta, yDelta):
        # Okay. If we just convert those to destinations, we can
        # just use the absolute function instead.
        targetX = self.x + xDelta
        targetY = self.y + yDelta
    
        # now we just hand that to the other function
        self.plotAbsolute(targetX, targetY)
    
    # move to the specified screen coordinates as quickly as possible
    def plotAbsolute(self, tarX, tarY):
        # clamp our targets
        targetX = self.clamp(tarX, mp.SCREEN_MIN_X, mp.SCREEN_MAX_X)
        targetY = self.clamp(tarY, mp.SCREEN_MIN_Y, mp.SCREEN_MAX_Y)
        
        # Great! Now we just need to buffer instructions until we
        # reach our targets!
        keepMoving = True
        
        while(keepMoving):
            # first, invalidate keep moving
            keepMoving = False
            
            # now, instruction X and Y need scoped, sort of
            instX = 0
            instY = 0
            
            # X there yet?
            if (self.x != targetX):
                keepMoving = True
                instX = self.getMaxDelta(self.x, targetX)
            
            # Y there yet?
            if (self.y != targetY):
                keepMoving = True
                instY = self.getMaxDelta(self.y, targetY)
            
            # we only need to output if we need to keep moving.
            if (keepMoving):
                self.bufferInstruction(instX, instY)
                self.x = self.x + instX
                self.y = self.y + instY
                
        self.outputBuffer(False)

    # wait some number of frames.
    def wait(self, frames):
        for i in range(frames):                # pylint: disable=unused-variable
            self.bufferInstruction(0, 0)
    
    # click the lmb for 7 frames, then release
    def click(self):
        self.penUp()
        self.wait(1)
        self.penDown()
        self.wait(7)
        self.penUp()
        self.wait(1)
    
    # click the rmb for 7 frames, then release
    def rightclick(self):
        self.rightUp()
        self.wait(1)
        self.rightDown()
        self.wait(7)
        self.rightUp()
        self.wait(1)
    
    def bufferInstruction(self, x, y):
        # for now, instructions are straight output
        # later, a buffer might go here to prevent
        # command prompt flooding
        out = ""
        
        # console buttons
        out = out + "|..|"
        
        # X delta
        out = out + str(int(x)).rjust(5, " ") + ","
        
        # Y delta
        out = out + str(int(y)).rjust(5, " ") + ","
        
        # left mouse
        if (self.down):
            out = out + "l"
        else:
            out = out + "."
        
        # right mouse
        if (self.rightdown):
            out = out + "r"
        else:
            out = out + "."
            
        # controller in port 2
        out = out + "|............|"
        
        # add to buffer
        self.buffer.append(out)
        
        # do the buffer output stuff
        self.outputBuffer(False)

    def outputBuffer(self, force):
        doOutput = False
        
        # yeppers
        if (len(self.buffer) >= self.scrollback):
            doOutput = True
        elif (force):
            doOutput = True
        
        if (doOutput):
            # reverse it
            self.buffer.reverse()
            
            print("")
            
            # pop the items off and print them
            # before discarding
            while(len(self.buffer) > 0):
                print(self.buffer.pop())
            
            # burn some time
            print("")
            #pylint: disable=unused-variable
            ignored = input("< Input enter to continue script. >")
    
    # draws a 1 bit mask's black pixels to the screen
    # assumes quite a lot I suppose - pen is already
    # selected, pen is a single pixel at (9, 9)
    # stamp, etc.
    def mask(self, path):
        # open image using PILLOW
        im = Image.open(path)
        
        # make sure it's RGB
        im = im.convert("RGB")
        
        # define black as the value of its RGB triple for comparison later
        black = (0, 0, 0)
        
        # prep pen
        if (self.down):
            # need to lift and wait so we know input will be read
            self.penUp()
            self.wait(10)

        # prep search grid
        width  = im.size[0]
        height = im.size[1]
        
        sGrid = Graph2D(width, height)
        
        # have to set targets in the grid
        for x in range(width):
            for y in range(height):
                px = im.getpixel((x, y))
                if (black == px):
                    sGrid.contents[x][y].target = True

        # we need to track where we just were
        lastX = self.x
        lastY = self.y
        
        nxtExists = True
        
        while (nxtExists):
            # find our next target
            nxtExists, x, y = sGrid.findClosestTargetTo(lastX, lastY)
        
            # and so we go ahead and do this, I suppose.
            if (nxtExists):
                # draw on the plotter
                if (self.down):
                    # determine adjacency
                    # defined here as "able to be drawn without lifting pen"
                    # now including if moving the pen would leave undrawn ones
                    # between also - remarkably - undrawn
                    adjacent = False
                    xDist    = int(abs(x - lastX))
                    yDist    = int(abs(y - lastY))
                            
                    # within one jump rules
                    if ((xDist <= 10) and (yDist == 0)):
                        # horizontal
                        adjacent = True
                    elif ((xDist == 0) and (yDist <= 10)):
                        # vertical
                        adjacent = True
                    elif ((xDist <= 10) and (yDist <= 10)):
                        # diagonal
                        adjacent = True
                    else:
                        # not adjacent, is it?
                        adjacent = False
                            
                    # anyway, if it's adjacent, we just move to it
                    if (adjacent):
                        self.plotAbsolute(x + self.offsetX, y + self.offsetY)
                    else:
                        # if it's not, what a pain.
                        self.penUp()
                        self.wait(1)
                        self.plotAbsolute(x + self.offsetX, y + self.offsetY)
                        self.penDown()
                        self.wait(8)
                else:
                    # not self.down
                    # we'll assume the wait has already happened here
                    self.plotAbsolute(x + self.offsetX, y + self.offsetY)
                    self.wait(1)
                    self.penDown()
                    self.wait(8)
                            
                # and now we just set the last drawn coordinates
                lastX = x
                lastY = y
        
        # just some slight cleanup
        self.penUp()
        
class PlotterREPL:
    # defines a REPL for the plotter so it can be used directly.
    def __init__(self):
        self.plotter = Plotter()
        
    def status(self):
        print("Status:")
        print("x    : " + str(self.plotter.x))
        print("offX : " + str(self.plotter.offsetX))
        print("y    : " + str(self.plotter.y))
        print("offY : " + str(self.plotter.offsetY))
        print("lmb  : " + str(self.plotter.down))
        print("rmb  : " + str(self.plotter.rightdown))
        print("buf  : " + str(len(self.plotter.buffer)))
    
    def run(self):
        # yes
        keepGoing = True
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Welcome to the Mario Paint plotter!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        self.status()
        print("")
        
        
        # main program loop
        while (keepGoing):
        
            # get user input
            userInput = str(input("COM? > ")).lower().strip()
            if("" == userInput):
                userInput = "ERROR"
            uin = userInput.split()
            
            # handle user inputs
            if ("click" == uin[0]):
                self.plotter.click()
            elif ("down" == uin[0]):
                self.plotter.penDown()
            elif ("exit" == uin[0]):
                keepGoing = False
            elif ("help" == uin[0]):
                print("click      - click mouse")
                print("down       - put pen down")
                print("exit       - exit this program")
                print("help       - print basic help text")
                print("mask file - plot black dots in mask")
                print("jump   x y - set internal location to x, y")
                print("move   x y - move pen by x, y")
                print("moveto x y - move pen to x, y")
                print("offset x y - adjust offset for plotting from image")
                print("rightdown  - push right button down")
                print("rightup    - release right button")
                print("status     - give status of pen")
                print("up         - put pen up")
            elif ("jump" == uin[0]):
                self.plotter.jump(int(uin[1]), int(uin[2]))
            elif ("mask" == uin[0]):
                self.plotter.mask(uin[1])
            elif ("move" == uin[0]):
                self.plotter.plotRelative(int(uin[1]), int(uin[2]))
            elif ("moveto" == uin[0]):
                self.plotter.plotAbsolute(int(uin[1]), int(uin[2]))
            elif ("offset" == uin[0]):
                self.plotter.setOffsets(int(uin[1]), int(uin[2]))
            elif ("rightdown" == uin[0]):
                self.plotter.rightDown()
            elif ("rightup" == uin[0]):
                self.plotter.rightUp()
            elif ("status" == uin[0]):
                self.status()
            elif ("up" == uin[0]):
                self.plotter.penUp()
            else:
                print("Not sure what you entered but it's not a command.")
            
            # dump the buffer
            if (len(self.plotter.buffer) > 0):
                self.plotter.outputBuffer(True)
            
            # get ready to cycle
            print("")

# if the name is main, run the repl
if ("__main__" == __name__):
    r = PlotterREPL()
    r.run()