###                                            Chrome's running game 2.0

#libraries
import pygame
from sys import exit
from random import randint, choice

#sprite / player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
        player2 = pygame.image.load('Graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player1, player2]
        self.player_jump = pygame.image.load('Graphics/player/jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity -= 20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk [int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

#sprite / obstacles
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly1 = pygame.image.load('Graphics/fly/fly1.png').convert_alpha()
            fly2 = pygame.image.load('Graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
            

        else:
            snail1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300
            
        self.index = 0
        self.image = self.frames[self.index]
        starting_x = randint(900,1100)
        self.rect = self.image.get_rect(midbottom = (starting_x, y_pos))

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
     
    def update(self):
        self.animation()
        self.rect.x -= 6
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()



#setup
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
music = pygame.mixer.Sound('Audio/music.wav')

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
obstacle_group = pygame.sprite.Group()

#player
player = pygame.sprite.GroupSingle()
player.add(Player())


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

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

while True:
    #listening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['fly', 'snail', 'snail', 'snail'])))

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
        music.set_volume(0.1)
        music.play(loops = -1)
        # draw elements
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()

        #player
        player.draw(screen)
        player.update()

        #obstacles group
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()


    else:
        music.set_volume(0)
        
        screen.fill((94,129,162))
        screen.blit(poster, poster_rect)
        screen.blit(name, name_rect)
        obstacle_list.clear()
        gravity = 0

        score_message = text_font.render(f'Your score is: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            screen.blit(message, message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        

    pygame.display.update()
    clock.tick(60)