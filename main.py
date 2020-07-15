import pygame
import random
from random import uniform
import math
from pygame import mixer

pygame.init()

height = 600
width = 800

window = pygame.display.set_mode((width, height))

# importing images and sounds
pygame.display.set_caption("KILL CORONA")
icon = pygame.image.load('virus.png').convert_alpha()
player_img0 = pygame.image.load('spaceship4.png').convert_alpha()
player_img1 = pygame.image.load('spaceship1.png').convert_alpha()
player_img2 = pygame.image.load('spaceship2.png').convert_alpha()
player_img3 = pygame.image.load('spaceship3.png').convert_alpha()
enemy_img0 = pygame.image.load('virus.png').convert_alpha()
enemy_img1 = pygame.image.load('virus4.png').convert_alpha()
enemy_img2 = pygame.image.load('virus2.png').convert_alpha()
enemy_img3 = pygame.image.load('virus3.png').convert_alpha()
bg_img0 = pygame.image.load('back0.jpg').convert()
bg_img1 = pygame.image.load('back1.png').convert()
bg_img2 = pygame.image.load('back2.jpg').convert()
bg_img3 = pygame.image.load('back3.jpg').convert()
bg_img4 = pygame.image.load('back4.jpg').convert()
bullet_img = pygame.image.load('bullet_32.png').convert_alpha()

player_img = [player_img0, player_img1, player_img2, player_img3]
enemy_img = [enemy_img0, enemy_img1, enemy_img2, enemy_img3]
bg_img = [bg_img0, bg_img1, bg_img2, bg_img3,bg_img4,]

# player_image = random.choice(player_img)
# bg_image = random.choice(bg_img)

mixer.music.load('background.mp3')
mixer.music.play(-1)
bullet_sound = mixer.Sound('laser.wav')
explode_sound = mixer.Sound('explosion.wav')

pygame.display.set_icon(icon)

# setting up constants and values
player_default_x = width / 2 - 32
player_default_y = 4 * height / 5

player_x = width / 2 - 32
player_y = 4 * height / 5

player_pos_x = 0
player_pos_y = 0

bulletx = player_x
bullety = player_y

bullet_changex = 0
bullet_changey = 20

player_speed = 5
enemy_speed = 2

score_x = 10
score_y = 10

score = 0
count = 1

game_over_stat = False
game_start = True


# defined classes and functions
class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.change_cx = uniform(.5, 2.5)
        self.change_cy = self.change_cx
        self.img = random.choice(enemy_img)

    def show(self, x, y):
        window.blit(self.img, (x, y))

    def reset_position(self):
        self.x = random.randint(0, 736)
        self.y = random.randint(0, 200)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show_bullet(self):
        window.blit(bullet_img, (self.x, self.y))


def player(x, y):
    window.blit(player_image, (x, y))


def draw_text(text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, color)
    window.blit(text, (x, y))


def collision(enemyx, enemyy, bullets):
    for bullet in bullets:
        distance = math.hypot(enemyx - bullet.x, enemyy - bullet.y)
        if distance < 35:
            bullets.remove(bullet)
            return True
    return False


def collision_of_ship(enemyx, enemyy, playerx, playery):
    distance = math.hypot(enemyx - playerx, enemyy - playery)
    if distance < 50:
        return True
    return False


# starting screen
def starting_screen():
    global game_start
    global game_over_stat
    window.blit(random.choice(bg_img), (0, 0))
    draw_text("KILL CORONA", 80, (255, 255, 255), width / 6, height / 5)
    draw_text("INSTRUCTIONS", 50, (255, 0, 0), width / 4, height / 5 + 120)
    draw_text("Arrow keys to move , Space to shoot", 32, (0, 255, 0), width / 6, height / 5 + 170)
    draw_text("Press any key to start", 32, (255, 0, 0), width / 4 + 20, height / 5 + 250)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def show_score():
    draw_text("Score : " + str(score), 32, (0, 255, 255), 10, 10)


def game_over():
    global enemies
    del enemies[0: len(enemies) + 1]


def game_over_text():
    window.blit(bg_image, (0, 0))
    draw_text('Game Over', 80, (255, 255, 255), width / 5 + 20, height / 3)
    draw_text('Your Score : ' + str(score), 50, (255, 0, 0), width / 4 + 30, height / 2 + 20)
    draw_text('Press Enter to play again', 20, (0, 255, 0), width / 3 + 10, height * 3 / 5 + 50)


fps = pygame.time.Clock()

# loop starts here
running = True
while running:
    # iniializing new game and showing main window
    while game_start:
        fps.tick(60)
        starting_screen()
        enemies = []
        enemy = Enemy(random.randint(0, 736), random.randint(0, 200))
        enemies.append(enemy)
        bullets = []
        player_image = random.choice(player_img)
        bg_image = random.choice(bg_img)
        game_start = False
    fps.tick(60)
    window.fill((0, 0, 0))

    window.blit(bg_image, (0, 0))
    # checking for key press event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:

            if game_over_stat == False:
                bulletx = player_x + 16
                bullety = player_y - 20
                bullet = Bullet(bulletx, bullety)
                bullets.append(bullet)
                bullet_sound.play()

        elif game_over_stat == True and keys[pygame.K_RETURN]:
            new_game_enemy = Enemy(random.randint(0, 736), random.randint(0, 200))
            enemies.append(new_game_enemy)
            player_x = player_default_x
            player_y = player_default_y
            score = 0
            mixer.music.unpause()
            player_image = random.choice(player_img)
            bg_image = random.choice(bg_img)
            game_over_stat = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos_x -= player_speed

            if event.key == pygame.K_RIGHT:
                player_pos_x += player_speed

            if event.key == pygame.K_DOWN:
                player_pos_y += player_speed

            if event.key == pygame.K_UP:
                player_pos_y -= player_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_DOWN or pygame.K_UP:
                player_pos_y = 0
                player_pos_x = 0

    # updating player position and checking bounds
    player_x += player_pos_x
    player_y += player_pos_y
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    if player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536

    # collision check between enemies and bullets
    for enemy in enemies:
        if enemy.x <= 0:
            enemy.change_cx = enemy_speed
        elif enemy.x >= 736:
            enemy.change_cx = -enemy_speed
        if enemy.y <= 0:
            enemy.change_cy = enemy_speed
        elif enemy.y >= 536:
            enemy.change_cy = -enemy_speed

        enemy.x += enemy.change_cx
        enemy.y += enemy.change_cy

        colision = collision(enemy.x, enemy.y, bullets)
        if colision == True:
            explode_sound.play()
            bulletx = player_x
            score += 1
            enemy.reset_position()
            x = random.randint(0, 736)
            y = random.randint(0, 200)
            new_enemy = Enemy(x, y)
            enemy_image = random.choice(enemy_img)
            enemies.append(new_enemy)

        collision_ships = collision_of_ship(enemy.x, enemy.y, player_x, player_y)
        if collision_ships == True:
            explode_sound.play()
            game_over_stat = True
            break

    # drawing player
    player(player_x, player_y)

    # drawing enemies
    for enemy in enemies:
        enemy.show(enemy.x, enemy.y)

    # drawing and updating position of bullets
    for bullet in bullets:
        bullet.show_bullet()
        bullet.y -= bullety / 60
        if bullet.y < 0:
            bullets.remove(bullet)

    # showing score
    show_score()

    # checking if game is running/not running
    if game_over_stat == True:
        game_over_text()
        game_over()
        mixer.music.pause()

    # updating display
    pygame.display.update()

pygame.quit()
