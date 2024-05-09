#########################################
# Programmer: Mrs.G
# Date: 07/05/2024
# File Name: tetrisTemplate3.py
# Description: This program is the third game template for our Tetris game.
#########################################
from tetrisClasses3 import *
from random import randint
import pygame
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (192,192,192)

#---------------------------------------#
COLUMNS = 10                          #
ROWS = 22                                   # 
LEFT = 9                                        # 
RIGHT = LEFT + COLUMNS         # 
MIDDLE = LEFT + COLUMNS//2  #
TOP = 1                                        #
FLOOR = TOP + ROWS             #
#---------------------------------------#

#---------------------------------------#
#   functions                            #
#---------------------------------------#
def redrawScreen():               
    screen.fill(BLACK)
    tetra.draw(screen, GRIDSIZE)
    floor.draw(screen, GRIDSIZE)
    leftWall.draw(screen, GRIDSIZE)
    rightWall.draw(screen, GRIDSIZE)
#####################################################################################################
# 11.  Draw the object obstacles on the screen
#####################################################################################################
    pygame.display.update() 
        
#---------------------------------------#
#   main program                    #
#---------------------------------------#    
shapeNo = randint(1,7)      
tetra = Shape(1,1,shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
#####################################################################################################
# 10.  Create an object obstacles of Obstacles class. Give it two parameters only - LEFT & FLOOR
#####################################################################################################
inPlay = True                                         

while inPlay:               
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
#####################################################################################################
# 7.  Modify the code below, so it calls rotateClkwise() method and it doesn't access _rot private variable
#     and the rotation method. Use the code below in the class template to write the new rotation methods
#####################################################################################################                     
                tetra._rot = (tetra._rot + 1)%4  
                tetra._rotate()
#####################################################################################################
# 8.  Modify the code so it uses rotateCntclkwise() method when collision is detected during rotation
#####################################################################################################
            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
            if event.key == pygame.K_SPACE:
                pass
####################################################################################################
# 12. Remove the space bar action that changes the shape.
#     Replace the code above with code that drops 
#     the shape until it hits the floor or obstacles.
#     HINT: Use a while loop, and the conflict method to stop the movement.
# 13. Remove the DOWN key check. Let the tetra move down freely
#     dedent the command to allign with the for loop at the top.
#     HINT: If the tetra moves very fast you can consider adding a timer: (if timer%5==0) use the clock command
####################################################################################################
            if event.key == pygame.K_DOWN:
                tetra.moveDown()
                if tetra.collides(floor):
                    tetra.moveUp()
#                   obstacles.show()    # print the blocks to visualize the process. Remove it afterwards

##################################################################################
# 14. Add the collisions between the shape and the obstacles in all if statements
#     Once the shape is down, it has to become a part of the obstacle object
#15. Use the append merhod to add the fallen tetra to the obstacle's object
##################################################################################        
                
                    fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS)    # finds the full rows and removes their blocks from the obstacles 
                    print ("full rows: ",fullRows)    # printing the full rows is done to visualize the process remove it afterwards
                    obstacle.removeFullRows(fullRows)
                
###################################################################################
# 16. Generate a new shape in the middle of the screen. Uncomment the 3 lines above 
###################################################################################
     
    redrawScreen()
    pygame.time.delay(30)
    
pygame.quit()
    
    
