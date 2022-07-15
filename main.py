try:
    import pygame
except:
    import pip
    pip.main(['install', 'pygame'])
    import pygame

from classes import *

pygame.init()

# Window
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_X, screen_Y = window.get_size()
# main_menu -- for main menu
# play -- for play
window_state = "main_menu"         
icon=pygame.image.load('./Images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("AstroZone - by Fahd Seddik and Abdelrahman Wael")
# Font
font = pygame.font.Font('./Fonts/Minecraft.ttf',64)

status_bar_height=font.render("R",True,(255,255,255)).get_height()


# *****************************
# --===Loading Menu Images===--
# *****************************

# Main Menu
name_img = pygame.image.load('./Images/Menu/GameName.png')
name_img=pygame.transform.scale(name_img,(name_img.get_width()*2,name_img.get_height()*2))
play_btn_img = pygame.image.load('./Images/Menu/PlayBTN.png')
play_btn_img_HL = pygame.image.load('./Images/Menu/PlayBTN_HL.png')
play_btn_X = play_btn_img.get_width()
play_btn_Y = play_btn_img.get_height()
play_btn_startX = screen_X*0.5-play_btn_X*0.5
play_btn_startY = screen_Y*0.5-play_btn_Y*0.5

play_frame0 = pygame.image.load('./Images/Menu/Background/0.bmp')
play_frame0 = pygame.transform.scale(play_frame0,(screen_X,screen_Y))
play_frame1 = pygame.image.load('./Images/Menu/Background/1.bmp')
play_frame1 = pygame.transform.scale(play_frame1,(screen_X,screen_Y))
play_frame2 = pygame.image.load('./Images/Menu/Background/2.bmp')
play_frame2 = pygame.transform.scale(play_frame2,(screen_X,screen_Y))
play_frame3 = pygame.image.load('./Images/Menu/Background/3.bmp')
play_frame3 = pygame.transform.scale(play_frame3,(screen_X,screen_Y))
play_frame4 = pygame.image.load('./Images/Menu/Background/4.bmp')
play_frame4 = pygame.transform.scale(play_frame4,(screen_X,screen_Y))
play_frame5 = pygame.image.load('./Images/Menu/Background/5.bmp')
play_frame5 = pygame.transform.scale(play_frame5,(screen_X,screen_Y))
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

# Game clock
clock = pygame.time.Clock()
last_cooldown=pygame.time.get_ticks()
highestLevel=0
# Highscore System
lastLevel = 0
with open('highestLevel.txt', 'r') as file:
    highestLevel = file.read()
    equalSign = highestLevel.find('=')
    highestLevel = int(highestLevel[equalSign+1:])
highestScoreLabel = font.render("Highest Level = " + str(highestLevel),True,(255,255,255))
# *****************************
# ----======Functions======----
# *****************************

# Displays gun reloading text and current bullets in window_state "play"
def display_gun_status(bullets,max_bullets):
    if(bullets+1==max_bullets):
        gun_status=font.render("Reloading..",True,(255,255,255))
    else:
        gun_status=font.render("Gun: "+ str(max_bullets-1-bullets)+"/"+str(max_bullets-1),True,(255,255,255))
    window.blit(gun_status,(screen_X-gun_status.get_width(),screen_Y-gun_status.get_height()))

def display_wave(level):
    wave = font.render("Wave: " + str(level),True,(255,255,255))
    window.blit(wave,(0,screen_Y-wave.get_height()))

# Displaying images/text only for mainmenu
def mainmenu_display():
    global play_btn_img,play_btn_startX,play_btn_img_HL,play_btn_X,play_btn_startY,play_btn_Y,name_img,highestLevel
    mouse_pos = pygame.mouse.get_pos()
    # Check for Hovering over button
    # Display highlighted (HL) btn
    press=font.render("Press Esc to exit game.",True,(255,0,0))
    press=pygame.transform.scale(press,(press.get_width()/2,press.get_height()/2))
    window.blit(press,(0,screen_Y-press.get_height()))
    window.blit(name_img,(screen_X/2-name_img.get_width()/2,20))
    highestScoreLabel=font.render("Highest Level = " + str(highestLevel),True,(255,255,255))
    window.blit(highestScoreLabel, (screen_X / 2 - highestScoreLabel.get_width() / 2, screen_Y - highestScoreLabel.get_height()))
    if (mouse_pos[0]>=play_btn_startX and mouse_pos[0]<=play_btn_startX+play_btn_X and mouse_pos[1]>=play_btn_startY and mouse_pos[1]<=play_btn_startY+play_btn_Y):
        window.blit(play_btn_img_HL,(play_btn_startX,play_btn_startY))
    else:
        window.blit(play_btn_img,(play_btn_startX,play_btn_startY))

# Displaying images/text only for settings
def settings_display():
    global window,settings_title_img,screen_X,settings_title_X
    global screen_X,settings_quit_X,screen_Y,settings_quit_Y
    global settings_quit_img_HL,settings_quit_img
    global settings_mainmenu_X,settings_mainmenu_Y,settings_mainmenu_img_HL,settings_mainmenu_img
    # Settings Title
    window.blit(settings_title_img,(screen_X/2-settings_title_X/2,-50))
    # Check for hovering and display appropriate HL btn img
    t=font.render("Game Paused",True,(0,255,0))
    t=pygame.transform.scale(t,(t.get_width()/3,t.get_height()/3))
    window.blit(t,(screen_X/2-t.get_width()/2,settings_title_Y-120))
    mouse_pos = pygame.mouse.get_pos()
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

def enemy_collisions(enemies,player_bullets,bullet_dmg):
    # using pygame's collisions

    for enemy in enemies:
        if not(enemy.isDead()) and not(enemy.hit):
            for bullet in player_bullets:
                if enemy.CB.isCollide(bullet.collisionBox) and not(bullet.hit) and bullet.shot:
                    enemy.hit=True
                    bullet.hit=True
                    enemy.health-=bullet_dmg


def player_collisions(player,enemies):
    # using pygame's collisions

    for enemy in enemies:
        if not(enemy.isDead()) and not(enemy.bullet_hit):
            if player.CB.isCollide(enemy.bullet_CB) and not(player.hit):
                player.hit=True
                enemy.bullet_hit=True
                player.health-=enemy.dmg

def gameover_display():
    gameover=font.render("Game Over",True,(255,0,0))
    press=font.render("Press Esc to return to Main Menu.",True,(255,255,255))
    gameover=pygame.transform.scale(gameover,(gameover.get_width()*2,gameover.get_height()*2))
    window.blit(gameover,(screen_X/2-gameover.get_width()/2,screen_Y/2-gameover.get_height()/2))
    window.blit(press,(screen_X/2-press.get_width()/2,screen_Y-press.get_height()))

def display_health(health,maxhealth):
    global screen_X,screen_Y
    if health<=maxhealth*0.5:
        color=(255, 248, 10)
    if health<=maxhealth*0.2:
        color=(255,0,0)
    if health>maxhealth*0.5:
        color=(0, 255, 0)
    hp=font.render("HP: "+str(health)+"/"+str(maxhealth),True,color)
    window.blit(hp,(screen_X/2-hp.get_width()/2,screen_Y-hp.get_height()))

def updateLastLevel(player, level):
    global lastLevel
    if player.health <= 100:
        lastLevel = level

def updateHighestLevel():
    global highestLevel
    with open('./highestLevel.txt', 'w') as file:
        file.write('highestLevel = ' + str(highestLevel))

# **************************
# ----=======Main=======----
# **************************

def main():
    global status_bar_height, current_menu_frame,play_frames, screen_X, screen_Y,highestLevel
    Player = player(window, './Images/Player', 100, 0, 0, 3, 'ready', 10, [screen_X, screen_Y - status_bar_height])
    Player.scale(2)
    Player.resetPostion()
    Gun = gun(window, './Images/Guns', 10, 50, Player, 2000, 20)
    Gun.scale(0.5)
    Gun.resetBulletPositions()
    run=True
    window_state = "main_menu"
    
    playBGD = playBackground(window, './Images/Playing/0.jpg', 100)

    level=1
    Waves=Wave(window,difficulty=level)
    Waves.spawn_enemies()
    next_wave=False
    # last cooldown for gun reloading
    Gun.lastCooldown = pygame.time.get_ticks()
    counter = 0

    #Game Loop
    while run:
        # Game CLOCK
        clock.tick(60)

        # BGD
        if window_state != "main_menu":
            if window_state == "play":
                playBGD.incScroll()
                playBGD.animate()
            else:
                window.fill((0,0,0))
        elif(counter <= 5):
            counter +=1
        else:
            window.blit(play_frames[current_menu_frame],(0, 0))
            current_menu_frame = (current_menu_frame+1)%6
            counter = 0

    #**************************************************
    # Looping on events
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
                elif event.key == pygame.K_ESCAPE and window_state=="game_over":
                    level=1
                    Waves=Wave(window,difficulty=level)
                    Waves.spawn_enemies()
                    Gun.reset()
                    Player.resetPostion()
                    Player.health=Player.maxHealth
                    window_state="main_menu"
                # if gun is ready and pressed SPACE change state to fire
                if event.key == pygame.K_SPACE and window_state=="play":
                    if Player.getGunState() == 'ready':
                        Player.setGunState('fire')
                if event.key ==pygame.K_l:
                    next_wave=True
            
                # Movement KEYS
                if event.key == pygame.K_d:
                    Player.xChange = 5
                elif event.key == pygame.K_a:
                    Player.xChange = -5
                if event.key == pygame.K_w:
                    Player.yChange = -5
                elif event.key == pygame.K_s:
                    Player.yChange = 5
            
            if event.type == pygame.KEYUP:
                # Movement KEYS adjustment
                if event.key == pygame.K_d and Player.xChange>=0:
                    Player.xChange = 0
                elif event.key == pygame.K_a and Player.xChange<=0:
                    Player.xChange = 0
                if event.key== pygame.K_w and Player.yChange<=0:
                    Player.yChange = 0
                elif event.key == pygame.K_s and Player.yChange>=0:
                    Player.yChange = 0

        #==========================================
        # --==BUTTON CLICKS ON ANY WINDOW STATE==--

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
                        level=1
                        Waves=Wave(window,difficulty=level)
                        Waves.spawn_enemies()
                        Gun.reset()
                        Player.resetPostion()
                        Player.health=Player.maxHealth
                        window_state="main_menu"
                # TODO: Add extra butt
        #==========================================

    # Finished looping on events
    #**************************************************

#**************************************************
# --===Displays===--
        # Main Menu displayx
        if window_state=="main_menu":
            mainmenu_display()
        # Play display
        elif window_state=="play":
            
            # Handle player position
            Player.updatePlayerPosition()
            # Handle Gun states
            Gun.updateBullets()
            if Player.health<=0:
                window_state="game_over"
            # Display Gun status and player
            display_health(Player.health,Player.maxHealth)
            display_gun_status(Gun.numBullets,Gun.maxBullets)
            display_wave(level)
            Player.display()
            Waves.update_enemies()
            updateLastLevel(Player, level)
            if Waves.isDead() or next_wave:
                next_wave=False
                level+=1
                if level>=highestLevel:
                    highestLevel=level
                Waves=Wave(window,difficulty=level)
                Waves.spawn_enemies()
            if Waves.ready:
                Player.start=True
                enemy_collisions(Waves.enemies, Gun.bullets, Player.firePower)
                player_collisions(Player,Waves.enemies)
        # Settings display
        elif window_state=="settings":
            settings_display()
        elif window_state=="game_over":
            gameover_display()
#**************************************************
        # Update Screen
        pygame.display.update()


# Call Main
main()
updateHighestLevel()