import random


from Constants import *


def is_game_over(snake):
    head = snake.head()
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    elif head in snake.segments[1:]:
        return True

    return False


def snake_ate_the_food(snake, food):
    head_x, head_y = snake.head()
    food_x, food_y = food
    return head_x == food_x and head_y == food_y


def new_food_position() -> tuple[int, int]:
    return random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
