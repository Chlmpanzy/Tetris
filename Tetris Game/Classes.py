import pygame

BLACK = (0, 0, 0)
GRAY = (72, 72, 72)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
CYAN = (0, 183, 235)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
COLOURS = [BLACK, RED, GREEN, BLUE, ORANGE, CYAN, MAGENTA, YELLOW, GRAY]
CLRNames = [
    'black', 'red', 'green', 'blue', 'orange', 'cyan', 'magenta', 'yellow',
    'white'
]
figures = [None, 'Z', 'S', 'J', 'L', 'I', 'T', 'O', None]

COLUMNS = 10
ROWS = 22
LEFT = 9
TOP = 1
MIDDLE = LEFT + COLUMNS // 2
RIGHT = LEFT + COLUMNS
BOTTOM = TOP + ROWS

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

    def __str__(self):
        return '(' + str(self.col) + ',' + str(
            self.row) + ') ' + CLRNames[self.clr]

    def draw(self, surface, gridsize=20):
        x = self.col * gridsize
        y = self.row * gridsize

        CLR = COLOURS[-1] if self.shadow else COLOURS[self.clr]
        
        pygame.draw.rect(surface, CLR, (x, y, gridsize, gridsize), 0)
        pygame.draw.rect(surface, WHITE, (x, y, gridsize + 1, gridsize + 1), 1)
        
    def __eq__(self, other):
        if self.col == other.col and self.row == other.row:
            return True
        return False

    def moveUp(self):
        self.row = self.row - 1

    def moveDown(self):
        self.row = self.row + 1

    def moveLeft(self):
        self.col = self.col - 1

    def moveRight(self):
        self.col = self.col + 1


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
        self.clr = 0
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
        for i in self.blocks:
            for j in other.blocks:
                if i == j:
                    return True
        return False

    def append(self, other):
        for i in other.blocks:
            self.blocks.append(i)

class Obstacles(Cluster):

    def __init__(self, col=0, row=0, blocksNo=0):
        Cluster.__init__(self, col, row, blocksNo)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print(block)

    def findFullRows(self, top, lastRow, columns):
        fullRows = []
        rows = []
        for block in self.blocks:
            rows.append(block.row)
        for row in range(TOP, BOTTOM):
            if rows.count(row) >= columns:
                fullRows.append(row)
        return fullRows

    def removeFullRows(self, fullRows):

        for row in fullRows:
            for i in reversed(range(len(self.blocks))):
                if self.blocks[i].row == row:
                    self.blocks.pop(i)
                elif self.blocks[i].row < row:
                    self.blocks[i].moveDown()


#---------------------------------------#
class Shape(Cluster):

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
        self.col = self.col - 1
        self._update()

    def moveRight(self):
        self.col = self.col + 1
        self._update()

    def moveDown(self):
        self.row = self.row + 1
        self._update()

    def moveUp(self):
        self.row = self.row - 1
        self._update()

    def rotateClkwise(self):
        self._rot = (self._rot + 1) % 4
        self._rotate()

    def rotateCntclkwise(self):
        self._rot = (self._rot - 1) % 4
        self._rotate()




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
    