import math
import random
import pygame

#Initializing pygame
pygame.init()
pygame.font.init()

#Setting up a game timer for the whole game
elapsed = pygame.time.set_timer(pygame.USEREVENT, 1000)


ScreenWidth = 1000
ScreenHeight = 500

paused = False
enemyDead = False
counter = 5

global projectileX, projectileY

bullets = []

clock = pygame.time.Clock()

# Score
global scoreVal
scoreVal = 0

font = pygame.font.Font('freesansbold.ttf', 64)
game_over_font = pygame.font.Font('freesansbold.ttf', 20)
game_time_font = pygame.font.Font('freesansbold.ttf', 20)

# Creating the screen
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

# Display Caption and Icons
pygame.display.set_caption("Fate of The World")
GameIcon = pygame.image.load("Images/save-the-world.png")
pygame.display.set_icon(GameIcon)

# Background
bgx = 0
background = pygame.image.load("Images/Clouds.png")
bg = pygame.transform.scale(background, (ScreenWidth, ScreenHeight))

# Player
playerImg = pygame.image.load("Images/Player3.png")
playerX = 50
playerY = 100
playerVel = 1

# Enemy
enemyImg = pygame.image.load("Images/enemy.png")
enemyIm = pygame.transform.scale(enemyImg, (50, 50))
enemyX = random.randint(500, 900)
enemyY = random.randint(60, 400)

#Projectile class for the bullet
class projectile(object):

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#Redrawing the game window to allow frame by frame bullet movement
def redrawGameWindow():
    for bullet in bullets:
        bullet.draw(screen)

#Player / Plane GUI
def Player(x, y):
    screen.blit(playerImg, (x, y))

#Enemy / CO2 cloud GUI
def Enemy(x, y):
    screen.blit(enemyIm, (x, y))

#Collision detection
def ifCollisionEnemy(enemyX, enemyY, projectileX, projectileY):
    distance = math.sqrt((math.pow(enemyX - projectileX, 2)) + (math.pow(enemyY - projectileY, 2)))
    if distance < 50:
        return True
    else:
        return False

#Rendering score font to the screen
def show_score(x, y):
    score = font.render(str(scoreVal), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Rendering time to the screen
def show_time(x, y):
    gameTime = font.render("Time Left: " + str(counter), True, (0, 0, 0))
    screen.blit(gameTime, (x, y))

#Main Game loop
running = True
while running:

    #Implementing the scrolling background
    RelX = bgx % bg.get_rect().width

    screen.blit(bg, (RelX - bg.get_rect().width, 0))

    if RelX < ScreenWidth:

        screen.blit(bg, (RelX, 0))
    bgx -= 0.5


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Reducing the counter every second
        if event.type == pygame.USEREVENT:
            counter -= 1

    #Implementing bullet instantiation
    for bullet in bullets:
        if bullet.x < ScreenWidth:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

        #Check collision of bullet with enemy
        collisionE = ifCollisionEnemy(enemyX, enemyY, bullet.x, bullet.y)

        #Making new enemy after collision
        if collisionE:
            scoreVal += 1
            enemyX = random.randint(500, 900)
            enemyY = random.randint(60, 400)
            counter += 1

    Player(playerX, playerY)

    #Checking for input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        playerX -= playerVel
    if keys[pygame.K_RIGHT]:
        playerX += playerVel
    if keys[pygame.K_UP]:
        playerY -= playerVel
    if keys[pygame.K_DOWN]:
        playerY += playerVel
    #Shooting the bullet
    if keys[pygame.K_SPACE]:
        if len(bullets) < 1:
            bullets.append(projectile(playerX + 240, playerY + 170, 6, (0, 0, 0)))

    #Implementing X boundaries onto the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 610:
        playerX = 610

    #Implementing Y boundaries onto the player
    if playerY >= 300:
        playerY = 300
    elif playerY <= -60:
        playerY = -60

    Enemy(enemyX, enemyY)

    #Showing GUI
    show_score(500, 10)
    show_time(100, 400)

    #Lose condition
    if counter < 0:
        screen.fill((0, 0, 0))
        GameOverText = game_over_font.render("You Suck, Have you ever considered getting a life?", True, (255, 255, 255))
        screen.blit(GameOverText, (50, 200))

    #Win condition
    if counter > 60 or scoreVal >= 50:
        screen.fill((0, 0, 0))
        GameOverText = game_over_font.render("You Win, You are a true gamer", True,
                                             (255, 255, 255))
        screen.blit(GameOverText, (50, 200))

    redrawGameWindow()
    pygame.display.update()

pygame.quit()