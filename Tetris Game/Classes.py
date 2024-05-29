import pygame
from random import randint
pygame.init()
BLACK = (0, 0, 0)
GRAY = (72, 72, 72)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (91,170,91)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
CYAN = (0, 183, 235)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
COLOURS = [BLACK, RED, GREEN, BLUE, ORANGE, CYAN, MAGENTA, YELLOW, GRAY]
colours = [
    None,
    "red1.bmp","green2.bmp", "blue3.bmp", "orange4.bmp",
    "cyan5.bmp" , "magenta6.bmp", "yellow7.bmp", "shadow.jpeg"
]
HEIGHT = 600
HALFHEIGHT = 300
WIDTH = 600
HALFWIDTH = 300
CLRNames = [
    'black', 'red', 'green', 'blue', 'orange', 'cyan', 'magenta', 'yellow',
    'white'
]
figures = [None, 'Z', 'S', 'J', 'L', 'I', 'T', 'O', None]

COLUMNS = 10
ROWS = 24
LEFT = 21
TOP = 9
MIDDLE = LEFT + COLUMNS // 2
RIGHT = LEFT + COLUMNS
BOTTOM = TOP + ROWS
GRIDSIZE = 16
FLOOR = TOP + ROWS  #

lineSound = pygame.mixer.Sound("clearline (2).wav")
lineSound.set_volume(10)
finishedLine = False

class Block(object):
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """

    def __init__(self, col=1, row=1, clr=1, shadow=False):
        self.col = col
        self.row = row
        self.clr = clr
        self.shadow = shadow
        self.image = pygame.image.load(colours[self.clr])
        if self.shadow:
            self.image = pygame.image.load(colours[-1]) #if it's a shadow, update colour/image
        self.image = pygame.transform.scale(self.image,(GRIDSIZE,GRIDSIZE))

        

    def __str__(self):
        return '(' + str(self.col) + ',' + str(
            self.row) + ') ' + CLRNames[self.clr]

    def draw(self, surface, gridsize=20):
        '''
        (Block, surface, int) -> None
        Function draws blocks on given surface
        '''
        x = self.col * gridsize
        y = self.row * gridsize


        surface.blit(self.image, (x,y))
  
    def __eq__(self, other):
        '''
        (Block, Block) -> bool
        return wether blocks are equal
        '''
        if self.col == other.col and self.row == other.row:
            return True
        return False

    def moveUp(self):
        '''
        (Block) -> None
        Function moves block up
        '''
        self.row = self.row - 1

    def moveDown(self):
        '''
        (Block) -> None
        Function moves block down
        '''
        self.row = self.row + 1

    def moveLeft(self):
        '''
        (Block) -> None
        Function moves block left
        '''
        self.col = self.col - 1

    def moveRight(self):
        '''
        (Block) -> None
        Function moves block right
        '''
        self.col = self.col + 1


#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """

    def __init__(self, col=1, row=1, blocksNo=1, shadow=False):
        self.col = col
        self.row = row
        self.clr = -1
        self.shadow = shadow
        self.blocks = [Block(shadow = self.shadow)] * blocksNo
        self._colOffsets = [0] * blocksNo
        self._rowOffsets = [0] * blocksNo

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col + self._colOffsets[i]
            blockROW = self.row + self._rowOffsets[i]
            blockCLR = self.clr
            self.blocks[i] = Block(blockCOL, blockROW, blockCLR, shadow=self.shadow)

    def draw(self, surface, gridsize):
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other):
        '''
        (Cluster, Cluster) -> bool
        Return wether clusters collide
        '''
        for i in self.blocks:
            for j in other.blocks:
                if i == j:
                    return True
        return False

    def append(self, other):
        """ 
        (Cluster, Cluster) -> None
        Append all blocks from another cluster to this one.
        """
        for i in other.blocks:
            self.blocks.append(i)


#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """

    def __init__(self, col=0, row=0, blocksNo=0):
        Cluster.__init__(self, col, row, blocksNo)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print(block)

    def findFullRows(self, top, lastRow, columns):
        '''
        (Obstacles, int, int, int) -> list
        Function returns all rows that are full
        '''
        fullRows = []
        rows = []
        for block in self.blocks:
            rows.append(block.row)
        for row in range(TOP, BOTTOM):
            if rows.count(row) == columns:
                fullRows.append(row)
        return fullRows

    def removeFullRows(self, fullRows):
        '''
        (Obstacles, list) -> None
        Funciton removes full rows from the obstacles
        '''
        for row in fullRows:
            for i in reversed(range(len(self.blocks))):
                if self.blocks[i].row == row:
                    self.blocks.pop(i)
                elif self.blocks[i].row < row:
                    self.blocks[i].moveDown()
        
        


#---------------------------------------#
class Shape(Cluster):
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """

    def __init__(self, col=1, row=1, clr=1, shadow = False):
        self.shadow = shadow
        Cluster.__init__(self, col, row, 4, self.shadow)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1]
        self._rowOffsets = [-1, -1, 0, 0]
        self._rotate()

    def __str__(self):
        return figures[self.clr] + ' (' + str(self.col) + ',' + str(
            self.row) + ') ' + CLRNames[self.clr]

    def _rotate(self):
        '''
        (Shape) -> None
        offsets are assigned starting from the farthest (most distant) block in reference to the anchor block, function rotates the shape '''
        if self.clr == 1:  #           (default rotation)
            #   o             o o                o
            # o x               x o            x o          o x
            # o                                o              o o
            _colOffsets = [[-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0],
                           [1, 0, 0, -1]]
            _rowOffsets = [[1, 0, 0, -1], [-1, -1, 0, 0], [-1, 0, 0, 1],
                           [1, 1, 0, 0]]
        elif self.clr == 2:  #
            # o                 o o           o
            # o x             o x             x o             x o
            #   o                               o           o o
            _colOffsets = [[-1, -1, 0, 0], [1, 0, 0, -1], [1, 1, 0, 0],
                           [-1, 0, 0, 1]]
            _rowOffsets = [[-1, 0, 0, 1], [-1, -1, 0, 0], [1, 0, 0, -1],
                           [1, 1, 0, 0]]
        elif self.clr == 3:  #
            #   o             o                o o
            #   x             o x o            x           o x o
            # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0],
                           [1, 1, 0, -1]]
            _rowOffsets = [[1, 1, 0, -1], [-1, 0, 0, 0], [-1, -1, 0, 1],
                           [1, 0, 0, 0]]
        elif self.clr == 4:  #
            # o o                o             o
            #   x            o x o             x           o x o
            #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [-1, 1, 0, 1], [0, 0, 0, 1],
                           [-1, -1, 0, 1]]
            _rowOffsets = [[-1, -1, 0, 1], [0, 0, 0, -1], [-1, 1, 0, 1],
                           [1, 0, 0, 0]]
        elif self.clr == 5:  #   o                              o
            #   o                              x
            #   x            o x o o           o          o o x o
            #   o                              o
            _colOffsets = [[0, 0, 0, 0], [2, 1, 0, -1], [0, 0, 0, 0],
                           [-2, -1, 0, 1]]
            _rowOffsets = [[-2, -1, 0, 1], [0, 0, 0, 0], [2, 1, 0, -1],
                           [0, 0, 0, 0]]
        elif self.clr == 6:  #
            #   o              o                o
            # o x            o x o              x o         o x o
            #   o                               o             o
            _colOffsets = [[0, -1, 0, 0], [-1, 0, 0, 1], [0, 1, 0, 0],
                           [1, 0, 0, -1]]
            _rowOffsets = [[1, 0, 0, -1], [0, -1, 0, 0], [-1, 0, 0, 1],
                           [0, 1, 0, 0]]
        else:  #
            # o o            o o               o o          o o
            # o x            o x               o x          o x
            #
            _colOffsets = [[-1, -1, 0, 0], [-1, -1, 0, 0], [-1, -1, 0, 0],
                           [-1, -1, 0, 0]]
            _rowOffsets = [[0, -1, 0, -1], [0, -1, 0, -1], [0, -1, 0, -1],
                           [0, -1, 0, -1]]
        self._colOffsets = _colOffsets[self._rot]
        self._rowOffsets = _rowOffsets[self._rot]
        self._update()

    def moveLeft(self):
        '''
        (Shape) -> None
        Function moves Shape left
        '''
        self.col = self.col - 1
        self._update()

    def moveRight(self):
        '''
        (Shape) -> None
        Function moves Shape right
        '''
        self.col = self.col + 1
        self._update()

    def moveDown(self):
        '''
        (Shape) -> None
        Function moves Shape down
        '''
        self.row = self.row + 1
        self._update()

    def moveUp(self):
        '''
        (Shape) -> None
        Function moves Shape up
        '''
        self.row = self.row - 1
        self._update()

    def rotateClkwise(self):
        '''
        (Shape) -> None
        Function rotates Shape clockwise
        '''
        self._rot = (self._rot + 1) % 4
        self._rotate()

    def rotateCntclkwise(self):
        '''
        (Shape) -> None
        Function roates Shape counterclockwise
        '''
        self._rot = (self._rot - 1) % 4
        self._rotate()

    def findBottom(self, obst, bottom):
        '''
        (Shape, Obstacle, Floor) -> int
        Function find the last row where the shape can be placed
        '''
        while not (self.collides(bottom) or self.collides(obst)):
            self.moveDown()
        self.moveUp()
        return self.row

class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """

    def __init__(self, col=1, row=1, blocksNo=1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i
        self._update()

class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """

    def __init__(self, col=1, row=1, blocksNo=1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i
        self._update()
        

class game(): #holds all varibales and allows for them to be easily reset when hitting "play again"
    def __init__(self):
        self.shapeNo = self.oldShape = randint(1, 7)
        self.tetra = Shape(MIDDLE - 1, TOP, self.shapeNo)
        self.shadow = Shape(MIDDLE - 1, TOP, self.shapeNo, shadow=True)
        self.obst = Obstacles(LEFT, BOTTOM - 1)
        self.nextShapeNo = randint(1, 7)
        self.nextShape = Shape(LEFT-16, TOP+7, self.nextShapeNo)
        self.holdShapeNo = self.points = self.recentPoints = 0
        self.holdShape = Shape(LEFT - 16, TOP+12, 8)
        self.counter = self.time = 0.0
        self.level = 1
        self.swap = self.stored = self.starting = self.pause = self.gameLost = False
        
        self.bottom = Floor(LEFT, BOTTOM-3, COLUMNS)
        self.leftWall = Wall(LEFT - 1, TOP-2, ROWS)
        self.rightWall = Wall(RIGHT, TOP-2, ROWS)
        self.top = Floor(LEFT, TOP-2, COLUMNS)
        
        self.bgImage = pygame.image.load("dswallpaper(4).jpeg")
        self.bg = pygame.transform.scale(self.bgImage,(WIDTH,HEIGHT))
        self.introBgImage = pygame.image.load("dsintro.jpeg")
        self.introBg = pygame.transform.scale(self.introBgImage,(WIDTH,HEIGHT))
        self.pauseImg = pygame.image.load("pausebutton.png")
        self.pauseImg = pygame.transform.scale(self.pauseImg,(GRIDSIZE+15,GRIDSIZE+15))

        self.soundVolume = 0.4
        pygame.mixer.music.load("dsMiiMaker.wav")
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(loops = -1)
        self.levelSound = pygame.mixer.Sound("clear_level.wav")
        self.levelSound.set_volume(self.soundVolume)
        self.rotSound = pygame.mixer.Sound("block-rotate.wav")
        self.rotSound.set_volume(self.soundVolume)
        self.lineSound = pygame.mixer.Sound("clearline (2).wav")
        lineSound.set_volume(0.7)
        self.dropSound = pygame.mixer.Sound("land.wav")
        self.dropSound.set_volume(self.soundVolume)
        self.overSound = pygame.mixer.Sound("gameover.wav")
        self.overSound.set_volume(self.soundVolume)
        self.swapSound = pygame.mixer.Sound("swap.wav")
        self.swapSound.set_volume(self.soundVolume)
        self.tetrisSound = pygame.mixer.Sound("line.wav")
        self.tetrisSound.set_volume(self.soundVolume)

        #fonts
        self.fonts = {"Big":pygame.font.SysFont("Ariel Black",40),
                "Small":pygame.font.SysFont("Ariel Black",24),
                "Medium":pygame.font.SysFont("Ariel Black",30),
                "Medium2":pygame.font.SysFont("Ariel Black",33),
                "Title":pygame.font.SysFont("Ariel Black",50)
                     }
    def reset(self):
        '''
        (game) -> None
        Function resets the game
        '''
        self.shapeNo = self.oldShape = randint(1, 7)
        self.tetra = Shape(MIDDLE - 1, TOP, self.shapeNo)
        self.shadow = Shape(MIDDLE - 1, TOP, self.shapeNo, shadow=True)
        self.obst.blocks.clear()
        self.nextShapeNo = randint(1, 7)
        self.nextShape = Shape(LEFT-16, TOP+7, self.nextShapeNo)
        self.holdShapeN = self.points = self.recentPoints = 0
        self.holdShape = Shape(LEFT - 16, TOP+12, 8)
        self.counter = self.time = 0.0
        self.swap = self.stored = self.starting = self.pause = self.gameLost = False