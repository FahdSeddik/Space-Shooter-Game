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
        self.hit = False
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
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.hit = False
        self.image = image

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
            self.bullets.append(bullet(self.player.position[0] + self.player.dimension[0]/2 -self.dimension[0]/2, self.player.position[1], self.state))

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
            if self.bullets[j].hit:
                continue
            else:
                self.bullets[j].y = self.bullets[j].y - self.bulletSpeed
                self.window.blit(bullet[j].image, (self.bullets[j].x, self.bullets[j].y))

    def reset(self):
        self.numBullets = 0

    def resetBulletPositions(self):
        self.bullets = []
        for i in range(self.maxBullets):
            self.bullets.append(bullet(self.player.position[0] + self.player.dimension[0]/2 -self.dimension[0]/2, self.player.position[1], self.state))

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
        self.attacking=False
        self.hit=False
        self.bullet_hit=False
        if(type=="alien"):
            self.bullet=pygame.image.load('./Images/Enemy/Bullets/Laser.png')
            
            self.sprite=pygame.image.load('./Images/Enemy/Aliens/Alien_'+str(self.sprite_number)+'.png')
        elif(type=="boss"):
            self.health=15*self.difficulty
            self.bullet=pygame.image.load('./Images/Enemy/Bullets/Laser_beam.png')
            self.sprite=pygame.image.load('./Images/Enemy/Bosses/Boss_'+str(self.sprite_number)+'.png')
        elif(type=="structure"):
            self.bullet=pygame.image.load('./Images/Enemy/Bullets/Laser.png')

            self.sprite=pygame.image.load('./Images/Enemy/Structures/Structure_'+str(self.sprite_number)+'.png')
        self.coordinates=[]


    def spawn_enemy(self,coordinates):
        #Coordinates are desired center coordinates of the enemy
        self.coordinates=coordinates
        self.bullet_coords=[coordinates[0]-self.bullet.get_width()/2,coordinates[1]+self.sprite.get_height()/2-self.bullet.get_height()/2]
        # Collision box for enemy bullet
        #self.bullet_CB = CollisionBox(self.bullet.get_width(),self.bullet.get_height(),self.bullet_coords[0]+self.bullet.get_width()/2,self.bullet_coords[1]+self.bullet.get_height()/2)
        # Collision box for enemy
        #self.CB = CollisionBox(self.sprite.get_width(),self.sprite.get_height(),coordinates[0],coordinates[1])
        self.window.blit(self.sprite,(coordinates[0]-self.sprite.get_width()/2,coordinates[1]-self.sprite.get_height()/2))
        self.exp=explosion(self.window,self.coordinates)

    def display_enemy(self):
        self.window.blit(self.sprite,(self.coordinates[0]-self.sprite.get_width()/2,self.coordinates[1]-self.sprite.get_height()/2))
        if self.attacking and not(self.bullet_hit):
            if(self.bullet_coords[1]<=self.window.get_height()):
                self.window.blit(self.bullet,(self.bullet_coords[0],self.bullet_coords[1]))
                self.bullet_coords[1]+=3
            else:
                self.attacking=False
        elif self.attacking and self.bullet_hit:
            self.attacking=False
            self.bullet_hit=False
        else:
            self.bullet_coords=[self.coordinates[0]-self.bullet.get_width()/2,self.coordinates[1]+self.sprite.get_height()/2-self.bullet.get_height()/2]
        if self.hit:
            self.exp=explosion(self.window,self.coordinates)
            self.hit=False
        self.exp.animate()
        #self.bullet_CB.update_coords(self.bullet_coords[0],self.bullet_coords[1])
        #self.CB.update_coords(self.coordinates[0],self.coordinates[1])
        

    def attack(self):
        self.attacking=True

    def isDead(self):
        if (self.health<=0):
            return True

    def move_down(self):
        self.coordinates[1]+=5
    


class Wave():
    def __init__(self,window,difficulty):
        self.window = window
        if(difficulty%10==0 and difficulty>=10):
            self.num_enemies=20
        elif(difficulty*5%45==0):
            self.num_enemies=45
        else:
            self.num_enemies=difficulty*5%45
            
        self.difficulty=difficulty
        self.enemies=[]

    def spawn_enemies(self):
        self.enemies=[]
        if(self.difficulty%10==0 and self.difficulty>=10):
            num_bosses=1
        else:
            num_bosses=0
        for i in range(self.num_enemies):
            self.enemies.append(Enemy(self.window,"alien",random.randint(0,3),self.difficulty))
        
        if(num_bosses==1):
            screenX, screenY = self.window.get_size()
            # 1 Boss
            self.enemies.append(Enemy(self.window,"boss",random.randint(0,0),self.difficulty))
            # 2 Structures
            self.enemies.append(Enemy(self.window,"structure",random.randint(0,0),self.difficulty))
            self.enemies.append(Enemy(self.window,"structure",random.randint(0,0),self.difficulty))
            # For spawning enemies can spawn in different patterns during waves
            # -upward or downward arrow
            # -lines
            # -lines are force in boss waves
            #line configuration
            window_width=self.window.get_width()
            window_height=self.window.get_height()
            # Two lines and boss in middle
            boss_X=window_width/2
            self.line_config(4)
            self.enemies[self.num_enemies].spawn_enemy([boss_X,-2*window_height/3-148])
            self.enemies[self.num_enemies+1].spawn_enemy([64,-window_height/2])
            self.enemies[self.num_enemies+2].spawn_enemy([screenX-64,-window_height/2])
        else:
            self.line_config(int(self.num_enemies/5))
            
    def isDead(self):
        for enemy in self.enemies:
            if(enemy.isDead()):
                return True

        return False

    def line_config(self,lines):
        #line configuration
        window_width=self.window.get_width()
        window_height=self.window.get_height()
        # Two lines and boss in middle
        first_X=window_width/(lines+1)
        if(lines==1):
            # Display
            # E E E E E
            first_X=window_width/6
            y_coords=-window_height
            for i in range(1,6):
                self.enemies[i-1].spawn_enemy([first_X*i,y_coords])
        else:
            y_coords=-window_height
            for j in range(lines):
                y_coords=-window_height
                for i in range(int(5*j),int(5*(j+1))):
                    self.enemies[i].spawn_enemy([first_X*(j+1),y_coords])
                    y_coords+=128
       
    

    def update_enemies(self):
        # Handle enemy movement
        # Handle shooting
        if(self.enemies[0].coordinates[1]<64):
            for enemy in self.enemies:
                enemy.move_down()
                enemy.display_enemy()
        else:
            for enemy in self.enemies:
                if not(enemy.isDead()):
                    enemy.display_enemy()
                    rint=random.randint(0,1000)
                    if(rint<=5):
                        enemy.attack()
                


# class CollisionBox():
#     def __init__(self,width,height,x,y):
#         self.width=width
#         self.height=height

#         # X and Y Coords are the center of the box
#         self.x=x
#         self.y=y
    
#     def update_coords(self,x,y):
#         self.x=x
#         self.y=y

#     def isCollide(self,box):
#         # given another collision box to check if collided with it
#         distance=sqrt((self.x-box.x)**2+(self.y-box.y)**2)
        
#         if distance<=self.width/2:
#             return True
#         else:
#             return False
