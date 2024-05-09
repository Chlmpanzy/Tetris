#########################################
# Programmer: Mrs.G
# Date: 7/05/2024
# File Name: tetrisClasses1.py
# Description: These classes are templates for writing a Tetris game.
#########################################
import pygame

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
figures   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
###################################################################
# 1. draw a white frame around the block
###################################################################

    def moveLeft(self):                
        self.col = self.col - 1    
        
    def moveRight(self):
########################################################################
# 2. move the block to the right and remove the pass
########################################################################        
        pass

    def moveDown(self):
        self.row = self.row + 1
########################################################################
# 3. move the block down and remove the pass
########################################################################   
        pass

    def moveUp(self):
#######################################################################
# 4. move the block up and remove the pass
#######################################################################
        pass
#---------------------------------------#
class Shape(object):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
        auxiliary data:
            blocksXoffset - list of horizontal offsets for each block, in reference to the anchor block
            blocksYoffset - list of vertical offsets for each block, in reference to the anchor block
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col         
        self.row = row
        self.clr = clr    
        self.rot = 1
        self.blocks = [Block()]*4        
        self.blocksXoffset = [-1, 0, 0, 1] 
        self.blocksYoffset = [-1,-1, 0, 0] 
        self.rotate()
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]
    
    def rotate(self):
        """ offsets are assigned starting from the farthest block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            blocksXoffset = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]]
            blocksYoffset = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]]        
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            blocksXoffset = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]]
            blocksYoffset = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]]
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            blocksXoffset = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]]
            blocksYoffset = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]]            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
#########################################################################################
# 5. fix the offsets for the L-shape below:
#########################################################################################                         
            blocksXoffset = [[-1, 1, 1,-1], [-1, 1, 1,-1], [-1, 1, 1,-1], [-1, 1, 1,-1]]
            blocksYoffset = [[-1,-1, 1, 1], [-1,-1, 1, 1], [-1,-1, 1, 1], [-1,-1, 1, 1]]
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            blocksXoffset = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]]
            blocksYoffset = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]]            
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            blocksXoffset = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]]
            blocksYoffset = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]]
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            blocksXoffset = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]]
            blocksYoffset = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]]
        self.blocksXoffset = blocksXoffset[self.rot]
        self.blocksYoffset = blocksYoffset[self.rot]
        self.update()
        
    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def moveLeft(self):
        self.col=self.col-1             
        self.update()
        
    def moveRight(self):               
########################################################################
# 6. move the shape to the right
########################################################################                   
        self.update()
        
    def moveDown(self):                
########################################################################
# 7. move the shape down
########################################################################            
        self.update()
        
    def moveUp(self):                  
########################################################################
# 8. move the shape up
########################################################################                   
        self.update()
            
    def update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self.blocksXoffset[i]
            blockROW = self.row+self.blocksYoffset[i]
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)
                                      

