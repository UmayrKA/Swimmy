import pygame
import random

# Set up the enemy's brain
class Enemy():
    # Enemy constructer function
    def __init__(self, x,y, speed,size):
        # make the enemy's variables
        self.x = x
        self.y = y
        self.pic = pygame.image.load("../assets/Fish02_A.png")
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.25), self.size)

        # Shrink the enemy pic
        self.pic = pygame.transform.scale(self.pic, (int (self.size*1.25),self.size))

        #Flip the pic if the Enemy is moving left
        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)

    # Enemy uptade function (stuff to happen over and over again)       
    def update(self, screen):
        self.x += self.speed
        self.hitbox.x += self.speed
        #pygame.draw.rect(screen, (255, 0, 255), self.hitbox)
        screen.blit(self.pic, (self.x, self.y))
        
# End of Enemy class

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# Load all the pictures for our game
background_pic = pygame.image.load("../assets/Scene_A.png")
background_pic2 = pygame.image.load("../assets/Scene_B.png")
player_pic = pygame.image.load("../assets/NewFish05_B.png")

# Make some variables for the backgound animation
bg_animation_timer_max = int(7.5)
bg_animation_timer = bg_animation_timer_max
bg_animation_frame = 0

# Make some variables for our player
player_starting_x = 480
player_starting_y = 310
player_starting_size = 30
player_x = player_starting_x
player_y = player_starting_y
player_speed = 10
player_size = player_starting_size
player_facing_left = False
player_hitbox = pygame.Rect(player_x, player_y, int(player_size*1.25), player_size)
player_alive = False

# Make some variables for the HUD (heads-up display)
score = -1
score_font = pygame.font.SysFont("default", 30)
score_text = score_font.render("Score: "+str(score), 1, (255,255,255))
play_button_pic = pygame.image.load("../assets/BtnPlayIcon.png")
play_button_x = game_width/2 - play_button_pic.get_width()/2
play_button_y = game_height/2 - play_button_pic.get_height()/2
title_pic = pygame.image.load("../assets/swimmy.png")
title_x = game_width/2 - title_pic.get_width()/2
title_y = play_button_y - 130




# Make the enemy spawning timer variable
enemy_timer_max = 45
enemy_timer = enemy_timer_max

#Make the enemies array
enemies = []
enemies_to_remove = []

# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Check to see what keys the player is pressing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_facing_left = False
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_facing_left = True
        player_x -= player_speed
    if keys[pygame.K_DOWN]:
        player_y+= player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_SPACE]:
        player_size +=2

    # Stop the player from leaving the screen
    if player_x < 0:
        player_x = 0
    if player_x > game_width - player_size*1.25:
        player_x = game_width - player_size*1.25
    if  player_y < 0:
        player_y = 0
    if player_y > game_height - player_size:
        player_y = game_height - player_size
    
        

    # Stop the player from leaving the screen.
        
    # Do the background animation_timer
    bg_animation_timer -= 1
    if bg_animation_timer<= 0:
        bg_animation_frame += 1
        if bg_animation_frame > 1 :
            bg_animation_frame = 0
        bg_animation_timer = bg_animation_timer_max
    
    if bg_animation_frame == 0:
        screen.blit(background_pic, (0,0))
    else:
        screen.blit(background_pic2, (0,0))

    # Spawn a new Enemy whenever enemy_timer hits 0
    enemy_timer -=1
    if enemy_timer <= 0:
        new_enemy_y = random.randint(0, game_height - 30)
        new_enemy_speed = random.randint(1, 5)
        new_enemy_size = random.randint(player_size/2, player_size*2)
        if random.randint(0, 1) == 0:
            enemies.append(Enemy(-new_enemy_size*2, new_enemy_y, new_enemy_speed, new_enemy_size))
        else:
            enemies.append(Enemy(game_width,new_enemy_y,-new_enemy_speed, new_enemy_size))
        enemy_timer = enemy_timer_max

    for enemy in enemies_to_remove:
        enemies.remove(enemy)
    enemies_to_remove = []
    
                           
    # Update all the enemies
    for enemy in enemies:
        enemy.update(screen)
        if enemy.x < - 1000 or enemy.x > game_width+1000:
            enemies_to_remove.append(enemy)
        
    if player_alive:        
        # Update the player hitbox       
        player_hitbox.x = player_x
        player_hitbox.y = player_y
        player_hitbox.width = int(player_size * 1.25)
        player_hitbox.height = player_size
        #pygame.draw.rect(screen, (255, 255, 255), player_hitbox)

        # Check to see when the player hits a Enemy
        for enemy in enemies:
            if player_hitbox.colliderect(enemy.hitbox):
                if player_size >= enemy.size:
                    score += enemy.size
                    player_size += 2
                    enemies.remove(enemy)
                else:
                    player_alive = False
    
        # Draw the player pic
        player_pic_small = pygame.transform.scale(player_pic, (int(player_size*1.25), player_size))
        if player_facing_left:
            player_pic_small = pygame.transform.flip(player_pic_small, True, False)
        screen.blit(player_pic_small, (player_x, player_y))

    # Draw the score text
    if player_alive:
        score_text = score_font.render("Score: "+str(score), 1, (255,255,255))
    else:
        score_text = score_font.render("Final Score: "+str(score),1, (255,255,255))
    if score >= 0:
            screen.blit(score_text, (30,30))

    # Draw the menu(when the player is not alive)
    if not player_alive:
        screen.blit(play_button_pic, (play_button_x, play_button_y))
        screen.blit(title_pic, (title_x, title_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Checck to see if the player clicks the play button
        if pygame.mouse.get_pressed()[0]:
            if mouse_x > play_button_x and mouse_x < play_button_x+play_button_pic.get_width():
                if mouse_y > play_button_y and mouse_y < play_button_y+play_button_pic.get_height():
                    # Restart the game
                    player_alive = True
                    score = 0
                    player_x = player_starting_x
                    player_y= player_starting_y
                    player_size = player_starting_size
                    for enemy in enemies:
                        enemies_to_remove.append(enemy)
                    
    
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
