import pygame, sys
from pygame.locals import *
import time

pygame.init()

# set up the window
FPS = 40
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

# load cat image
catImg = pygame.image.load("C:/Users/dimit/Downloads/cat3.png")
catx = 10
caty = 10
direction = 'right'
catImg = pygame.transform.scale(catImg, (200, 100))

# set up font and text
font = pygame.font.Font(None, 36)
text = font.render('Helloooooooooooooooooo', True, BLACK)
text_rect = text.get_rect(center=(200, 150))

# load sound
soundObj = pygame.mixer.Sound("C:/Users/dimit/Downloads/file_example_WAV_1MG.wav")
soundObj.play()  # Play the sound once at the beginning
start_time = time.time()  # record the start time

while True:
    DISPLAYSURF.fill(WHITE)  # Fill the screen with white

    # Move the cat image based on the current direction
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw shapes
    pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
    pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
    pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)
    pygame.draw.circle(DISPLAYSURF, RED, (300, 50), 20, 0)
    pygame.draw.ellipse(DISPLAYSURF, RED, (300, 200, 40, 80), 1)
    pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

    # Draw the cat image at the updated position
    DISPLAYSURF.blit(catImg, (catx, caty))

    # Modify pixels (optional)
    pixObj = pygame.PixelArray(DISPLAYSURF)
    pixObj[380][280] = BLACK
    pixObj[382][282] = BLACK
    pixObj[384][284] = BLACK
    pixObj[386][286] = BLACK
    pixObj[388][288] = BLACK
    del pixObj

    # Draw text
    DISPLAYSURF.blit(text, text_rect)

    # Stop the sound after 3 seconds
    if time.time() - start_time > 3:
        soundObj.stop()

    # Update the display
    pygame.display.update()

    # Control the frame rate
    fpsClock.tick(FPS)
