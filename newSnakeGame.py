import pygame
import sys
import random
import copy

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:

    def __init__(self):
        self.segments = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.eaten = False  # Initialize the eaten flag

    def head(self):
        return self.segments[0]

    def add_segment(self):
        self.eaten = True  # Set the eaten flag to True

    def move(self):
        new_head = (self.head()[0] + self.direction[0], self.head()[1] + self.direction[1])
        self.segments.insert(0, new_head)
        if self.eaten:
            self.eaten = False
        else:
            self.segments.pop()


class SnakeBot:
    def decide(self, snake, food):
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


def game_over():
    pygame.quit()
    sys.exit()


def draw_food(food, screen):
    pygame.draw.rect(screen, WHITE,
                     (food[0] * GRID_SIZE - 1, food[1] * GRID_SIZE - 1, GRID_SIZE - 1, GRID_SIZE - 1))


def draw_snake_body(snake, screen):
    for key, segment in enumerate(snake.segments):
        pygame.draw.rect(screen, GREEN,
                         (segment[0] * GRID_SIZE - 1, segment[1] * GRID_SIZE - 1, GRID_SIZE - 1, GRID_SIZE - 1))
        if key == 0:
            pygame.draw.rect(screen, RED,
                             (segment[0] * GRID_SIZE - 1, segment[1] * GRID_SIZE - 1, GRID_SIZE - 1, GRID_SIZE - 1))


def new_food_position() -> tuple[int, int]:
    return random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)


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

    def human_controls(self):
        key_processed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
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

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over()

            self.snake.direction = self.snakeBot.decide(self.snake, self.food)

            self.snake.move()

            if snake_ate_the_food(self.snake, self.food):
                self.snake.add_segment()
                self.score += 1
                self.food = new_food_position()

            if is_game_over(self.snake):
                game_over()

            self.screen.fill(BLACK)
            draw_snake_body(self.snake, self.screen)
            draw_food(self.food, self.screen)
            pygame.display.flip()

            self.clock.tick(20)  # Control the frame rate


game = Game()
game.start_game()
