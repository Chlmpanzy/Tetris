from Classes import *
from random import randint
import pygame

pygame.init()
clock = pygame.time.Clock()
HEIGHT = 600
WIDTH = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GREY = (192, 192, 192)

shapeNo = randint(1, 7)
tetra = Shape(MIDDLE - 1, TOP, shapeNo)
shadow = Shape(MIDDLE - 1, TOP, shapeNo, shadow=True)
nextShapeNo = randint(1, 7)
nextShape = Shape(LEFT - 16, TOP+5, nextShapeNo)
oldShape = shapeNo
holdShapeNo = 0
holdShape = Shape(LEFT - 16, TOP+12, 8)

bottom = Floor(LEFT, BOTTOM, COLUMNS)
leftWall = Wall(LEFT - 1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obst = Obstacles(LEFT, BOTTOM - 1)

counter = 0
level = 1
time = 0
font = pygame.font.SysFont("Ariel Black",40)
font2 = pygame.font.SysFont("Ariel Black",24)
font3 = pygame.font.SysFont("Ariel Black",30)
swap = False
stored = False
points = 0
tetris = False
recentPoints = 0
starting = False
soundVolume = 0.4

pygame.mixer.music.load("Ruins.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops = -1)
levelSound = pygame.mixer.Sound("clear_level.wav")
levelSound.set_volume(soundVolume)
rotSound = pygame.mixer.Sound("block-rotate.wav")
rotSound.set_volume(soundVolume)
lineSound = pygame.mixer.Sound("clearline (2).wav")
lineSound.set_volume(0.7)
dropSound = pygame.mixer.Sound("land.wav")
dropSound.set_volume(soundVolume)
overSound = pygame.mixer.Sound("gameover.wav")
overSound.set_volume(soundVolume)
#add swap sound

bgImage = pygame.image.load("dswallpaper(4).jpeg")
bg = pygame.transform.scale(bgImage,(WIDTH,HEIGHT))

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def start():
    '''
    () -> None
    This function displays the introduction screen
    '''
    screen.fill (BLACK)
    playAgain = font.render("Play", 1, BLACK)
    pygame.draw.rect(screen, GREEN, (WIDTH//2-250, HEIGHT//2,WIDTH//2+10, 100))
    screen.blit(playAgain, (WIDTH//2-125, HEIGHT//2+30))
    pygame.display.update()

def gameOver():
    '''
    () -> None
    This function displays the game over screen
    '''
    screen.fill (BLACK)
    playAgain = font.render("Play Again", 1, BLACK)
    pygame.draw.rect(screen, GREEN, (WIDTH//2-250, HEIGHT//2,WIDTH//2+10, 100))
    screen.blit(playAgain, (WIDTH//2-125, HEIGHT//2+30))
    pygame.display.update()

def redrawScreen():
    if starting:
        screen.blit(bg,(0,0))
        shadow.row = 0
        shadow.row = shadow.findBottom(obst, bottom)
        pointstext=font.render("Points: " + str(points),1,DARKGREEN)
        screen.blit(pointstext,(15,(TOP-1)*GRIDSIZE))
        rptext = font2.render("Level: " + str(level),1,DARKGREEN)
        screen.blit(rptext,(15,(TOP+1)*GRIDSIZE))
        if shadow.row > tetra.row:
            shadow.draw(screen, GRIDSIZE)
        tetra.draw(screen, GRIDSIZE)
        for ob in obst.blocks:
            ob.draw(screen, GRIDSIZE)
        nextShape.draw(screen, GRIDSIZE)
        holdShape.draw(screen, GRIDSIZE)
        bottom.draw(screen, GRIDSIZE)
        leftWall.draw(screen, GRIDSIZE)
        rightWall.draw(screen, GRIDSIZE)
    else:
        start()
    

    pygame.display.update()


#---------------------------------------#
#   main program                        #
#---------------------------------------#

inPlay = True

while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN and not starting:
            cursorX, cursorY = pygame.mouse.get_pos()
            if WIDTH//2-250<=cursorX<= WIDTH//2+210 and HEIGHT//2<=cursorY<=HEIGHT//2+100:
                starting = True

        if starting and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetra.rotateClkwise()
                shadow.rotateClkwise()
                rotSound.play()
                if tetra.collides(leftWall) or tetra.collides(
                        rightWall) or tetra.collides(bottom) or tetra.collides(
                            obst):
                    tetra.rotateCntclkwise()
                    shadow.rotateCntclkwise()
                    
            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
                shadow.moveLeft()
                if tetra.collides(leftWall) or tetra.collides(obst):
                    tetra.moveRight()
                    shadow.moveRight()

            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
                shadow.moveRight()

                if tetra.collides(rightWall) or tetra.collides(obst):
                    tetra.moveLeft()
                    shadow.moveLeft()
            if event.key == pygame.K_c and not swap:
                if not stored:
                    tetra, shadow, holdShape = Shape(MIDDLE - 1, TOP, nextShapeNo), Shape(MIDDLE - 1, TOP, nextShapeNo,shadow=True), Shape(LEFT - 16, TOP+12,oldShape)
                    oldShape, nextShapeNo = nextShapeNo, oldShape
                    holdShapeNo = nextShapeNo
                    swap = True
                    stored = True
                else:
                    tetra, shadow, holdShape = Shape(
                        MIDDLE - 1, TOP, holdShapeNo), Shape(MIDDLE - 1, TOP, holdShapeNo, shadow=True), Shape(LEFT - 16, TOP+12,oldShape)
                    oldShape, holdShapeNo = holdShapeNo, oldShape
                    swap = True
            if event.key == pygame.K_SPACE:
                dropSound.play()
                while not (tetra.collides(bottom) or tetra.collides(obst)):
                    tetra.moveDown()
                counter = 0

            if event.key == pygame.K_DOWN:
                tetra.moveDown()
    if starting:
        if counter > 1000:
            counter = 0
            tetra.moveDown()
    
        if tetra.collides(bottom) or tetra.collides(obst):
            print("level:", level)
            print("points:", points)
            for block in tetra.blocks:
                print(block.row)
                if block.row <= 8:
                    starting = False
            if inPlay:
                tetra.moveUp()
                obst.append(tetra)
                #obst.show()
                tetra = Shape(MIDDLE - 1, TOP, nextShapeNo)
                shadow = Shape(MIDDLE - 1, TOP, nextShapeNo, shadow=True)
                oldShape = nextShapeNo
                nextShapeNo = randint(1, 7)
                nextShape = Shape(LEFT - 16, TOP+5, nextShapeNo)
                swap = False
    
            fullRows = obst.findFullRows(TOP, FLOOR, COLUMNS) 
            if 0<len(fullRows)<4:
                points += len(fullRows)*100
                recentPoints = len(fullRows)*100
                lineSound.play()
            elif len(fullRows) == 4:
                if recentPoints == 800:
                    points += 1300
                    recentPoints = 1300
                    lineSound.play()
                else:
                    points += len(fullRows)*200
                    recentPoints = len(fullRows)*200
                    lineSound.play()
               
            obst.removeFullRows(fullRows)
            print(recentPoints)
    
        
        level = divmod(points, 500)[0] + 1
            
        counter += clock.get_time() * (1 + (level / 10))  
    
        
    clock.tick(10000)
    pygame.time.delay(30)
    redrawScreen()

pygame.quit()
