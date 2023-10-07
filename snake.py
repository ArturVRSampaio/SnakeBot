import pygame
import random
import sys
from pygame.locals import *

from SnakeBot import SnakeBot


def bite(snake_position):
    snake = list(snake_position)
    head = str(snake[0][0]) + str(snake[1][0])

    for x in range(1, len(snake) - 1):
        if str(snake[0][x]) + str(snake[1][x]) == str(head):
            return True
    return False


while True:
    restart = False

    control = SnakeBot()
    width = 600

    snake_position = [[280, 280, 280], [280, 260, 240]]

    dirs = last_direction = 1
    score = 0

    apple_position = [(random.randrange(0, width, 20)), (random.randrange(0, width, 20))]
    pygame.init()
    s = pygame.display.set_mode((width, width))
    pygame.display.set_caption('Snake')
    apple_image = pygame.Surface((19, 19))
    apple_image.fill((0, 255, 0))
    img = pygame.Surface((19, 19))
    img.fill((255, 0, 0))

    f = pygame.font.SysFont('Arial', 20)

    clock = pygame.time.Clock()

    while not restart:
        # print("loop")
        restart = False
        clock.tick(10)
        i = len(snake_position) - 1

        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit(0)

        if str(apple_position[0]) + str(apple_position[1]) == str(snake_position[0][0]) + str(snake_position[1][0]):
            score += 1
            snake_position.append(0)
            snake_position[0].append(0)
            snake_position[1].append(0)
            apple_position = [(random.randrange(0, width, 20)), (random.randrange(0, width, 20))]
        # print(apple_position)

        if bite(snake_position):
            print("bitten itself")
            restart = True

        if snake_position[0][0] < 0 or snake_position[0][0] > width or snake_position[1][0] < 0 or snake_position[1][
            0] > width:
            print("wall")
            restart = True

        i = len(snake_position)
        while i >= 1:
            snake_position[0][i] = snake_position[0][i - 1]
            snake_position[1][i] = snake_position[1][i - 1]
            i -= 1

        dirs = control.control(apple_position, snake_position, last_direction)

        last_direction = dirs

        if last_direction == 1:
            snake_position[1][0] += 20
        #	print("down")
        elif last_direction == 2:
            snake_position[1][0] -= 20
        #	print("up")
        elif last_direction == 3:
            snake_position[0][0] += 20
        #	print("right")
        elif last_direction == 6:
            snake_position[0][0] -= 20
        #	print("left")

        s.fill((0, 0, 0))

        for i in range(0, len(snake_position[0])):
            s.blit(img, (snake_position[0][i], snake_position[1][i]))

        s.blit(apple_image, (apple_position[0], apple_position[1]))
        t = f.render(str(score), True, (0, 255, 0))
        s.blit(t, (20, 20))
        pygame.display.update()
