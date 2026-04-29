import sys

import pygame

from snakebot.constants import WIDTH, HEIGHT, GRID_SIZE, BLACK, WHITE, GREEN, RED, GHOST_GREEN, GHOST_RED, GAME_SPEED
from snakebot.snake import Snake
from snakebot.bot import SnakeBot
from snakebot.utils import new_food_position, will_snake_eat_the_food, is_game_over


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.snake = Snake()
        self.food = new_food_position(self.snake.segments)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.snakeBot = SnakeBot()

    def draw_food(self, food, screen):
        pygame.draw.rect(screen, WHITE,
                         (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    def draw_snake_body(self, snake, screen):
        for key, segment in enumerate(snake.segments):
            pygame.draw.rect(screen, GREEN,
                             (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
            if key == 0:
                pygame.draw.rect(screen, RED,
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    def draw_ghost_snake(self, snake, screen):
        for key, segment in enumerate(snake.segments):
            pygame.draw.rect(screen, GHOST_GREEN,
                             (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
            if key == 0:
                pygame.draw.rect(screen, GHOST_RED,
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    def _make_ghost_callback(self):
        last_render = [0]
        min_interval_ms = 1000 // 60

        def callback(ghost_snake):
            now = pygame.time.get_ticks()
            if now - last_render[0] < min_interval_ms:
                return
            last_render[0] = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over()

            self.screen.fill(BLACK)
            self.draw_snake_body(self.snake, self.screen)
            self.draw_food(self.food, self.screen)
            self.draw_ghost_snake(ghost_snake, self.screen)
            pygame.display.flip()

        return callback

    def game_over(self):
        pygame.quit()
        sys.exit()

    def start_game(self):
        self.screen.fill(BLACK)
        self.draw_snake_body(self.snake, self.screen)
        self.draw_food(self.food, self.screen)
        pygame.display.flip()

        directions = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over()

            if not directions:
                directions = self.snakeBot.decide(self.snake, self.food, self._make_ghost_callback())

            self.snake.direction = directions.pop()

            self.snake.move()

            if will_snake_eat_the_food(self.snake, self.food):
                self.snake.add_segment()
                self.score += 1
                self.food = new_food_position(self.snake.segments)
                self.screen.fill(BLACK)
                self.draw_snake_body(self.snake, self.screen)
                self.draw_food(self.food, self.screen)
                pygame.display.flip()
                directions = self.snakeBot.decide(self.snake, self.food, self._make_ghost_callback())

            if is_game_over(self.snake):
                self.game_over()

            self.screen.fill(BLACK)
            self.draw_snake_body(self.snake, self.screen)
            self.draw_food(self.food, self.screen)
            pygame.display.flip()

            self.clock.tick(GAME_SPEED)
