import sys

import pygame

from Constants import *
from Snake import Snake
from SnakeBot import SnakeBot
from Utils import new_food_position, snake_ate_the_food, is_game_over


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.snake = Snake()
        self.food = new_food_position()
        self.score = 0
        self.clock = pygame.time.Clock()
        self.snakeBot = SnakeBot()

    def draw_food(self, food, screen):
        pygame.draw.rect(screen, WHITE,
                         (food[0] * GRID_SIZE - 1, food[1] * GRID_SIZE - 1, GRID_SIZE - 1, GRID_SIZE - 1))

    def draw_snake_body(self, snake, screen):
        for key, segment in enumerate(snake.segments):
            pygame.draw.rect(screen, GREEN,
                             (segment[0] * GRID_SIZE - 1, segment[1] * GRID_SIZE - 1, GRID_SIZE - 1, GRID_SIZE - 1))
            if key == 0:
                pygame.draw.rect(screen, RED,
                                 (segment[0] * GRID_SIZE - 1, segment[1] * GRID_SIZE - 1, GRID_SIZE - 1, GRID_SIZE - 1))

    def human_controls(self):
        key_processed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            elif event.type == pygame.KEYDOWN and not key_processed:
                if event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.direction = RIGHT
                key_processed = True

    def game_over(self):
        pygame.quit()
        sys.exit()

    def start_game(self):
        self.screen.fill(BLACK)
        self.draw_snake_body(self.snake, self.screen)
        self.draw_food(self.food, self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over()

            self.snake.direction = self.snakeBot.smart_decide(self.snake, self.food)

            self.snake.move()

            if snake_ate_the_food(self.snake, self.food):
                self.snake.add_segment()
                self.score += 1
                self.food = new_food_position()

            if is_game_over(self.snake):
                self.game_over()

            self.screen.fill(BLACK)
            self.draw_snake_body(self.snake, self.screen)
            self.draw_food(self.food, self.screen)
            pygame.display.flip()

            self.clock.tick(10)  # Control the frame rate

