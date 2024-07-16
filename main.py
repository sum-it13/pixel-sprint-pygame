import pygame
from sys import exit
from random import randint

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surface = text.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center= (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=6
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -110]
        return obstacle_list  
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                return False
    return True

def  player_anime():
    global player_surf, player_index
    if player_rect.bottom < 300:
        #jump
        player_surf = player_jump
    else:
        #walk
        player_index+=0.1
        if player_index>=len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
    # walking animation on floor
    # jump animation when in air

pygame.init()
#does some stuff in the bg to run images and audio files
screen = pygame.display.set_mode((800,400))#display on
pygame.display.set_caption('PixelSprint')#title
clock = pygame.time.Clock()
text = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0 #used to restart game
score = 0 #to display score


sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_image = pygame.image.load('graphics/ground.png').convert()

#Obstacles 
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png')
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png')
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


obstacle_rect_list = []



player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_surf = player_walk[player_index]

player_rect = player_surf.get_rect(midbottom=(80,300))
#creating rectangle to make alignment easier and to detect collisions
player_gravity = 0
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()

#Intro screen
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = text.render('Pixel Sprint',False,(64,64,64))
game_name_rect = game_name.get_rect(center=(400,100))
game_msg = text.render('press space to sprint',False,(64,64,64))
game_msg_rect = game_msg.get_rect(center=(400,300))

#Timer
obstacle_timer = pygame.USEREVENT+1 # bcoz some are already reserved
pygame.time.set_timer(obstacle_timer,1500)
snail_anime_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_anime_timer,300)
fly_anime_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_anime_timer,100)

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()#clicking on close
            exit()#opposite of .init()
        if game_active:    
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rect.bottom>=300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active = True
                start_time=pygame.time.get_ticks()//1000
        if game_active:
            if event.type==obstacle_timer :
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1100),250)))
            if event.type == snail_anime_timer:
                if snail_frame_index == 0: snail_frame_index=1
                else:snail_frame_index=0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_anime_timer:
                if fly_frame_index==0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index ]

    if game_active:
        screen.blit(sky_surface,(0,0))#blit=block image transfer
        screen.blit(ground_image,(0,300))
        #screen.blit(score_surface,score_rect)
        score = display_score()

        # snail_rect.x -=6 #speed of snail
        # if snail_rect.right<0:
        #     snail_rect.left=800
        # screen.blit(snail_surface,snail_rect)

        #Player
        player_gravity+=1 #speed increases like gravity
        player_rect.y+=player_gravity
        if player_rect.bottom>=300:
            player_rect.bottom = 300
        player_anime()
        screen.blit(player_surf,player_rect)

        # Obstacle
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rect,obstacle_rect_list)

    else:#separates game over window
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity = 0 # to start on ground not air
        player_rect.midbottom= (80,300)
        score_msg = text.render(f'Your Score: {score}',False,(64,64,64))
        score_msg_rect = score_msg.get_rect(center=(400,330))
        screen.blit(game_name,game_name_rect)
        if score==0:
            screen.blit(game_msg,game_msg_rect)
        else:
            screen.blit(score_msg,score_msg_rect)
        

    pygame.display.update()#keeps looking for events(inputs)
    clock.tick(60)#locks to 60fps

     
