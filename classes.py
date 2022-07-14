import math

import pygame
import os
from math import sqrt
import random

class player:
    # Constructor
    def __init__(self, window, spriteFolder, health, xChange, yChange, speed, gunState, firePower, movementBorder):
        self.window = window
        self.spriteFolder = spriteFolder
        self.health = health
        self.xChange = xChange
        self.yChange = yChange
        self.speed = speed
        self.gunState = gunState
        self.firePower = firePower

        #self.movementBorder takes a border list [max_Xcooridinate, maxYcoordinate]
        self.movementBorder = movementBorder
        self.spriteImages = []


        # Load all the sprite images in the sprite folder into spriteImages list
        playerSprites = os.listdir(spriteFolder)
        numImages = len(playerSprites)
        for i in range(numImages):
            self.spriteImages.append(pygame.image.load(spriteFolder + '/player_' + str(i) + '.png'))

        # Set the current shown sprite image to the still version 0 -> still as initial state
        self.state = self.spriteImages[0]
        self.dimension = [self.spriteImages[0].get_width(), self.spriteImages[0].get_height()]

        # self.position is a position list [xPosition, yPosition]
        screenX, screenY = self.window.get_size()
        self.position = [screenX/2 - self.dimension[0]/2, self.movementBorder[1]]
        self.center = [self.position[0] + self.dimension[0] / 2, self.position[1] + self.dimension[1] / 2]

    def setGunState(self, state):
        self.gunState = state

    def getGunState(self):
        return self.gunState

    def updatePlayerPosition(self):
        self.position[0] += self.xChange * self.speed
        self.position[1] += self.yChange * self.speed

        # Boundary checks

        if self.position[0] >= self.movementBorder[0]- self.dimension[0]:
            self.position[0] = self.movementBorder[0] - self.dimension[0]

        elif self.position[0] <= 0:
            self.position[0] = 0

        if self.position[1]  >= self.movementBorder[1] - self.dimension[1]:
            self.position[1] = self.movementBorder[1] - self.dimension[1]

        elif self.position[1] <= 0:
            self.position[1] = 0

        self.center = [self.position[0] + self.dimension[0]/2, self.position[1] + self.dimension[1]/2]

    def display(self):
        self.window.blit(self.state, (self.position[0], self.position[1]))

    def resetPostion(self):
        screenX, screenY = self.window.get_size()
        self.position = [screenX/2 - self.dimension[0]/2, self.movementBorder[1]]
        self.state = self.spriteImages[0]
        self.center = [self.position[0] + self.dimension[0] / 2, self.position[1] + self.dimension[1] / 2]

    # Scales all images in sprite folder by a multiplyer

    def scale(self, multiplyer):
        for i in range(len(self.spriteImages)):
            image = self.spriteImages[i]
            xDimension = image.get_width() * multiplyer
            yDimension = image.get_height() * multiplyer
            image = pygame.transform.scale(image, (xDimension, yDimension))
            self.spriteImages[i] = image
            self.dimension = [xDimension, yDimension]


class bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class gun:
    def __init__(self, window, spriteFolder, damage, maxBullets, player, reloadTime, bulletSpeed):
        self.window = window
        self.spriteFolder = spriteFolder
        self.damage = damage
        self.maxBullets = maxBullets + 1
        laserSprites = os.listdir(spriteFolder)
        numImages = len(laserSprites)
        self.state = pygame.image.load(self.spriteFolder + '/laser.png')
        self.dimension = [self.state.get_width(), self.state.get_height()]
        self.bullets = []
        self.numBullets = 0
        self.player = player
        self.lastCooldown = pygame.time.get_ticks()
        self.reloadTime = reloadTime
        self.bulletSpeed = bulletSpeed
        for i in range(self.maxBullets):
            self.bullets.append(bullet(self.player.position[0] + self.player.dimension[0]/2 -self.dimension[0]/2, self.player.position[1]))

    def updateBullets(self):
        if self.player.getGunState() == 'fire':
            if (self.numBullets + 1 != self.maxBullets):
                self.player.setGunState('ready')
                self.numBullets = (self.numBullets + 1)% self.maxBullets
                self.bullets[self.numBullets].x = self.player.position[0]
                self.bullets[self.numBullets].y = self.player.position[1]
                self.lastCooldown = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - self.lastCooldown >= self.reloadTime) and not (self.numBullets + 1 != self.maxBullets):
                self.player.setGunState('ready')
                self.numBullets = 0
        for i in range(self.numBullets, self.maxBullets):
            self.bullets[i].x = self.player.position[0] + self.player.dimension[0] / 2 - self.dimension[0] / 2
            self.bullets[i].y = self.player.position[1]
        for j in range(self.numBullets):
            self.bullets[j].y = self.bullets[j].y - self.bulletSpeed
            self.window.blit(self.state, (self.bullets[j].x, self.bullets[j].y))

    def reset(self):
        self.numBullets = 0

    def resetBulletPositions(self):
        self.bullets = []
        for i in range(self.maxBullets):
            self.bullets.append(bullet(self.player.position[0] + self.player.dimension[0]/2 -self.dimension[0]/2, self.player.position[1]))

    def scale(self, multiplyer):
        self.dimension = [self.dimension[0] * multiplyer, self.dimension[1]* multiplyer]
        self.state = pygame.transform.scale(self.state, (self.dimension[0], self.dimension[1]))

class explosion:
    def __init__(self, window, position):
        self.window = window
        self.x = position[0]
        self.y = position[1]
        self.spriteImages = []
        self.spriteFolder = './Images/Explosion'
        explosionSprites = os.listdir(self.spriteFolder)
        numImages = len(explosionSprites)
        for i in range(numImages):
            image = pygame.image.load(self.spriteFolder + '/' + str(i) + '.png')
            image = pygame.transform.scale(image, (image.get_width()/2, image.get_height()/2))
            self.spriteImages.append(image)
            self.spriteImages.append(image)
            self.spriteImages.append(image)
            self.spriteImages.append(image)
        self.currentFrame = self.spriteImages[0]
        self.counter = 0

    def __del__(self):
        pass

    def animate(self):
        if self.counter == len(self.spriteImages):
            self.__del__()
        else:
            self.window.blit(self.spriteImages[self.counter], (self.x, self.y))
            self.counter += 1

class mainMenuBGD:
    def __init__(self, window, folder):
        self.window = window
        self.bgdFolder = folder
        self.bgdImages = []
        backgroundFrames = os.listdir(self.bgdFolder)
        numImages = len(backgroundFrames)
        for i in range(numImages):
            image = pygame.image.load(self.bgdFolder + '/' + str(i) + '.bmp')
            self.bgdImages.append(image)
        self.counter = 0
        self.currentFrame = self.bgdImages[0]


    def animate(self):
        self.window.blit(self.bgdImages[self.counter], (0,0))
        self.counter = (self.counter + 1)% len(self.bgdImages)


class playBackground:
    def __init__(self, window, file, scroll):
        self.window = window
        self.file = file
        self.image = pygame.image.load(self.file).convert()
        self.x, self.y = self.window.get_size()
        self.tiles = math.ceil(self.y/ self.image.get_height()) + 10
        self.scroll = scroll
        self.i = 0

    def incScroll(self):
        self.scroll += 6
        if abs(self.scroll) > self.image.get_height():
            self.scroll = 0

    def animate(self):
        while self.i < self.tiles:
            self.window.blit(self.image, (0, self.image.get_height()*self.i + self.scroll - self.image.get_height()))
            self.i += 1
        self.i = 0
class Enemy():

    def __init__(self,window,type,sprite_number,difficulty):
        self.window=window
        self.type=type
        self.sprite_number=sprite_number
        self.difficulty=difficulty
        self.health=2*self.difficulty
        if(type=="alien"):
            self.sprite=pygame.image.load('./Images/Enemy/Aliens/Alien_'+str(self.sprite_number)+'.png')
        elif(type=="boss"):
            self.sprite=pygame.image.load('./Images/Enemy/Bosses/Boss_'+str(self.sprite_number)+'.png')
        elif(type=="structure"):
            self.sprite=pygame.image.load('./Images/Enemy/Structures/Structure_'+str(self.sprite_number)+'.png')
        self.coordinates=[]


    def spawn_enemy(self,coordinates):
        #Coordinates are desired center coordinates of the enemy
        self.coordinates=coordinates
        self.window.blit(self.sprite,(coordinates[0]-self.sprite.get_width()/2,coordinates[1]-self.sprite.get_height()/2))

    def display_enemy(self):
        self.window.blit(self.sprite,(self.coordinates[0]-self.sprite.get_width()/2,self.coordinates[1]-self.sprite.get_height()/2))


    def move_down(self):
        self.coordinates[1]+=5
        self.window.blit(self.sprite,(self.coordinates[0]-self.sprite.get_width()/2,self.coordinates[1]-self.sprite.get_height()/2))

class Wave():
    def __init__(self,window,num_enemies,difficulty):
        self.window = window
        self.num_enemies=num_enemies
        self.difficulty=difficulty
        self.enemies=[]

    def spawn_enemies(self):
        self.enemies=[]
        if(self.difficulty%10==0 and self.difficulty>=10):
            num_bosses=1
        else:
            num_bosses=0
        for i in range(self.num_enemies-num_bosses):
            self.enemies.append(Enemy(self.window,"alien",random.randint(0,3),self.difficulty))
        if(num_bosses==1):
            self.enemies.append(Enemy(self.window,"boss",random.randint(0,0),self.difficulty))
        # For spawning enemies can spawn in different patterns during waves
        # -upward or downward arrow
        # -lines
        # -lines are force in boss waves
        if(num_bosses==1):
            #line configuration
            window_width=self.window.get_width()
            window_height=self.window.get_height()
            # Two lines and boss in middle
            boss_X=window_width/2
            self.line_config(2)
            self.enemies[self.num_enemies].spawn_enemy([boss_X,-window_height/2])
        else:
            if(self.difficulty==1):
                self.line_config(self.difficulty)
            elif(self.difficulty<=5):
                self.line_config(self.difficulty/2+1)
            else:
                self.line_config(self.difficulty/3+1)

    def line_config(self,lines):
        #line configuration
        window_width=self.window.get_width()
        window_height=self.window.get_height()
        # Two lines and boss in middle
        first_X=window_width/(lines+1)
        
        y_coords=-window_height/2
        for j in range(lines):
            y_coords=-window_height/2
            for i in range(int(self.num_enemies/lines*j),int(self.num_enemies/lines*(j+1))):
                self.enemies[i].spawn_enemy([first_X*(j+1),y_coords])
                y_coords+=(window_height/2)/self.num_enemies
       
            

    def update_enemies(self):
        # Handle enemy movement
        # Handle shooting
        if(self.enemies[0].coordinates[1]<0):
            for i in range(self.num_enemies):
                self.enemies[i].move_down()
                self.enemies[i].display_enemy()
        else:
            for i in range(self.num_enemies):
                self.enemies[i].display_enemy()



