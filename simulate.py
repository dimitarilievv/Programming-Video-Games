# Simulate (a Simon clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, time, pygame
from pygame.locals import *

# Константи за играта
FPS = 30  # Фрејмови во секунда
WINDOWWIDTH = 640  # Ширина на прозорецот
WINDOWHEIGHT = 480  # Висина на прозорецот
FLASHSPEED = 500  # Брзина на светкање на копчињата (во милисекунди)
FLASHDELAY = 200  # Задршка меѓу светкања (во милисекунди)
BUTTONSIZE = 50  # Големина на секое копче
BUTTONGAPSIZE = 20  # Простор меѓу копчињата
TIMEOUT = 4  # Време (во секунди) пред "Game Over" ако нема активност

# Бои (RGB вредности)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
ORANGE = (255,165,0)
BRIGHTORANGE=(0,255,0)
PURPLE=(60,60,60)
BRIGHTPURPLE=(0,60,0)
PINK=(255,120,0)
BRIGHTPINK=(0,120,255)
CYAN = (0, 255, 255)


# Позадинска боја на прозорецот
bgColor = BLACK

# Позиционирање на копчињата во прозорецот
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rect објекти за четирите копчиња
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
PURPLERECT = pygame.Rect(XMARGIN, YMARGIN - BUTTONSIZE - BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
ORANGERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN - BUTTONSIZE - BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
PINKRECT = pygame.Rect(XMARGIN - BUTTONSIZE - BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
CYANRECT = pygame.Rect(XMARGIN + BUTTONSIZE * 3 + BUTTONGAPSIZE * 3, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)


# Главна функција која го стартува програмот
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the buttons.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0
    waitingForInput = False

    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN
                elif event.key == K_e:
                    clickedButton = PURPLE
                elif event.key == K_r:
                    clickedButton = ORANGE
                elif event.key == K_t:
                    clickedButton = PINK

        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN, PURPLE, ORANGE, PINK)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                gameOverAnimation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Завршување на играта
def terminate():
    pygame.quit()
    sys.exit()


# Проверка дали играта треба да се затвори
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


# Анимација за светкање на копче
def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    elif color == PURPLE:
        sound = BEEP1
        flashColor = BRIGHTPURPLE
        rectangle = PURPLERECT
    elif color == ORANGE:
        sound = BEEP2
        flashColor = BRIGHTORANGE
        rectangle = ORANGERECT
    elif color == PINK:
        sound = BEEP3
        flashColor = BRIGHTPINK
        rectangle = PINKRECT
        # elif color == CYAN:
        sound = BEEP4  # Reuse sound file
        flashColor = (0, 255, 255)  # Cyan color
        rectangle = CYANRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE)).convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))


# Цртање на копчињата
def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
    pygame.draw.rect(DISPLAYSURF, PURPLE, PURPLERECT)
    pygame.draw.rect(DISPLAYSURF, ORANGE, ORANGERECT)
    pygame.draw.rect(DISPLAYSURF, PINK, PINKRECT)
    pygame.draw.rect(DISPLAYSURF, CYAN, CYANRECT)  # Draw new cyan button


# Врати кое копче е кликнато
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE
    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    elif PURPLERECT.collidepoint((x, y)):
        return PURPLE
    elif ORANGERECT.collidepoint((x, y)):
        return ORANGE
    elif PINKRECT.collidepoint((x, y)):
        return PINK
    elif CYANRECT.collidepoint((x, y)):  # Cyan button click
        return CYAN
    return None


# Анимација за промена на позадина
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT)).convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newSurf, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


# Анимација за Game Over
def gameOverAnimation(color=WHITE, animationSpeed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    for i in range(3):  # Светкање три пати
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashSurf.fill((color[0], color[1], color[2], alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


# Повик на главната функција
if __name__ == '__main__':
    main()
