#########################################
# Programmer: Mrs.G
# Date: 7/05/2024
# File Name: tetrisTemplate1.py
# Description: This program is a template for a Tetris game.
#########################################
from tetrisClasses1 import *
from random import randint
import pygame
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw():               
    screen.fill(BLACK)
    drawGrid()
    tetra.draw(screen, GRIDSIZE)
##########################################################################
# 9. remove the line below, after you have added white frames to the blocks
##########################################################################
    pygame.draw.rect(screen, WHITE, (tetra.col*GRIDSIZE,tetra.row*GRIDSIZE,GRIDSIZE,GRIDSIZE), 1)    
    pygame.display.update() 


def drawGrid():
    """ Draw horisontal and vertical lines on the entire game window.
        Space between the lines is GRIDSIZE.
    """
    for x in range(0,WIDTH,GRIDSIZE):
        pygame.draw.line(screen,WHITE, (x,0),(x,HEIGHT),1)

##################################################################################
# 10. Add here your code that draws the grid and remove the pass ( use for loops)
#     Hint for drawing a line:  pygame.draw.line(surface, color, (start_x,start_y),(end_x,end_y))
#
# 11. Draw a grid only on the playing field ( 22rows/10 col).
#########################################################################
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)      
tetra = Shape(1,1,shapeNo)
inPlay = True                                         

while inPlay:               
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetra.rot = (tetra.rot + 1)%4  
                tetra.rotate()
            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
            if event.key == pygame.K_DOWN:
                tetra.moveDown()                
            if event.key == pygame.K_SPACE:
###################################################################
# 12. Replace the code below with a single line, which changes the shape/clr 
# use remainder operator, as shown for rotation change with K_UP
###################################################################
                tetra.clr = tetra.clr + 1
                if tetra.clr > 7:
                    tetra.clr = 1
                # after chaging the shape/clr the tetra must be rotated and updated
                tetra.rotate()               

    # update the screen     
    redraw()
    pygame.time.delay(30)
    
pygame.quit()
    
    
