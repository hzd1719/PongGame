import pygame, sys, time, random, math
from pygame.locals import*
from time import sleep


HEIGHT = 800
WIDTH = 1000
TEXTCOLOR = (255, 255 ,255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 80
RECTANGLEHEIGHT = 100
RECTHANGLEWIDTH = 20
RECTANGLEMOVERATE = 8
BALLSPEED = 6

RED = (255, 0, 0)
GREEN = (0, 255, 0)

def terminate():
    pygame.quit()
    sys.exit()


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# Set up pygame
pygame.init()
main_clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong game")
pygame.mouse.set_visible(False)

# Set up fonts
font = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 56)

# Set up sounds
pygame.mixer.music.load('C:/Users/User/Desktop/python/GPongGame/background.mp3')
score_sound = pygame.mixer.Sound('C:/Users/User/Desktop/python/GPongGame/score.wav')

# Set up images
pongImage = pygame.image.load("C:/Users/User/Desktop/python/GPongGame/pong2.png")
pongImage.set_colorkey((0, 0, 0))
pongRect = pygame.Rect(WIDTH/2, HEIGHT/2 ,25, 25)
pongSurface = pygame.transform.scale(pongImage,(25, 25))
#pongRect = pongImage.get_rect()

# Setting up players
player1 = pygame.Rect(10, HEIGHT / 2 - RECTANGLEHEIGHT/2, RECTHANGLEWIDTH, RECTANGLEHEIGHT)
player2 = pygame.Rect(WIDTH - 27, HEIGHT / 2 - RECTANGLEHEIGHT/2, RECTHANGLEWIDTH, RECTANGLEHEIGHT)



matches1 = 0
matches2 = 0

while True:
    # Setting up the start screen
    window.fill(BACKGROUNDCOLOR)
    drawText("Pong game", font2, window, (WIDTH / 3) + 50, (HEIGHT / 2))
    drawText("Press a key to start.", font2, window, (WIDTH / 3) - 30, (HEIGHT / 3) + 50)
    pygame.display.update()
    drawText('Games won: {}:{}'.format(matches1, matches2), font, window, WIDTH/2 - 120, 0)
    pygame.display.update()
    waitForPlayerToPressKey()
    score1 = 0
    score2 = 0
    move_up1 = move_down1 = False
    move_up2 = move_down2 = False
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.1)
    musicPlaying = True
    ball_x_movement = 1 if random.random() < 0.5 else -1
    ball_y_movement = 1 if random.random() < 0.5 else -1


    while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        move_down1 = False
                        move_up1 = True
                    if event.key == K_s:
                        move_up1 = False
                        move_down1 = True

                    if event.key == K_UP:
                        move_down2 = False
                        move_up2 = True
                    if event.key == K_DOWN:
                        move_up2 = False
                        move_down2 = True
                    if event.key == K_m:
                        if musicPlaying:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1, 0.0)
                        musicPlaying = not musicPlaying
                
                if event.type == KEYUP:
                    if event.key == K_w:
                        move_up1 = False
                    if event.key == K_s:
                        move_down1 = False
                    if event.key == K_UP:
                        move_up2 = False
                    if event.key == K_DOWN:
                        move_down2 = False
        
        if move_up1 and player1.top > 0:
            player1.top += -1 * RECTANGLEMOVERATE
        if move_down1 and player1.bottom < HEIGHT:
            player1.top += RECTANGLEMOVERATE
        if move_up2 and player2.top > 0:
            player2.top += -1 * RECTANGLEMOVERATE
        if move_down2 and player2.bottom < HEIGHT:
            player2.top += RECTANGLEMOVERATE

        
        # Ball Movenemnt
        #pongRect.left += ball_x_movement*BALLSPEED
        #pongRect.top += ball_y_movement*BALLSPEED
        if pongRect.colliderect(player1):
            if BALLSPEED < 20:
                BALLSPEED += 1
            if player1.top < 1:
                player1.top == 1
            collidePoint = pongRect.left - (player1.left + player1.top/2)
            try:
                collidePoint = collidePoint/(player1.top/2)
            except ZeroDivisionError:
                #collidePoint = collidePoint/(0.000001/2)
                collidePoint = 1.01
            
            angleRad = collidePoint * math.pi/4
            direction = 1 if pongRect.left < WIDTH/2 else -1 
            ball_x_movement = direction * (math.cos(angleRad))
            ball_y_movement = math.sin(angleRad)
        if pongRect.colliderect(player2):
            if BALLSPEED < 20:
                BALLSPEED += 1
            if player2.top < 1:
                player2.top == 1
            collidePoint = pongRect.left - (player2.left + player2.top/2)
            try:
                collidePoint = collidePoint/(player2.top/2)
            except ZeroDivisionError:
                #collidePoint = collidePoint/(0.000001/2)
                collidePoint = 1.01
            angleRad = collidePoint * math.pi/4
            direction = 1 if pongRect.left < WIDTH/2 else -1 
            ball_x_movement = direction * (math.cos(angleRad))
            ball_y_movement = math.sin(angleRad)

            #ball_x_movement = -ball_x_movement
            #ball_y_movement = random.randint(-1,1)
        pongRect.left += ball_x_movement*BALLSPEED
        pongRect.top += ball_y_movement*BALLSPEED
        
        if pongRect.left < -3:
            score2 += 1
            score_sound.play()
            sleep(0.5)
            pongRect.left = WIDTH/2
            pongRect.top = HEIGHT/2
            player1.top = HEIGHT/2
            player2.top = HEIGHT/2
            BALLSPEED = 6
            ball_x_movement = -ball_x_movement
            ball_y_movement = -ball_y_movement
            
        if pongRect.left >= WIDTH-20:
            score1 +=1
            score_sound.play()
            sleep(0.5)
            pongRect.left = WIDTH/2
            pongRect.top = HEIGHT/2
            player1.top = HEIGHT/2
            player2.top = HEIGHT/2
            BALLSPEED = 6
            ball_x_movement = -ball_x_movement
            ball_y_movement = -ball_y_movement

        #If the ball hits the walls
        if pongRect.top >= HEIGHT - 20 or pongRect.top < 0:
            ball_y_movement = -ball_y_movement
            if BALLSPEED < 10:
                BALLSPEED += 1

        
        window.fill(BACKGROUNDCOLOR)
        # Draw the score
        drawText('Score: {}:{}'.format(score1, score2), font, window, WIDTH/2 - 60, 0)
        # Draw player1
        pygame.draw.rect(window, GREEN, player1)
        # Draw player2
        pygame.draw.rect(window, RED, player2)

        # Draw the ball
        window.blit(pongSurface, pongRect)
        
        pygame.display.update()

        if score1 == 5:
            matches1 += 1
            break
        if score2 == 5:
            matches2 +=1
            break
        
        main_clock.tick(FPS)
    pygame.mixer.music.stop()
                