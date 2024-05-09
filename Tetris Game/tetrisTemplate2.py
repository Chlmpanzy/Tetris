###########################################################
# Programmer: Mrs.G
# Date: 7/05/2024
# File Name: tetrisTemplate2.py
# Description: This program is a template for a Tetris game.
############################################################
from tetrisClasses2 import *
from random import randint
import pygame
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT/24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
############################################################
# 1. Adjust your grid location according to these parameters
#    or change the parameters to match your grid location.
############################################################
COLUMNS = 10                            
ROWS = 22                            
LEFT = 9                                
TOP = 1                                 
MIDDLE = LEFT + COLUMNS//2               
RIGHT = LEFT + COLUMNS                  
BOTTOM = TOP + ROWS                      


#---------------------------------------#
#   functions                           #
#--------------------------------------#
def redraw():               
    screen.fill(BLACK)
    tetra.draw(screen, GRIDSIZE)
    bottom.draw(screen, GRIDSIZE)
    ###########################################################
    # 4. Draw the left and right walls using the same draw method
    ###########################################################
    pygame.display.update() 
    
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)
tetra = Shape(1,1,shapeNo)     
##############################################################
# 9. Creates a new tetra at the middle top of your game field.  
##############################################################

bottom = Floor(9,23,COLUMNS)
#############################################################################################
# 3. Ceate the left and right walls (leftWall & rightWall). Use the Wall class and adjust the
#   first two parameters to determine the coordinates of the anchor block
#############################################################################################

inPlay = True                                         

while inPlay:               

    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetra.rot = (tetra.rot + 1)%4     
                tetra.rotate()
######################################################################################################
# 8.  Check for collisions with the walls and floor during rotation and undo it, if a conflict occurs
######################################################################################################

            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
######################################################################################################
# 7.   Use the tetra.collides() method shown below to avoid collisions with the left and right walls
######################################################################################################
            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
            if event.key == pygame.K_DOWN:
                tetra.moveDown()
                
            # temporary change of shape functionality.
            if event.key == pygame.K_SPACE:
                tetra.clr = tetra.clr + 1
                if tetra.clr > 7:
                    tetra.clr = 1
                tetra.rotate()

# update the screen     
    redraw()
    pygame.time.delay(30)
    
pygame.quit()
    
    
