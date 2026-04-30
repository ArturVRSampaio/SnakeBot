from unittest.mock import patch

from snakebot.snake import Snake
from snakebot.bot import SnakeBot, _manhattan_distance, _euclidean_distance, _chebyshev_distance, _HAMILTONIAN_PATH, _HAMILTONIAN_INDEX
from snakebot.constants import RIGHT, LEFT, UP, DOWN, GRID_WIDTH, GRID_HEIGHT
from snakebot.utils import will_snake_eat_the_food, new_food_position


def _snake_at(x, y):
    s = Snake()
    s.segments = [(x, y)]
    return s


class TestDecide:
    def setup_method(self):
        self.bot = SnakeBot()
        self.snake = _snake_at(10, 10)
        self.food = (15, 10)

    def test_dfs_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "dfs"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_bfs_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "bfs"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_distance_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "distance"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert result[0] in [UP, DOWN, LEFT, RIGHT]

    def test_greedy_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "greedy"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert result[0] in [UP, DOWN, LEFT, RIGHT]

    def test_iddfs_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "iddfs"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_bidirectional_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "bidirectional"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_hamiltonian_strategy_returns_list(self):
        with patch("snakebot.bot.STRATEGY", "hamiltonian"):
            result = self.bot.decide(self.snake, self.food)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_invalid_strategy_raises(self):
        import pytest
        with patch("snakebot.bot.STRATEGY", "unknown"):
            with pytest.raises(ValueError, match="Unknown strategy"):
                self.bot.decide(self.snake, self.food)


class TestDistanceFunctions:
    def test_manhattan_same_point(self):
        assert _manhattan_distance((5, 5), (5, 5)) == 0

    def test_manhattan_horizontal(self):
        assert _manhattan_distance((0, 0), (3, 0)) == 3

    def test_manhattan_diagonal(self):
        assert _manhattan_distance((0, 0), (3, 4)) == 7

    def test_euclidean_same_point(self):
        assert _euclidean_distance((5, 5), (5, 5)) == 0.0

    def test_euclidean_known(self):
        assert _euclidean_distance((0, 0), (3, 4)) == 5.0

    def test_chebyshev_same_point(self):
        assert _chebyshev_distance((5, 5), (5, 5)) == 0

    def test_chebyshev_diagonal(self):
        assert _chebyshev_distance((0, 0), (3, 4)) == 4


class TestDecideBySide:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_moves_right_toward_food(self):
        assert self.bot.decide_by_side(_snake_at(10, 10), (15, 10)) == RIGHT

    def test_moves_left_toward_food(self):
        assert self.bot.decide_by_side(_snake_at(10, 10), (5, 10)) == LEFT

    def test_moves_up_toward_food(self):
        assert self.bot.decide_by_side(_snake_at(10, 10), (10, 5)) == UP

    def test_moves_down_toward_food(self):
        assert self.bot.decide_by_side(_snake_at(10, 10), (10, 15)) == DOWN

    def test_survival_right_when_optimal_blocked(self):
        snake = _snake_at(10, 10)
        assert self.bot.decide_by_side(snake, (10, 10)) == RIGHT

    def test_survival_left_when_right_is_wall(self):
        snake = _snake_at(39, 10)
        assert self.bot.decide_by_side(snake, (39, 10)) == LEFT

    def test_survival_up_when_right_and_left_blocked(self):
        snake = Snake()
        snake.segments = [(39, 10), (38, 10), (38, 9)]
        assert self.bot.decide_by_side(snake, (39, 10)) == UP

    def test_survival_down_when_right_left_up_blocked(self):
        snake = Snake()
        snake.segments = [(39, 0), (38, 0), (39, 1)]
        assert self.bot.decide_by_side(snake, (39, 0)) == DOWN

    def test_no_choice_returns_current_direction(self):
        snake = Snake()
        snake.segments = [(0, 0), (1, 0), (0, 1), (5, 5)]
        assert self.bot.decide_by_side(snake, (15, 15)) == snake.direction


class TestDecideWithDistance:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_returns_a_direction(self):
        direction = self.bot.decide_with_distance(_snake_at(10, 10), (15, 10))
        assert direction in [UP, DOWN, LEFT, RIGHT]

    def test_moves_toward_food(self):
        direction = self.bot.decide_with_distance(_snake_at(10, 10), (15, 10))
        assert direction == RIGHT

    def test_avoids_wall(self):
        snake = _snake_at(0, 10)
        direction = self.bot.decide_with_distance(snake, (0, 15))
        assert direction != LEFT

    def test_returns_current_direction_when_all_moves_fatal(self):
        snake = Snake()
        snake.segments = [(0, 0), (1, 0), (0, 1), (5, 5)]
        assert self.bot.decide_with_distance(snake, (15, 15)) == snake.direction


class TestDecideBfs:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_render_callback_is_called(self):
        calls = []
        self.bot.decide_bfs(_snake_at(10, 10), (15, 10), render_callback=lambda s: calls.append(s))
        assert len(calls) > 0

    def test_render_callback_receives_snake(self):
        snakes = []
        self.bot.decide_bfs(_snake_at(10, 10), (11, 10), render_callback=lambda s: snakes.append(s))
        assert all(hasattr(s, "segments") for s in snakes)

    def test_returns_list(self):
        path = self.bot.decide_bfs(_snake_at(10, 10), (15, 10))
        assert isinstance(path, list)
        assert len(path) > 0

    def test_finds_adjacent_food_right(self):
        path = self.bot.decide_bfs(_snake_at(10, 10), (11, 10))
        assert path == [RIGHT]

    def test_finds_adjacent_food_down(self):
        path = self.bot.decide_bfs(_snake_at(10, 10), (10, 11))
        assert path == [DOWN]

    def test_path_leads_to_food(self):
        snake = _snake_at(10, 10)
        food = (13, 10)
        path = self.bot.decide_bfs(snake, food)

        for direction in reversed(path):
            snake.direction = direction
            snake.move()

        assert will_snake_eat_the_food(snake, food)

    def test_finds_shortest_path(self):
        snake = _snake_at(10, 10)
        food = (13, 10)  # 3 steps right
        path = self.bot.decide_bfs(snake, food)
        assert len(path) == 3

    def test_head_already_at_food_uses_decide_by_side_fallback(self):
        snake = _snake_at(10, 10)
        path = self.bot.decide_bfs(snake, (10, 10))
        assert len(path) == 1
        assert path[0] in [UP, DOWN, LEFT, RIGHT]

    def test_returns_direction_when_trapped(self):
        snake = Snake()
        snake.segments = [
            (1, 1),
            (0, 1), (0, 0), (1, 0), (2, 0),
            (2, 1), (2, 2), (1, 2), (0, 2),
        ]
        path = self.bot.decide_bfs(snake, (5, 5))
        assert isinstance(path, list)
        assert len(path) > 0


class TestDecideDfs:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_render_callback_is_called(self):
        calls = []
        self.bot.decide_dfs(_snake_at(10, 10), (15, 10), render_callback=lambda s: calls.append(s))
        assert len(calls) > 0

    def test_render_callback_receives_snake(self):
        snakes = []
        self.bot.decide_dfs(_snake_at(10, 10), (11, 10), render_callback=lambda s: snakes.append(s))
        assert all(hasattr(s, "segments") for s in snakes)

    def test_returns_list(self):
        path = self.bot.decide_dfs(_snake_at(10, 10), (15, 10))
        assert isinstance(path, list)
        assert len(path) > 0

    def test_finds_adjacent_food_right(self):
        snake = _snake_at(10, 10)
        path = self.bot.decide_dfs(snake, (11, 10))
        assert path == [RIGHT]

    def test_finds_adjacent_food_down(self):
        snake = _snake_at(10, 10)
        path = self.bot.decide_dfs(snake, (10, 11))
        assert path == [DOWN]

    def test_path_leads_to_food(self):
        snake = _snake_at(10, 10)
        food = (13, 10)
        path = self.bot.decide_dfs(snake, food)

        for direction in reversed(path):
            snake.direction = direction
            snake.move()

        assert will_snake_eat_the_food(snake, food)

    def test_head_already_at_food_uses_decide_by_side_fallback(self):
        snake = _snake_at(10, 10)
        path = self.bot.decide_dfs(snake, (10, 10))
        assert len(path) == 1
        assert path[0] in [UP, DOWN, LEFT, RIGHT]

    def test_returns_direction_when_trapped(self):
        snake = Snake()
        snake.segments = [
            (1, 1),
            (0, 1), (0, 0), (1, 0), (2, 0),
            (2, 1), (2, 2), (1, 2), (0, 2),
        ]
        path = self.bot.decide_dfs(snake, (5, 5))
        assert isinstance(path, list)
        assert len(path) > 0


class TestDecideHamiltonian:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_returns_valid_direction(self):
        direction = self.bot.decide_hamiltonian(_snake_at(0, 0))
        assert direction in [UP, DOWN, LEFT, RIGHT]

    def test_moves_right_on_first_row(self):
        assert self.bot.decide_hamiltonian(_snake_at(0, 0)) == RIGHT
        assert self.bot.decide_hamiltonian(_snake_at(5, 0)) == RIGHT

    def test_moves_left_on_second_row(self):
        assert self.bot.decide_hamiltonian(_snake_at(GRID_WIDTH - 1, 1)) == LEFT
        assert self.bot.decide_hamiltonian(_snake_at(5, 1)) == LEFT

    def test_moves_down_at_end_of_even_row(self):
        assert self.bot.decide_hamiltonian(_snake_at(GRID_WIDTH - 1, 0)) == DOWN

    def test_moves_down_at_end_of_odd_row(self):
        # Row 1 (odd) ends at (1,1); next is (1,2)
        assert self.bot.decide_hamiltonian(_snake_at(1, 1)) == DOWN

    def test_column_0_returns_up_to_start(self):
        # Column 0 is the return spine; (0,1) is the last cell before cycle closes
        assert self.bot.decide_hamiltonian(_snake_at(0, 1)) == UP

    def test_last_cell_adjacent_to_first_cell(self):
        last = _HAMILTONIAN_PATH[-1]
        first = _HAMILTONIAN_PATH[0]
        assert abs(last[0] - first[0]) + abs(last[1] - first[1]) == 1

    def test_path_covers_all_cells(self):
        assert len(_HAMILTONIAN_PATH) == GRID_WIDTH * GRID_HEIGHT

    def test_path_has_no_duplicate_cells(self):
        assert len(set(_HAMILTONIAN_PATH)) == len(_HAMILTONIAN_PATH)

    def test_index_matches_path(self):
        for pos, idx in _HAMILTONIAN_INDEX.items():
            assert _HAMILTONIAN_PATH[idx] == pos

    def test_consecutive_cells_are_adjacent(self):
        for i in range(len(_HAMILTONIAN_PATH) - 1):
            x0, y0 = _HAMILTONIAN_PATH[i]
            x1, y1 = _HAMILTONIAN_PATH[i + 1]
            assert abs(x1 - x0) + abs(y1 - y0) == 1


class TestDecideIDDFS:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_returns_list(self):
        path = self.bot.decide_iddfs(_snake_at(10, 10), (15, 10))
        assert isinstance(path, list)
        assert len(path) > 0

    def test_finds_adjacent_food_right(self):
        assert self.bot.decide_iddfs(_snake_at(10, 10), (11, 10)) == [RIGHT]

    def test_finds_adjacent_food_down(self):
        assert self.bot.decide_iddfs(_snake_at(10, 10), (10, 11)) == [DOWN]

    def test_finds_shortest_path(self):
        path = self.bot.decide_iddfs(_snake_at(10, 10), (13, 10))
        assert len(path) == 3

    def test_path_leads_to_food(self):
        snake = _snake_at(10, 10)
        food = (13, 10)
        path = self.bot.decide_iddfs(snake, food)
        for direction in reversed(path):
            snake.direction = direction
            snake.move()
        assert will_snake_eat_the_food(snake, food)

    def test_head_already_at_food_uses_decide_by_side_fallback(self):
        path = self.bot.decide_iddfs(_snake_at(10, 10), (10, 10))
        assert len(path) == 1
        assert path[0] in [UP, DOWN, LEFT, RIGHT]

    def test_returns_direction_when_trapped(self):
        snake = Snake()
        snake.segments = [
            (1, 1),
            (0, 1), (0, 0), (1, 0), (2, 0),
            (2, 1), (2, 2), (1, 2), (0, 2),
        ]
        path = self.bot.decide_iddfs(snake, (5, 5))
        assert isinstance(path, list)
        assert len(path) > 0

    def test_render_callback_is_called(self):
        calls = []
        self.bot.decide_iddfs(_snake_at(10, 10), (11, 10), render_callback=lambda s: calls.append(s))
        assert len(calls) > 0


class TestDecideBidirectionalBFS:
    def setup_method(self):
        self.bot = SnakeBot()

    def test_returns_list(self):
        path = self.bot.decide_bidirectional_bfs(_snake_at(10, 10), (15, 10))
        assert isinstance(path, list)
        assert len(path) > 0

    def test_finds_adjacent_food_right(self):
        path = self.bot.decide_bidirectional_bfs(_snake_at(10, 10), (11, 10))
        assert path == [RIGHT]

    def test_finds_adjacent_food_down(self):
        path = self.bot.decide_bidirectional_bfs(_snake_at(10, 10), (10, 11))
        assert path == [DOWN]

    def test_finds_shortest_path(self):
        path = self.bot.decide_bidirectional_bfs(_snake_at(10, 10), (13, 10))
        assert len(path) == 3

    def test_path_leads_to_food(self):
        snake = _snake_at(10, 10)
        food = (13, 10)
        path = self.bot.decide_bidirectional_bfs(snake, food)
        for direction in reversed(path):
            snake.direction = direction
            snake.move()
        assert will_snake_eat_the_food(snake, food)

    def test_head_already_at_food_uses_decide_by_side_fallback(self):
        path = self.bot.decide_bidirectional_bfs(_snake_at(10, 10), (10, 10))
        assert len(path) == 1
        assert path[0] in [UP, DOWN, LEFT, RIGHT]

    def test_render_callback_is_called(self):
        calls = []
        self.bot.decide_bidirectional_bfs(
            _snake_at(10, 10), (15, 10), render_callback=lambda s: calls.append(s)
        )
        assert len(calls) > 0
