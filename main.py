import pygame
import random
import math
import time
import os

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

# ****************************
# ----=======Player=======----
# ****************************
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


# *****************************
# ----=======Enemies=======----
# *****************************
# Enemies divide into 3 Categories
# - Aliens: small
# - Bosses: large
# - Structures: stationary


# has different alien images
alien_img=[]
# contains dimensions of each alien image
alien_X=[]
alien_Y=[]

# has locations of aliens on screen
alienX=[]
alienY=[]

LIST_DIR_ALIENS = os.listdir('./Images/Enemy/Aliens')
num_aliens = len(LIST_DIR_ALIENS)
for i in range(num_aliens):
    alien_img.append(pygame.image.load('./Images/Enemy/Aliens/Alien_'+str(i)+'.png'))
    alien_X.append(alien_img[i].get_width())
    alien_Y.append(alien_img[i].get_height())
    
# has different boss images
boss_img=[]
# contains dimensions of each boss image
boss_X=[]
boss_Y=[]

# has locations of boss on screen
bossX=[]
bossY=[]
LIST_DIR_BOSSES = os.listdir('./Images/Enemy/Bosses')
num_bosses = len(LIST_DIR_BOSSES)
for i in range(num_bosses):
    boss_img.append(pygame.image.load('./Images/Enemy/Bosses/Boss_'+str(i)+'.png'))
    boss_X.append(boss_img[i].get_width())
    boss_Y.append(boss_img[i].get_height())


# has different structure images
structure_img=[]
# contains dimensions of each structure image
structure_X=[]
structure_Y=[]

# has locations of structure on screen
structureX=[]
structureY=[]
LIST_DIR_STRUCTURES = os.listdir('./Images/Enemy/Structures')
num_structures = len(LIST_DIR_STRUCTURES)
for i in range(num_structures):
    structure_img.append(pygame.image.load('./Images/Enemy/Structures/Structure_'+str(i)+'.png'))
    structure_X.append(structure_img[i].get_width())
    structure_Y.append(structure_img[i].get_height())



# ****************************
# -----=======Guns=======-----
# ****************************

guns_laser_img = pygame.image.load('./Images/Guns/laser.png')
guns_laser_X = guns_laser_img.get_width()
guns_laser_Y = guns_laser_img.get_height()
guns_laser_X/=2
guns_laser_Y/=2
guns_laser_img = pygame.transform.scale(guns_laser_img,(guns_laser_X,guns_laser_Y))
bulletsX=[]
bulletsY=[]


# Set initial positions for bullets to be at player position
# All max_bullets bullets are pre-loaded into array
# After each fire bullets are displayed accordingly
# Max bullets ensures that no performance issues occur
num_bullets=0
max_bullets=51
for i in range(max_bullets):
    bulletsX.append(playerX+player_X/2-guns_laser_X/2)
    bulletsY.append(playerY)

# *****************************
# --===Loading Menu Images===--
# *****************************

#name_img = pygame.image.load('GameName.png')
play_btn_img = pygame.image.load('./Images/Menu/PlayBTN.png')
play_btn_img_HL = pygame.image.load('./Images/Menu/PlayBTN_HL.png')
play_btn_X = play_btn_img.get_width()
play_btn_Y = play_btn_img.get_height()
play_btn_startX = screen_X*0.5-play_btn_X*0.5
play_btn_startY = screen_Y*0.5-play_btn_Y*0.5
play_frame0 = pygame.image.load('./Images/Menu/Background/0.png')
play_frame1 = pygame.image.load('./Images/Menu/Background/1.png')
play_frame2 = pygame.image.load('./Images/Menu/Background/2.png')
play_frame3 = pygame.image.load('./Images/Menu/Background/3.png')
play_frame4 = pygame.image.load('./Images/Menu/Background/4.png')
play_frame5 = pygame.image.load('./Images/Menu/Background/5.png')
play_frames = [play_frame0,  play_frame1, play_frame2, play_frame3, play_frame4,play_frame5]
current_menu_frame = 0

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



# *****************************
# ----======Functions======----
# *****************************

# Reset function
# called when window_state changes from "play" to "main_menu"
def reset():
    global playerX,playerY,num_bullets
    playerX = screen_X/2 - player_X/2
    playerY = screen_Y - player_Y - status_bar_height
    num_bullets=0

# Displays gun reloading and current bullets in window_state "play"
def display_gun_status(bullets,max_bullets):
    if(bullets+1==max_bullets):
        gun_status=font.render("Reloading..",True,(255,255,255))
    else:
        gun_status=font.render("Gun: "+ str(bullets)+"/"+str(max_bullets-1),True,(255,255,255))
    window.blit(gun_status,(screen_X-gun_status.get_width(),screen_Y-gun_status.get_height()))

# Display Player
def display_player(x,y):
    window.blit(player_img,(x,y))

# Game clock
clock = pygame.time.Clock()

# Main menu refresh
def mainmenu_background(i):
    global play_frames
    window.blit(play_frames[i],(0, 0))

# **************************
# ----=======Main=======----
# **************************

def main():
    global playerX,playerX_change,num_bullets,max_bullets,status_bar_height
    global playerY,playerY_change,gun_state, current_menu_frame
    run=True
    window_state = "main_menu"

    # last cooldown for gun reloading
    last_cooldown=pygame.time.get_ticks()

    #Game Loop
    while run:
        # BGD
        if window_state != "main_menu":
            window.fill((0,0,0))
        # Game CLOCK
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                # Exit if on main_menu and pressed ESCAPE
                if event.key == pygame.K_ESCAPE and window_state=="main_menu":
                    run=False
                # Go to settings if on main_menu and pressed ESCAPE
                elif event.key == pygame.K_ESCAPE and window_state=="play":
                    window_state="settings"
                # Play if on settings and pressed ESCAPE
                elif event.key == pygame.K_ESCAPE and window_state=="settings":
                    window_state="play"
                # if gun is ready and pressed SPACE change state to fire
                if event.key == pygame.K_SPACE and window_state=="play":
                    if gun_state=="ready":
                        gun_state="fire"

                # Movement KEYS
                if event.key == pygame.K_d:
                    playerX_change=5
                elif event.key == pygame.K_a:
                    playerX_change=-5
                if event.key == pygame.K_w:
                    playerY_change=-5
                elif event.key == pygame.K_s:
                    playerY_change=5
                
            if event.type == pygame.KEYUP:
                # Movement KEYS adjustment
                if event.key == pygame.K_d and playerX_change>=0:
                    playerX_change=0
                elif event.key == pygame.K_a and playerX_change<=0:
                    playerX_change=0
                if event.key== pygame.K_w and playerY_change<=0:
                    playerY_change=0
                elif event.key == pygame.K_s and playerY_change>=0:
                    playerY_change=0
            
            # Check for button clicks

            # MAIN MENU BUTTONS
            if(window_state=="main_menu"):
                mouse_pos = pygame.mouse.get_pos()
                # Play Button
                if (mouse_pos[0]>=play_btn_startX and mouse_pos[0]<=play_btn_startX+play_btn_X and mouse_pos[1]>=play_btn_startY and mouse_pos[1]<=play_btn_startY+play_btn_Y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        window_state="play"
                # TODO: Add extra buttons

            # SETTINGS BUTTONS
            if window_state=="settings":
                mouse_pos = pygame.mouse.get_pos()
                # Quit Button
                if (mouse_pos[0]>=screen_X-settings_quit_X and mouse_pos[1]>=screen_Y-settings_quit_Y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run=False
                # Main Menu Button
                if (mouse_pos[0]<=settings_mainmenu_X and mouse_pos[1]>=screen_Y-settings_mainmenu_Y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        reset()
                        window_state="main_menu"
                # TODO: Add extra buttons
            
        
        # Main Menu display
        if window_state=="main_menu":
            if current_menu_frame <= 5:
                mainmenu_background(current_menu_frame)
                current_menu_frame += 1
            else:
                current_menu_frame = 0
                mainmenu_background(current_menu_frame)
            mouse_pos = pygame.mouse.get_pos()
            # Check for Hovering over button
            # Display highlighted (HL) btn
            if (mouse_pos[0]>=play_btn_startX and mouse_pos[0]<=play_btn_startX+play_btn_X and mouse_pos[1]>=play_btn_startY and mouse_pos[1]<=play_btn_startY+play_btn_Y):
                window.blit(play_btn_img_HL,(play_btn_startX,play_btn_startY))
            else:
                window.blit(play_btn_img,(play_btn_startX,play_btn_startY))
        # Play display
        elif window_state=="play":
            # Update player position
            # with speed multiplier
            playerX+=playerX_change*player_speed_multiplier
            playerY+=playerY_change*player_speed_multiplier

            # Check for boundaries
            if(playerX>=screen_X-player_X):
                playerX=screen_X-player_X
            elif playerX<=0:
                playerX=0
            if playerY>=screen_Y-player_Y-status_bar_height:
                playerY=screen_Y-player_Y-status_bar_height
            elif playerY<=0:
                playerY=0
            
            # Handle Gun states
            if gun_state=="fire":
                if(num_bullets+1!=max_bullets):
                    gun_state="ready"
                    num_bullets=(num_bullets+1) % max_bullets
                    bulletsX[num_bullets]=playerX
                    bulletsY[num_bullets]=playerY
                    # update last cooldown each fire
                    last_cooldown=pygame.time.get_ticks()
                # if on cooldown check if 2 seconds (2000 ms) passed
            if(pygame.time.get_ticks()-last_cooldown >=2000 and not (num_bullets+1!=max_bullets)):
                    gun_state="ready"
                    num_bullets=0
            # update not fired bullet positions to player
            for i in range(num_bullets,max_bullets):
                bulletsX[i]=playerX+player_X/2-guns_laser_X/2
                bulletsY[i]=playerY
            # Move fired bullet positions
            for i in range(num_bullets):
                bulletsY[i]-=20
                window.blit(guns_laser_img,(bulletsX[i],bulletsY[i]))

            # Display Gun status and player
            display_gun_status(num_bullets,max_bullets)
            display_player(playerX,playerY)
        
        # Settings display
        elif window_state=="settings":
            # Settings Title
            window.blit(settings_title_img,(screen_X/2-settings_title_X/2,30))
            # Check for hovering and display appropriate HL btn img

            # Quit BTN
            if (mouse_pos[0]>=screen_X-settings_quit_X and mouse_pos[1]>=screen_Y-settings_quit_Y):
                window.blit(settings_quit_img_HL,(screen_X-settings_quit_X,screen_Y-settings_quit_Y))
            else:
                window.blit(settings_quit_img,(screen_X-settings_quit_X,screen_Y-settings_quit_Y))
            
            # Main Menu BTN
            if (mouse_pos[0]<=settings_mainmenu_X and mouse_pos[1]>=screen_Y-settings_mainmenu_Y):
                window.blit(settings_mainmenu_img_HL,(0,screen_Y-settings_mainmenu_Y))
            else:
                window.blit(settings_mainmenu_img,(0,screen_Y-settings_mainmenu_Y))

        # Update Screen
        pygame.display.update()


# Call Main
main()