from Utils import *
import math
from collections import deque
import copy


class SnakeBot:

    def decide_bfs(self, snake, food):

        queue = deque([(snake, [])])

        while queue:
            current_snake, path = queue.popleft()

            if snake_ate_the_food(current_snake, food):
                return path[0] if path else current_snake.direction

            for direction in DIRECTIONS:
                new_snake = copy.deepcopy(current_snake)
                new_snake.direction = direction
                new_snake.move()

                if not is_game_over(new_snake):
                    new_path = path + [direction]
                    queue.append((new_snake, new_path))

        return snake.direction

    def smart_decide(self, snake, food):
        paths = []
        for direction in DIRECTIONS:
            new_snake = copy.deepcopy(snake)
            new_snake.direction = direction
            new_snake.move()
            if not is_game_over(new_snake):
                paths.append([new_snake.direction, _manhattan_distance(new_snake.head(), food)])

        # already dead
        if not paths:
            return snake.direction

        paths = sorted(paths, key=lambda x: x[1])
        return paths[0][0]

    def simple_decide(self, snake, food):
        head_x, head_y = snake.head()
        food_x, food_y = food

        snake_up = copy.deepcopy(snake)
        snake_up.direction = UP
        snake_up.move()

        snake_down = copy.deepcopy(snake)
        snake_down.direction = DOWN
        snake_down.move()

        snake_left = copy.deepcopy(snake)
        snake_left.direction = LEFT
        snake_left.move()

        snake_right = copy.deepcopy(snake)
        snake_right.direction = RIGHT
        snake_right.move()

        # optimal movement
        if head_x < food_x and not is_game_over(snake_right):
            return RIGHT
        if head_x > food_x and not is_game_over(snake_left):
            return LEFT
        if head_y > food_y and not is_game_over(snake_up):
            return UP
        if head_y < food_y and not is_game_over(snake_down):
            return DOWN

        # survival movement
        if not is_game_over(snake_right):
            return RIGHT
        if not is_game_over(snake_left):
            return LEFT
        if not is_game_over(snake_up):
            return UP
        if not is_game_over(snake_down):
            return DOWN

        # no choice
        return snake.direction


def _manhattan_distance(head, food):
    head_x, head_y = head
    food_x, food_y = food
    return abs(head_x - food_x) + abs(head_y - food_y)


def _euclidean_distance(head, food):
    x1, y1 = head
    x2, y2 = food
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def _chebyshev_distance(head, food):
    x1, y1 = head
    x2, y2 = food
    return max(abs(x1 - x2), abs(y1 - y2))
