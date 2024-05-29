from Classes import *
from random import randint
import pygame

pygame.init()
clock = pygame.time.Clock()
HEIGHT = 600
HALFHEIGHT = 300
WIDTH = 600
HALFWIDTH = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GREY = (192, 192, 192)
PAUSEBLACK = (0,0,0,50)

#---------------------------------------#

game = game()

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def gameOver():
    '''
    () -> None
    This function displays the gameover screen.
    '''
    screen.blit(game.introBg,(0,0))
    gameOverText = game.fonts["Big"].render("You Lost!",1,RED)
    screen.blit(gameOverText,(HALFWIDTH-85, HALFHEIGHT+30))
    pygame.draw.rect(screen, GREEN, (HALFWIDTH+20, HALFHEIGHT+180,HALFWIDTH-50, 100))
    playAgain = game.fonts["Big"].render("Play Again", 1, BLACK)
    screen.blit(playAgain, (HALFWIDTH+70, HALFHEIGHT+215))
    pygame.display.update()
    
def start():
    '''
    () -> None
    This function displays the introduction screen with a start button
    '''
    screen.blit(game.introBg,(0,0))
    pygame.draw.rect(screen, GREEN, (HALFWIDTH+20, HALFHEIGHT+180,HALFWIDTH-50, 100))
    playAgain = game.fonts["Big"].render("Play", 1, BLACK)
    screen.blit(playAgain, (HALFWIDTH+110, HALFHEIGHT+215))
    pygame.display.update()

def pauseScreen():
    '''
    () -> None
    This function displays the pause screen
    '''
    pygame.draw.rect(screen, BLACK, (HALFWIDTH-100, HALFHEIGHT,HALFWIDTH-100, 100))
    playAgain = game.fonts["Big"].render("PAUSED", 1, GREEN)
    screen.blit(playAgain, (HALFWIDTH-55, HALFHEIGHT+30))
    pygame.display.update()
    
def redrawScreen():
    '''
    This function updates the screen, drawing according to the game state
    '''
    if not game.starting: #if game not running either: start game or game is over
        if game.gameLost:
            gameOver()
        else: 
            start()
    else: #if game is running
        screen.blit(game.bg,(0,0))
        game.shadow.row = 0
        game.shadow.row = game.shadow.findBottom(game.obst, game.bottom)
        time = game.fonts["Medium2"].render("Time: " + str(int(divmod(game.time//1000,60)[0]))+":"+str(int(divmod(game.time//1000,60)[1])), 1, DARKGREEN) #spliting time into minutes:second
        
        screen.blit(time,(35,((TOP-3)*GRIDSIZE)+5))
        pointstext=game.fonts["Medium2"].render("Points: " + str(game.points),1,DARKGREEN)
        screen.blit(pointstext,(35,(TOP-1)*GRIDSIZE))
        leveltext = game.fonts["Small"].render("Level: " + str(game.level),1,DARKGREEN)
        screen.blit(leveltext,(35,(TOP+1)*GRIDSIZE))
        nextShapetext = game.fonts["Small"].render("Next Shape: ",1,DARKGREEN)
        screen.blit(nextShapetext,(35,213))
        holdShapetext = game.fonts["Small"].render("Hold: ",1,DARKGREEN)
        screen.blit(holdShapetext,(35,295))
        if game.shadow.row > game.tetra.row:
            game.shadow.draw(screen, GRIDSIZE)
        if not (game.tetra.collides(game.obst) and game.tetra.row <= 8):
            game.tetra.draw(screen, GRIDSIZE)
        for ob in game.obst.blocks:
            ob.draw(screen, GRIDSIZE)
        game.nextShape.draw(screen, GRIDSIZE)
        game.holdShape.draw(screen, GRIDSIZE)
        game.bottom.draw(screen, GRIDSIZE)
        game.top.draw(screen, GRIDSIZE)
        game.leftWall.draw(screen, GRIDSIZE)
        game.rightWall.draw(screen, GRIDSIZE)
        screen.blit(game.pauseImg, (0,(TOP-3)*GRIDSIZE))
        if game.pause: #if game is paused
            pauseScreen()
    
    pygame.display.update()


#---------------------------------------#
#   main program                        #
#---------------------------------------#

inPlay = True

while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game.starting: #the starting play button
            cursorX, cursorY = pygame.mouse.get_pos()
            if HALFWIDTH+20<=cursorX<= (HALFWIDTH+20+HALFWIDTH-50) and HALFHEIGHT+180<=cursorY<=(HALFHEIGHT+180+100): #this is the location of the button
                game.reset()
                game.starting = True
                
        if event.type == pygame.MOUSEBUTTONDOWN and not game.pause: #pause button
            cursorX, cursorY = pygame.mouse.get_pos()
            if (TOP-3)*GRIDSIZE<=cursorY<=((TOP-3)*GRIDSIZE+ GRIDSIZE+15) and 0<=cursorX<=GRIDSIZE+15: #location of the pause button
                game.pause = True
                
        elif event.type == pygame.MOUSEBUTTONDOWN and game.pause:
            cursorX, cursorY = pygame.mouse.get_pos()
            if (TOP-3)*GRIDSIZE<=cursorY<=((TOP-3)*GRIDSIZE+ GRIDSIZE+15) and 0<=cursorX<=GRIDSIZE+15:
                game.pause = False     
            
        if game.starting and event.type == pygame.KEYDOWN and not game.pause:
            if event.key == pygame.K_UP: #rotate shadow and tetra
                game.tetra.rotateClkwise()
                game.shadow.rotateClkwise()
                game.rotSound.play()
                if game.tetra.collides(game.leftWall) or game.tetra.collides(
                        game.rightWall) or game.tetra.collides(game.bottom) or game.tetra.collides(game.obst):
                    game.tetra.rotateCntclkwise()
                    game.shadow.rotateCntclkwise()
                    
            if event.key == pygame.K_LEFT: #move tetra and shadow left
                game.tetra.moveLeft()
                game.shadow.moveLeft()
                if game.tetra.collides(game.leftWall) or game.tetra.collides(game.obst):
                    game.tetra.moveRight()
                    game.shadow.moveRight()

            if event.key == pygame.K_RIGHT: #move tetra and shadow right
                game.tetra.moveRight()
                game.shadow.moveRight()

                if game.tetra.collides(game.rightWall) or game.tetra.collides(game.obst):
                    game.tetra.moveLeft()
                    game.shadow.moveLeft()
            if event.key == pygame.K_c and not game.swap: #Place current tetra on hold and generate new tetra
                game.swapSound.play()
                if not game.stored: #shows blank square if not stored
                    game.tetra, game.shadow, game.holdShape = Shape(MIDDLE - 1, TOP, game.nextShapeNo), Shape(MIDDLE - 1, TOP, game.nextShapeNo,shadow=True), Shape(LEFT - 16, TOP+12,game.oldShape)
                    game.oldShape, game.nextShapeNo = game.nextShapeNo, game.oldShape
                    game.holdShapeNo = game.nextShapeNo
                    game.nextShapeNo = randint(1, 7)
                    game.nextShape = Shape(LEFT - 16, TOP+7, game.nextShapeNo)
                    game.swap = True
                    game.stored = True
                else:
                    game.tetra, game.shadow, game.holdShape = Shape(MIDDLE - 1, TOP, game.holdShapeNo), Shape(MIDDLE - 1, TOP, game.holdShapeNo, shadow=True), Shape(LEFT - 16, TOP+12,game.oldShape)
                    game.oldShape, game.holdShapeNo = game.holdShapeNo, game.oldShape
                    game.swap = True
                    game.nextShapeNo = randint(1, 7)
                    game.nextShape = Shape(LEFT - 16, TOP+7, game.nextShapeNo)
            if event.key == pygame.K_SPACE: #move tetra to the bottom
                game.dropSound.play()
                while not (game.tetra.collides(game.bottom) or game.tetra.collides(game.obst)):
                    game.tetra.moveDown()
                game.counter = 0

            if event.key == pygame.K_DOWN: #move tetra down
                game.tetra.moveDown()
    if game.starting and not game.pause:
        if game.counter > 1000: #move tetra down at an according speed based on level (logic below)
            game.counter = 0
            game.tetra.moveDown()
    
        if game.tetra.collides(game.bottom) or game.tetra.collides(game.obst):
            for block in game.tetra.blocks:
                if block.row <= 8: #if the blocks are at the top of the screen the game ends
                    game.starting = False
                    game.gameLost = True
            if inPlay:
                game.tetra.moveUp() #move tetra out of obstacle

                #adding tetra to obst and making new tetra
                game.obst.append(game.tetra)
                game.tetra = Shape(MIDDLE - 1, TOP, game.nextShapeNo)
                game.shadow = Shape(MIDDLE - 1, TOP, game.nextShapeNo, shadow=True)
                game.oldShape = game.nextShapeNo
                game.nextShapeNo = randint(1, 7)
                game.nextShape = Shape(LEFT - 16, TOP+7, game.nextShapeNo)
                game.swap = False
    
            fullRows = game.obst.findFullRows(TOP, FLOOR, COLUMNS)

            #points system
            if 0<len(fullRows)<4:
                game.points += len(fullRows)*100
                game.recentPoints = len(fullRows)*100
                game.lineSound.play()
            elif len(fullRows) == 4:
                if game.recentPoints == 800:
                    game.points += 1300
                    game.recentPoints = 1300
                    game.tetrisSound.play()
                else:
                    game.points += len(fullRows)*200
                    game.recentPoints = len(fullRows)*200
                    game.tetrisSound.play()

            #removing full rows
            game.obst.removeFullRows(fullRows)
    
        #game level system
        game.level = divmod(game.points, 500)[0] + 1

        #tetris speed logic (up by tenth of second every level)
        game.counter += clock.get_time() * (1 + (game.level / 10))  

        #time system
        game.time += clock.get_time()
    
        
        
    clock.tick(10000)
    pygame.time.delay(30)
    redrawScreen()

pygame.quit()
