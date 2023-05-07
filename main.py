import random
import pygame
import time
from pygame.locals import *
import json

window_width = 600
window_height = 499

window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
game_over_text = False
red_frame = False
welcome = True
pipeimage = 'images/pipe.png'
background_image = 'images/background.jpg'
birdplayer_image = 'images/bird.png'
sealevel_image = 'images/base.jfif'
companion_image = 'images/companion.png'
your_score = 0
high_score = 0


def flappygame():
    global your_score
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    mytempheight = 100
    your_score = 0
    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()
    down_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width + 300 - mytempheight + (window_width / 2),
         'y': second_pipe[1]['y']},
    ]
    up_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width + 200 - mytempheight + (window_width / 2),
         'y': second_pipe[0]['y']},
    ]
    # pipe velocity along x
    pipeVelX = -4
    # bird velocity
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1

    bird_flap_velocity = -8
    bird_flapped = False

    game_active = True

    cur_text = ''

    while game_active:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                game_active = False
            if (event.type == KEYDOWN and event.key == K_SPACE) or (event.type == MOUSEBUTTONUP and event.button == 1):

                if vertical > 0:
                    pygame.mixer.music.load('images/swoosh.wav')
                    pygame.mixer.music.play(1)
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)

        if game_over:
            global game_over_text, red_frame
            game_over_text = True
            red_frame = True

            global high_score
            
            if your_score > high_score:
                high_score = your_score
                data = {"high_score": high_score}
                with open('data.json', 'w') as f:
                    json.dump(data, f)

            pygame.mixer.music.load('images/hit.wav')
            pygame.mixer.music.play(1)
            return

        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                # print(f"Your your_score is {your_score}")

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        pygame.draw.circle(window, (255, 255, 255), (horizontal + 20, vertical + 12), 15)
        window.blit(game_images['flappybird'], (horizontal, vertical))

        if 0 <= your_score % 5 < 2 and your_score > 4:
            bird_font = pygame.font.SysFont('Comic Sans MS', 20)
            txt = bird_font.render('Thanks!', False, (0, 0, 0))
            window.blit(txt, (horizontal + 10, vertical + 20))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        window.blit(game_images['companion'], (125, 400))

        if your_score % 5 == 0 and your_score != 0 and cur_text == '':
            game_font = pygame.font.SysFont('Comic Sans MS', 16)
            lst = [
                'You are doing great! Keep it up!',
                'Wonderful! You are gonna beat record!',
                'Good playing! Go on',
                'Show great game!',
                'Awesome!'
            ]
            cur_text = random.choice(lst)
        if your_score % 5 == 2 and cur_text != '':
            cur_text = ''

        game_font = pygame.font.SysFont('Comic Sans MS', 10)
        text_surface = game_font.render(cur_text, False, (0, 0, 0))
        window.blit(text_surface, (65, 430))

        game_font = pygame.font.SysFont('Comic Sans MS', 10)
        text = game_font.render('x: 125, y:' + str(vertical), False, (0, 0, 0))
        window.blit(text, (30, 60))
        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)




def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and \
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False


def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},

        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == '__main__':
    f = open('data.json')
    data = json.load(f)
    high_score = data['high_score']
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    programIcon = pygame.image.load('images/bird.png')
    pygame.display.set_icon(programIcon)

    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                                pygame.image.load(pipeimage).convert_alpha())
    game_images['companion'] = pygame.transform.scale(pygame.image.load(companion_image).convert_alpha(), (40, 35))

    # Here starts the main game
    active = True
    while active:
        # sets the coordinates of flappy bird
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
        ground = 0

        while active:

            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    active = False

                # If the user presses space or
                # up key, start the game for them
                elif (event.type == KEYDOWN and event.key == K_SPACE) or (
                        event.type == MOUSEBUTTONUP and event.button == 1):
                    flappygame()


                # if user doesn't press any key Nothing happen
                else:

                    window.blit(game_images['background'], (0, 0))
                    if game_over_text:
                        pygame.draw.circle(window, (255, 255, 255), (horizontal + 20, vertical + 12), 10)
                    window.blit(game_images['flappybird'],
                                (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))
                    if game_over_text:
                        game_font = pygame.font.SysFont('Comic Sans MS', 16)
                        text_surface = game_font.render('Good attempt! Next will be better!', False,
                                                        (0, 0, 0))
                        window.blit(text_surface, (65, 430))
                    else:
                        game_font = pygame.font.SysFont('Comic Sans MS', 16)
                        text_surface = game_font.render('Hello, my name is Skyler! I am your bird-companion', False,
                                                        (0, 0, 0))
                        text_surface2 = game_font.render(
                            'You need to avoid obstacles. To jump just press space or right-click', False, (0, 0, 0))
                        text_surface3 = game_font.render(
                            'Passing pipe gives you a score and goal is to fly as far as possible', False, (0, 0, 0))
                        window.blit(text_surface, (65, 430))
                        window.blit(text_surface2, (65, 450))
                        window.blit(text_surface3, (65, 470))
                    window.blit(game_images['companion'], (125, 400))

                    game_font = pygame.font.SysFont('Comic Sans MS', 26)
                    text_surface = game_font.render('Your max score: ' + str(high_score), False, (0, 0, 0))
                    window.blit(text_surface, (int(window_width / 2) - 300, 0))

                    game_font = pygame.font.SysFont('Comic Sans MS', 26)
                    text_surface = game_font.render('Last score: ' + str(your_score), False, (0, 0, 0))
                    window.blit(text_surface, (int(window_width / 2) + 100, 0))

                    pygame.display.update()

                    framepersecond_clock.tick(framepersecond)

                    time.sleep(0.1)

    pygame.quit()
