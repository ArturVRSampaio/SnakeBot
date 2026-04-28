from snakebot.snake import Snake
from snakebot.constants import RIGHT, LEFT, UP, DOWN, GRID_WIDTH, GRID_HEIGHT


def test_initial_position():
    snake = Snake()
    assert snake.segments == [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]


def test_initial_direction():
    snake = Snake()
    assert snake.direction == RIGHT


def test_initial_not_eaten():
    snake = Snake()
    assert snake.eaten is False


def test_head_returns_first_segment():
    snake = Snake()
    snake.segments = [(5, 3), (4, 3)]
    assert snake.head() == (5, 3)


def test_move_right():
    snake = Snake()
    snake.segments = [(10, 10)]
    snake.direction = RIGHT
    snake.move()
    assert snake.head() == (11, 10)
    assert len(snake.segments) == 1


def test_move_left():
    snake = Snake()
    snake.segments = [(10, 10)]
    snake.direction = LEFT
    snake.move()
    assert snake.head() == (9, 10)


def test_move_up():
    snake = Snake()
    snake.segments = [(10, 10)]
    snake.direction = UP
    snake.move()
    assert snake.head() == (10, 9)


def test_move_down():
    snake = Snake()
    snake.segments = [(10, 10)]
    snake.direction = DOWN
    snake.move()
    assert snake.head() == (10, 11)


def test_grow_after_eating():
    snake = Snake()
    snake.segments = [(10, 10)]
    snake.add_segment()
    snake.move()
    assert len(snake.segments) == 2
    assert snake.eaten is False


def test_no_grow_without_eating():
    snake = Snake()
    snake.segments = [(10, 10)]
    snake.move()
    assert len(snake.segments) == 1


def test_tail_dropped_when_not_eaten():
    snake = Snake()
    snake.segments = [(10, 10), (9, 10), (8, 10)]
    snake.direction = RIGHT
    snake.move()
    assert snake.segments == [(11, 10), (10, 10), (9, 10)]
