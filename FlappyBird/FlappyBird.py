import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports
import random


# Global Variables for the game
FPS = 60
scr_width =  288
scr_height = 512
display_screen_window = pygame.display.set_mode((scr_width, scr_height))
play_ground = scr_height * 0.8
game_image = {}
game_audio_sound = {}
player = 'sprites/bird.png'
bcg_image = 'sprites/background.png'
pipe_image = 'sprites/pipe.png'
bird_color = random.choice(['red', 'blue', 'yellow'])
num = random.randint(1,3)

# Bird Class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0        
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'sprites/Grumpy/{bird_color}{num}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0


    def update(self):
        # Handle Animation
        self.counter += 1
        flap_cooldown = 5


        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(60, int(512 / 2))

bird_group.add(flappy)


def welcome_main_screen():
    """
    Shows welcome images on the screen
    """
    ground_scroll = 0
    scroll_speed = 2
    

    while True:
        # Game FPS
        time_clock.tick(FPS)
        
        display_screen_window.blit(game_image['background'], (0, 0))
        display_screen_window.blit(game_image['message'], (55, 65))
        display_screen_window.blit(game_image['base'], (ground_scroll, 408))
                
        # Move ground right to left 
        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 23:
            ground_scroll = 0
                
        # Draw bird
        bird_group.draw(display_screen_window)
        bird_group.update()
        
        
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            

        pygame.display.update()


def main_gameplay():
    score = 0
    p_x = int(scr_width / 5)
    p_y = int(scr_width / 2)
    b_x = 0

    ground_scroll = 0
    scroll_speed = 2
    

    n_pip1 = get_Random_Pipes()
    n_pip2 = get_Random_Pipes()


    up_pips = [
        {'x': scr_width + 200, 'y': n_pip1[0]['y']},
        {'x': scr_width + 200 + (scr_width / 2), 'y': n_pip2[0]['y']},
    ]

    low_pips = [
        {'x': scr_width + 200, 'y': n_pip1[1]['y']},
        {'x': scr_width + 200 + (scr_width / 2), 'y': n_pip2[1]['y']},
    ]

    pip_Vx = -4

    p_vx = -9
    p_mvx = 10
    p_mvy = -8
    p_accuracy = 1

    p_flap_accuracy = -8
    p_flap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if p_y > 0:
                    p_vx = p_flap_accuracy
                    p_flap = True
                    game_audio_sound['wing'].play()

        cr_tst = is_Colliding(p_x, p_y, up_pips,
                              low_pips)
        if cr_tst:
            return


        p_middle_positions = p_x + game_image['player'].get_width() / 2
        for pipe in up_pips:
            pip_middle_positions = pipe['x'] + game_image['pipe'][0].get_width() / 2
            if pip_middle_positions <= p_middle_positions < pip_middle_positions + 4:
                score += 1
                print(f"Your score is {score}")
                game_audio_sound['point'].play()

        if p_vx < p_mvx and not p_flap:
            p_vx += p_accuracy

        if p_flap:
            p_flap = False
        p_height = game_image['player'].get_height()
        p_y = p_y + min(p_vx, play_ground - p_y - p_height)


        for pip_upper, pip_lower in zip(up_pips, low_pips):
            pip_upper['x'] += pip_Vx
            pip_lower['x'] += pip_Vx


        if 0 < up_pips[0]['x'] < 5:
            new_pip = get_Random_Pipes()
            up_pips.append(new_pip[0])
            low_pips.append(new_pip[1])


        if up_pips[0]['x'] < -game_image['pipe'][0].get_width():
            up_pips.pop(0)
            low_pips.pop(0)


        display_screen_window.blit(game_image['background'], (0, 0))
        for pip_upper, pip_lower in zip(up_pips, low_pips):
            display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
            display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))

        display_screen_window.blit(game_image['base'], (ground_scroll, 408))
                
        # Move ground right to left 
        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 23:
            ground_scroll = 0
        
        # Draw Bird
        # bird_group.draw(display_screen_window)
        display_screen_window.blit(game_image['player'], (p_x, p_y))
        bird_group.update()
        
        d = [int(x) for x in list(str(score))]
        w = 0
        for digit in d:
            w += game_image['numbers'][digit].get_width()
        Xoffset = (scr_width - w) / 2

        for digit in d:
            display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.12))
            Xoffset += game_image['numbers'][digit].get_width()
        pygame.display.update()
        time_clock.tick(40)


def is_Colliding(p_x, p_y, up_pipes, low_pipes):
    if p_y > play_ground - 25 or p_y < 0:
        game_audio_sound['hit'].play()
        return True

    for pipe in up_pipes:
        pip_h = game_image['pipe'][0].get_height()
        if (p_y < pip_h + pipe['y'] and abs(p_x - pipe['x']) < game_image['pipe'][0].get_width()):
            game_audio_sound['hit'].play()
            return True

    for pipe in low_pipes:
        if (p_y + game_image['player'].get_height() > pipe['y']) and abs(p_x - pipe['x']) < \
                game_image['pipe'][0].get_width():
            game_audio_sound['hit'].play()
            return True

    return False


def get_Random_Pipes():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pip_h = game_image['pipe'][0].get_height()
    off_s = scr_height / 3
    yes2 = off_s + random.randrange(0, int(scr_height - game_image['base'].get_height() - 1.2 * off_s))
    pipeX = scr_width + 10
    y1 = pip_h - yes2 + off_s
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': yes2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":

    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    game_image['numbers'] = (
        pygame.image.load('sprites/num0.png').convert_alpha(),
        pygame.image.load('sprites/num1.png').convert_alpha(),
        pygame.image.load('sprites/num2.png').convert_alpha(),
        pygame.image.load('sprites/num3.png').convert_alpha(),
        pygame.image.load('sprites/num4.png').convert_alpha(),
        pygame.image.load('sprites/num5.png').convert_alpha(),
        pygame.image.load('sprites/num6.png').convert_alpha(),
        pygame.image.load('sprites/num7.png').convert_alpha(),
        pygame.image.load('sprites/num8.png').convert_alpha(),
        pygame.image.load('sprites/num9.png').convert_alpha(),
    )

    game_image['message'] = pygame.image.load('sprites/message.png').convert_alpha()
    game_image['base'] = pygame.image.load('sprites/base.png').convert_alpha()
    game_image['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180),
                          pygame.image.load(pipe_image).convert_alpha()
                          )

    # Game sounds
    game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audio_sound['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    game_audio_sound['point'] = pygame.mixer.Sound('sounds/point.wav')
    game_audio_sound['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    game_audio_sound['wing'] = pygame.mixer.Sound('sounds/wing.wav')

    game_image['background'] = pygame.image.load(bcg_image).convert()
    
    # bird_color = random.choice(['red', 'blue', 'yellow'])
    # num = random.randint(1,3)
    game_image['player'] = pygame.image.load(f'sprites/Grumpy/{bird_color}{num}.png')

    while True:
        welcome_main_screen()  # Shows welcome screen to the user until he presses a button
        main_gameplay()  # This is the main game function