import pygame
import random
import sys

pygame.init()

# Димензии на екран
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Бои
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (30, 30, 30)

# Слики и звуци
ship_image = pygame.image.load("spaceship.png")
asteroid_image = pygame.image.load("asteroid.png")
crystal_image = pygame.image.load("energy_crystal.png")
background_music = "background_music.wav"
collect_sound = pygame.mixer.Sound("clash_sound.wav")
explosion_sound = pygame.mixer.Sound("clash_sound.wav")

# Скалирање на сликите
ship_image = pygame.transform.scale(ship_image, (50, 50))
asteroid_image = pygame.transform.scale(asteroid_image, (40, 40))
crystal_image = pygame.transform.scale(crystal_image, (30, 30))

# Поставување на позадинска музика
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

# Време
clock = pygame.time.Clock()
FPS = 60

# Фонт
font = pygame.font.SysFont("Arial", 30)

# Иницијализација на променливи
ship = pygame.Rect(WIDTH // 2, HEIGHT - 70, 50, 50) #поставување на бродот на почетна позиција
astroids = []
crystals = []
score = 0
high_score = 0
speed = 5
asteroid_speed = 4
asteroid_size = 40
max_asteroid_size = 100
game_over = False

# ф-ја за скалирање на астероидите
def scale_asteroids():
    global asteroid_image, asteroid_size
    if asteroid_size < max_asteroid_size:
        asteroid_size += 5
        asteroid_image = pygame.transform.scale(pygame.image.load("asteroid.png"), (asteroid_size, asteroid_size))

# ф-ја за поставување на астероид
def spawn_asteroid():
    x = random.randint(0, WIDTH - asteroid_size)
    y = random.randint(-100, -40) # да паѓа астероидот надолу
    astroids.append(pygame.Rect(x, y, asteroid_size, asteroid_size))

# ф-ја за поставување на кристал
def spawn_crystal():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(-100, -30)
    crystals.append(pygame.Rect(x, y, 30, 30))

# ф-ја за прикажување текст
def draw_text(text, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# ф-ја за ресетирање на играта
def reset_game():
    global score, speed, asteroid_speed, asteroid_size, game_over, astroids, crystals, ship, asteroid_image
    score = 0
    speed = 5
    asteroid_speed = 4
    asteroid_size = 40
    asteroid_image = pygame.transform.scale(pygame.image.load("asteroid.png"), (asteroid_size, asteroid_size))
    game_over = False
    astroids.clear()
    crystals.clear()
    ship.x = WIDTH // 2
    ship.y = HEIGHT - 70


running = True
while running:
    screen.fill(DARK_GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and ship.left > 0:
            ship.x -= speed
        if keys[pygame.K_RIGHT] and ship.right < WIDTH:
            ship.x += speed
        if keys[pygame.K_UP] and ship.top > 0:
            ship.y -= speed
        if keys[pygame.K_DOWN] and ship.bottom < HEIGHT:
            ship.y += speed

    if not game_over:
        if random.randint(1, 60) == 1:
            spawn_asteroid()
        if random.randint(1, 100) == 1:
            spawn_crystal()

    # Update на астероиди
    if not game_over:
        for asteroid in astroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.colliderect(ship): #дали астероидот се судира со бродот
                explosion_sound.play()
                game_over = True
                if score > high_score:
                    high_score = score
            if asteroid.top > HEIGHT:
                astroids.remove(asteroid)

    # Update на кристали
    if not game_over:
        for crystal in crystals[:]:
            crystal.y += asteroid_speed
            if crystal.colliderect(ship):
                collect_sound.play()
                score += 1
                crystals.remove(crystal)
            if crystal.top > HEIGHT:
                crystals.remove(crystal)

    # Зголемување на тежина
    if not game_over and score > 0 and score % 10 == 0:
        speed += 0.01
        asteroid_speed += 0.01
        if score % 20 == 0:
            scale_asteroids()

    # Прикажувае на екран на обејктите
    screen.blit(ship_image, ship)
    for asteroid in astroids:
        screen.blit(asteroid_image, asteroid)
    for crystal in crystals:
        screen.blit(crystal_image, crystal)

    # Приказ на текстот
    draw_text(f"Score: {score}", WHITE, 10, 10)
    draw_text(f"High Score: {high_score}", GREEN, 10, 40)

    if game_over:
        draw_text("GAME OVER", RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", WHITE, WIDTH // 2 - 120, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
