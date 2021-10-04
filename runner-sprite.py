import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):  # inherates from pygame.sprite.Sprite
    def __init__(self):
        super().__init__()  # inherate sprite class inside itself. #Needs 2 attributes at minimum
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]  # ALWAYS NEEDED
        self.rect = self.image.get_rect(midbottom=(80, 300))  # ALWAYS NEEDED
        self.gravity = 0  # player.gravity

        #Sound
        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.2)

    # Player Jump
    def player_input(self):  # player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  # player.rect.bottom
            self.gravity = -20  # player.gravity
            self.jump_sound.play()

    # Gavity
    def apply_gravity(self):  # player
        self.gravity += 1  # player.gravity
        self.rect.y += self.gravity  # player.rect.y / player.gravity
        if self.rect.bottom >= 300:  # player.rect.bottom
            self.rect.bottom = 300  # player.rect.bottom

    # Animation
    def animation_state(self):
        # Play walking animation if on floor, jump when not on floor
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1  # Increas walk picture change slowly
            # If the index gets to 1, reset index to 0
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    # Update
    def update(self):  # player
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):  # inherates from pygame.sprite.Sprite
    def __init__(self, type):  # Type of obsticle.  Fly or Snail
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]  # fly_frames
            y_pos = 210  # y_pos of fly
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]  # snail_frames
            y_pos = 300  # Ground possition

        self.animation_index = 0
        self.image = self.frames[self.animation_index]  # ALWAYS NEEDED
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))  # ALWAYS NEEDED

    # Animation State
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # Update
    def update(self):
        self.animation_state()  # Call animation_state def
        self.rect.x -= 6  # Subtract 6px every update
        self.destroy()

    # Remove extra
    def destroy(self):
        if self.rect.x <= -100:  # If the X axis is greater than -100
            self.kill()  # Destroys Obstacle sprite


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  # in milliseconds
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite(): # sprite, group, bool
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True



""" Frames Per Second Math: 1 frame/second > (10px/s * 1fps) = 10px/s """
# In Pygame, the Origin point is the Top Left at 0,0
# To go right from the top left, increase X, to go down, increase Y
pygame.init()  # Initialize everything

screen = pygame.display.set_mode((800, 400))  # ((width,height))
pygame.display.set_caption("Runner")  # Window Title Bar
clock = pygame.time.Clock()  # Capital 'C' in Clock
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # Font type, Font size
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.set_volume(0.3)
bg_Music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()  # Group Player class into Single instance
player.add(Player())

obstacle_group = pygame.sprite.Group()


""" Surfaces: Display Surface (game window), Regular Surface (any images) """
sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()  # converts image for pygame to handle better
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
# score_surf = test_font.render("My Game", False, (64,64,64)).convert_alpha() #text ino, AA, color


# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.scale(player_stand,(200,200)) #Scale Player
# player_stand = pygame.transform.scale2x(player_stand) #Scale Player
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Game Name
game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press SPACE to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(410, 330))

# Event Timer
# Add +1 to every event to avoid errors with events 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

####################################################################################################
""" Game While-Loop """
while True:  # draw all elements
    for event in pygame.event.get():  # Check for a specific event
        if event.type == pygame.QUIT:  # If someone has clicked the upper X to close the window
            pygame.quit()  # Close the window, unintialize everything
            exit()  # from sys.exit, stops the graphic error message

        if game_active:
            if event.type == obstacle_timer:
                # calling Obstacle class and type of obstacle
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:  # If game_active is True, run the code below
        # blit draws variable on surface at stated coordinates
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))  # Over 0, Down 300
        score = display_score()

        player.draw(screen)  # Specify 1 argument, what surface to draw on
        player.update()  # update sprite

        obstacle_group.draw(screen)
        obstacle_group.update()  # update sprite

        game_active= collision_sprite() # Collision

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
 
        score_message = test_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(410, 330))
        screen.blit(game_name, game_name_rect)

            # If score is 0, display start message
        if score == 0: screen.blit(game_message, game_message_rect)
            # If score not 0, display score
        else: screen.blit(score_message, score_message_rect)


    pygame.display.update()  # update everything
    clock.tick(60)  # Tells the game not to run faster than 60 FPS