import pygame
import random
import math
import time


pygame.init()

# Window
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_X, screen_Y = window.get_size()
# main_menu -- for main menu
# play -- for play
window_state = "main_menu"         

# Font
font = pygame.font.Font('./Fonts/Minecraft.ttf',64)

status_bar_height=font.render("R",True,(255,255,255)).get_height()
# Loading images

# Player
player_img = pygame.image.load('./Images/Player/Player_0.png')
player_X = player_img.get_width()
player_Y = player_img.get_height()
player_X*=2
player_Y*=2
player_img = pygame.transform.scale(player_img,(player_X,player_Y))
playerX = screen_X/2 - player_X/2
playerY = screen_Y - player_Y - 20
playerX_change = 0
playerY_change = 0
player_speed_multiplier = 3
player_state="still"
gun_state="ready"

# Enemies
enemy_img=[]
enemy_X=[]
enemy_Y=[]
enemyX=[]
enemyY=[]

# Guns/bullets/lasers
guns_laser_img = pygame.image.load('./Images/Guns/laser.png')
guns_laser_X = guns_laser_img.get_width()
guns_laser_Y = guns_laser_img.get_height()
guns_laser_X/=2
guns_laser_Y/=2
guns_laser_img = pygame.transform.scale(guns_laser_img,(guns_laser_X,guns_laser_Y))
bulletsX=[]
bulletsY=[]

num_bullets=0
max_bullets=51
for i in range(max_bullets):
    bulletsX.append(playerX+player_X/2-guns_laser_X/2)
    bulletsY.append(playerY)
# Main Menu 
#name_img = pygame.image.load('GameName.png')
play_btn_img = pygame.image.load('./Images/Menu/PlayBTN.png')
play_btn_img_HL = pygame.image.load('./Images/Menu/PlayBTN_HL.png')
play_btn_X = play_btn_img.get_width()
play_btn_Y = play_btn_img.get_height()
play_btn_startX = screen_X*0.5-play_btn_X*0.5
play_btn_startY = screen_Y*0.5-play_btn_Y*0.5

#settings_btn_img = pygame.image.load('SettingsBTN.png')

# Settings Menu
settings_title_img = pygame.image.load('./Images/Settings/Settings.png')
settings_title_X = settings_title_img.get_width()
settings_title_Y = settings_title_img.get_height()

settings_quit_img = pygame.image.load('./Images/Settings/Quit.png')
settings_quit_X = settings_quit_img.get_width()
settings_quit_Y = settings_quit_img.get_height()
settings_quit_img_HL = pygame.image.load('./Images/Settings/Quit_HL.png')

settings_mainmenu_img = pygame.image.load('./Images/Settings/MainMenu.png')
settings_mainmenu_X = settings_quit_img.get_width()
settings_mainmenu_Y = settings_quit_img.get_height()
settings_mainmenu_img_HL = pygame.image.load('./Images/Settings/MainMenu_HL.png')


def reset():
    global playerX,playerY,num_bullets
    playerX = screen_X/2 - player_X/2
    playerY = screen_Y - player_Y - status_bar_height
    num_bullets=0

def display_gun_status(bullets,max_bullets):
    if(bullets+1==max_bullets):
        gun_status=font.render("Reloading..",True,(255,255,255))
    else:
        gun_status=font.render("Gun: "+ str(bullets)+"/"+str(max_bullets-1),True,(255,255,255))
    window.blit(gun_status,(screen_X-gun_status.get_width(),screen_Y-gun_status.get_height()))


def display_player(x,y):
    window.blit(player_img,(x,y))

clock = pygame.time.Clock()

def main():
    global playerX,playerX_change,num_bullets,max_bullets,status_bar_height
    global playerY,playerY_change,gun_state
    run=True
    window_state = "main_menu"

    last_cooldown=pygame.time.get_ticks()
    while run:
        window.fill((0,0,0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and window_state=="main_menu":
                    run=False
                elif event.key == pygame.K_ESCAPE and window_state=="play":
                    window_state="settings"
                elif event.key == pygame.K_ESCAPE and window_state=="settings":
                    window_state="play"
                if event.key == pygame.K_SPACE and window_state=="play":
                    if gun_state=="ready":
                        gun_state="fire"
                if event.key == pygame.K_d:
                    playerX_change=5
                elif event.key == pygame.K_a:
                    playerX_change=-5
                if event.key == pygame.K_w:
                    playerY_change=-5
                elif event.key == pygame.K_s:
                    playerY_change=5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d and playerX_change>=0:
                    playerX_change=0
                elif event.key == pygame.K_a and playerX_change<=0:
                    playerX_change=0
                if event.key== pygame.K_w and playerY_change<=0:
                    playerY_change=0
                elif event.key == pygame.K_s and playerY_change>=0:
                    playerY_change=0
            if(window_state=="main_menu"):
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0]>=play_btn_startX and mouse_pos[0]<=play_btn_startX+play_btn_X and mouse_pos[1]>=play_btn_startY and mouse_pos[1]<=play_btn_startY+play_btn_Y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        window_state="play"
            if window_state=="settings":
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0]>=screen_X-settings_quit_X and mouse_pos[1]>=screen_Y-settings_quit_Y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run=False
                if (mouse_pos[0]<=settings_mainmenu_X and mouse_pos[1]>=screen_Y-settings_mainmenu_Y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        reset()
                        window_state="main_menu"
            
        
        # main menu display
        if window_state=="main_menu":
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0]>=play_btn_startX and mouse_pos[0]<=play_btn_startX+play_btn_X and mouse_pos[1]>=play_btn_startY and mouse_pos[1]<=play_btn_startY+play_btn_Y):
                window.blit(play_btn_img_HL,(play_btn_startX,play_btn_startY))
            else:
                window.blit(play_btn_img,(play_btn_startX,play_btn_startY))
        # playing display
        elif window_state=="play":
            playerX+=playerX_change*player_speed_multiplier
            playerY+=playerY_change*player_speed_multiplier
            if(playerX>=screen_X-player_X):
                playerX=screen_X-player_X
            elif playerX<=0:
                playerX=0
            if playerY>=screen_Y-player_Y-status_bar_height:
                playerY=screen_Y-player_Y-status_bar_height
            elif playerY<=0:
                playerY=0
            
            if gun_state=="fire":
                if(num_bullets+1!=max_bullets):
                    gun_state="ready"
                    num_bullets=(num_bullets+1) % max_bullets
                    bulletsX[num_bullets]=playerX
                    bulletsY[num_bullets]=playerY
                    last_cooldown=pygame.time.get_ticks()
                elif(pygame.time.get_ticks()-last_cooldown >=2000):
                    gun_state="ready"
                    num_bullets=0
                    
            for i in range(num_bullets,max_bullets):
                bulletsX[i]=playerX+player_X/2-guns_laser_X/2
                bulletsY[i]=playerY
            for i in range(num_bullets):
                bulletsY[i]-=20
                window.blit(guns_laser_img,(bulletsX[i],bulletsY[i]))
            display_gun_status(num_bullets,max_bullets)
            display_player(playerX,playerY)
        elif window_state=="settings":
            window.blit(settings_title_img,(screen_X/2-settings_title_X/2,30))
            if (mouse_pos[0]>=screen_X-settings_quit_X and mouse_pos[1]>=screen_Y-settings_quit_Y):
                window.blit(settings_quit_img_HL,(screen_X-settings_quit_X,screen_Y-settings_quit_Y))
            else:
                window.blit(settings_quit_img,(screen_X-settings_quit_X,screen_Y-settings_quit_Y))
            if (mouse_pos[0]<=settings_mainmenu_X and mouse_pos[1]>=screen_Y-settings_mainmenu_Y):
                window.blit(settings_mainmenu_img_HL,(0,screen_Y-settings_mainmenu_Y))
            else:
                window.blit(settings_mainmenu_img,(0,screen_Y-settings_mainmenu_Y))

        pygame.display.update()



main()