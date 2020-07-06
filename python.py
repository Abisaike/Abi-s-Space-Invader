import pygame
import random
import math
from pygame import mixer

# initialise
pygame.init()

# window,title,icon,
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Abi's Space invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background2.mp3')
mixer.music.play(-1)

# player
player_img = pygame.image.load('space-invaders.png')
player_posi_X = 370
player_posi_Y = 480
player_changeX = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# enemy
enemy_img = []
enemy_posi_X = []
enemy_posi_Y = []
enemy_changeX = []
enemy_changeY = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    enemy_posi_X.append(random.randint(0, 735))
    enemy_posi_Y.append(random.randint(50, 150))
    enemy_changeX.append(4)
    enemy_changeY.append(45)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_posi_X = 0
bullet_posi_Y = 480
bullet_changeX = 0
bullet_changeY = 15
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))  # to center the bullet in the spaceship


# collision
def collision_happ(enemy_posi_X, enemy_posi_Y, bullet_posi_X, bullet_posi_Y):
    distance = math.sqrt(math.pow(enemy_posi_X - bullet_posi_X, 2) + (math.pow(enemy_posi_Y - bullet_posi_Y, 2)))
    if distance < 27:
        return True
    else:
        return False


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_Y = 10


def scoring(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    game_over_font = game_over_font.render("GAME OVER !", True, (255, 255, 255))
    screen.blit(game_over_font, (200, 250))


# Game window loop
screen_run = True
while screen_run:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_run = False
        # movement of the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_changeX = -5
            if event.key == pygame.K_RIGHT:
                player_changeX = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_posi_X = player_posi_X  # getting the current x coordinate
                    fire_bullet(player_posi_X, bullet_posi_Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_changeX = 0

    player_posi_X += player_changeX

    # player border position
    if player_posi_X <= 0:
        player_posi_X = 0
    elif player_posi_X >= 736:
        player_posi_X = 736

    # enemy border position
    for i in range(no_of_enemies):
        # game over
        if enemy_posi_Y[i] > 440:
            game_over_text()
            for j in range(no_of_enemies):
                enemy_posi_Y[j] = 2000
                break
        if enemy_posi_X[i] <= 0:
            enemy_posi_Y[i] += enemy_changeY[i]
            enemy_changeX[i] = 4
        elif enemy_posi_X[i] >= 736:
            enemy_posi_Y[i] += enemy_changeY[i]
            enemy_changeX[i] = -4
        enemy_posi_X[i] += enemy_changeX[i]

        # collision
        collision = collision_happ(enemy_posi_X[i], enemy_posi_Y[i], bullet_posi_X, bullet_posi_Y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_posi_Y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_posi_X[i] = random.randint(0, 735)
            enemy_posi_Y[i] = random.randint(50, 150)

        enemy(enemy_posi_X[i], enemy_posi_Y[i], i)

    # bullet persistance
    if bullet_posi_Y <= 0:
        bullet_state = "ready"
        bullet_posi_Y = 480
    if bullet_state is "fire":
        fire_bullet(bullet_posi_X, bullet_posi_Y)
        bullet_posi_Y -= bullet_changeY

    player(player_posi_X, player_posi_Y)
    scoring(text_x, text_Y)
    pygame.display.update()
