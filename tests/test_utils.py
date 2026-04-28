from snakebot.snake import Snake
from snakebot.utils import is_game_over, will_snake_eat_the_food, new_food_position
from snakebot.constants import GRID_WIDTH, GRID_HEIGHT


def _snake_at(x, y):
    s = Snake()
    s.segments = [(x, y)]
    return s


def test_game_over_left_wall():
    assert is_game_over(_snake_at(-1, 10)) is True


def test_game_over_right_wall():
    assert is_game_over(_snake_at(GRID_WIDTH, 10)) is True


def test_game_over_top_wall():
    assert is_game_over(_snake_at(10, -1)) is True


def test_game_over_bottom_wall():
    assert is_game_over(_snake_at(10, GRID_HEIGHT)) is True


def test_game_over_self_collision():
    snake = Snake()
    snake.segments = [(10, 10), (11, 10), (10, 10)]
    assert is_game_over(snake) is True


def test_no_game_over_center():
    assert is_game_over(_snake_at(10, 10)) is False


def test_no_game_over_corners():
    for x, y in [(0, 0), (GRID_WIDTH - 1, 0), (0, GRID_HEIGHT - 1), (GRID_WIDTH - 1, GRID_HEIGHT - 1)]:
        assert is_game_over(_snake_at(x, y)) is False


def test_will_eat_food_true():
    snake = _snake_at(5, 5)
    assert will_snake_eat_the_food(snake, (5, 5)) is True


def test_will_eat_food_false_adjacent():
    snake = _snake_at(5, 5)
    assert will_snake_eat_the_food(snake, (6, 5)) is False
    assert will_snake_eat_the_food(snake, (5, 6)) is False


def test_new_food_within_bounds():
    for _ in range(50):
        x, y = new_food_position()
        assert 0 <= x < GRID_WIDTH
        assert 0 <= y < GRID_HEIGHT
