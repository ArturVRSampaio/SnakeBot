import random
import sys

import pygame

from Constants import *


def is_game_over(snake):
    head = snake.head()
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        print('hit the wall')
        return True
    elif head in snake.segments[1:]:
        print('bite itself')
        return True

    return False


def snake_ate_the_food(snake, food):
    return snake.head() == food


def new_food_position() -> tuple[int, int]:
    return random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
