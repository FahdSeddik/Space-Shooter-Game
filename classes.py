import pygame
import os
from math import sqrt


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
        self.position = [screenX/2 - self.dimension[0], self.movementBorder[1]]
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
        self.position = [screenX/2 - self.dimension[0], self.movementBorder[1]]
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
            image = pygame.image.load(self.bgdFolder + '/' + str(i) + '.png')
            self.bgdImages.append(image)
        self.counter = 0
        self.currentFrame = self.bgdImages[0]


    def animate(self):
        self.window.blit(self.bgdImages[self.counter], (0,0))
        self.counter = (self.counter + 1)% len(self.bgdImages)
