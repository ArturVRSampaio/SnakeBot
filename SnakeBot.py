from Structures.ExplorationNode import ExplorationNode
from Structures.UniqueStack import UniqueStack
from Utils import *
import math
from collections import deque
import copy


class SnakeBot:

    def decide_dfs(self, snake, food):
        stack = UniqueStack()
        stack.push(ExplorationNode(snake))

        while stack.has_not_discarted_items():
            node = stack.get_last_not_discarded_item()

            if is_game_over(node.snake) or node.is_explored():
                node.discard()
            elif snake_ate_the_food(node.snake, food):
                node.explore()
                path = []

                while node.parent:
                    path.append(node.snake.direction)
                    node = node.parent

                print(path)
                return path
            else:
                node.explore()
                new_nodes = []
                for direction in DIRECTIONS:
                    new_snake = copy.deepcopy(node.snake)
                    new_snake.direction = direction
                    new_snake.move()

                    new_node = ExplorationNode(new_snake, node)
                    new_node = stack.push(new_node)
                    new_nodes.append(new_node)
                has_only_discarted_childs = True
                for node in new_nodes:
                    if not node.is_discarded():
                        has_only_discarted_childs = False

                if has_only_discarted_childs:
                    node.discard()

        return snake.direction

    def decide_bfs(self, snake, food):
        queue = []

        return snake.direction

    def decide_with_distance(self, snake, food):
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

    def decide_by_side(self, snake, food):
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
