###                                            Chrome's running game 2.0

#libraries
import pygame
from sys import exit
from random import randint

#setup
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
music = pygame.mixer.Sound('Audio/music.wav')
music.set_volume(0.1)
jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
jump_sound.set_volume(0.3)
music.play()
game_active = False
clock = pygame.time.Clock()
text_font = pygame.font.Font('Fonts/Pixeltype.ttf', 50)

# graphics
sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

#obstacles
snail1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
snail2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
snails = [snail1, snail2]
snail_index = 0
snail = snails[snail_index]

fly1 = pygame.image.load('Graphics/fly/fly1.png').convert_alpha()
fly2 = pygame.image.load('Graphics/fly/fly2.png').convert_alpha()
flies = [fly1, fly2]
fly_index = 0
fly = flies[fly_index]

obstacle_list = []

#player
player1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
player2 = pygame.image.load('Graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player1, player2]
player_jump = pygame.image.load('Graphics/player/jump.png').convert_alpha()
player_index = 0

player = player_walk[player_index]
player_rect = player.get_rect(midbottom = (80,300))

def player_animation():
    global player, player_index

    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk [int(player_index)]



#intro
poster = pygame.image.load('Graphics/player/player_stand.png').convert_alpha()
poster = pygame.transform.rotozoom(poster, 0, 2)
poster_rect = poster.get_rect(center = (400,200))
name = text_font.render("Chrome's runner 2.0", False, (111,196,169))
name_rect = name.get_rect(center = (400, 80))
message = text_font.render("Press space to run", False, (111,196,169))
message_rect = name.get_rect(center = (400, 340))

gravity = -0
start_time = 0
score = 0

#score
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score = text_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score.get_rect(center = (400,50))
    screen.blit(score, score_rect)
    return current_time

#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


#movements
def obstacle_movement(objects):
    if objects:
        for object in objects:
            object.x -= 5

            if object.bottom == 300:
                screen.blit(snail, object)
            else:
                screen.blit(fly, object)

        objects = [object for object in objects if object.x > -100]
        return objects
    else:
        return []
    
#collisions
def collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
    return True

while True:
    #listening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if player_rect.bottom == 300:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint((event.pos)):
                        gravity = -20
                        jump_sound.play()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        gravity = -20
                        jump_sound.play()

            if event.type == obstacle_timer:
                starting_x = randint(900,1100)
                if randint(0,2):
                    obstacle_list.append(snail.get_rect(bottomright = (starting_x,300)))
                else:
                    obstacle_list.append(fly.get_rect(bottomright = (starting_x,210)))

            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail = snails[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly = flies[fly_index]


        else:
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        game_active = True
                        start_time = int(pygame.time.get_ticks()/1000)
        


    if game_active:
        music.play(loops = -1)
        # draw elements
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        # screen.blit(snail, snail_rect)
        # snail_rect.x -= 4

        #player
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player, player_rect)

        #movement
        obstacle_list = obstacle_movement(obstacle_list)
        player_animation()

        #collision
        game_active = collisions(player_rect, obstacle_list)


    else:
        music.set_volume(0)
        screen.fill((94,129,162))
        screen.blit(poster, poster_rect)
        screen.blit(name, name_rect)
        obstacle_list.clear()
        player_rect.midbottom = (80,300)
        gravity = 0

        score_message = text_font.render(f'Your score is: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            screen.blit(message, message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        

    pygame.display.update()
    clock.tick(60)