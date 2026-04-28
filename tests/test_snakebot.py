from Snake import Snake
from SnakeBot import SnakeBot, _manhattan_distance, _euclidean_distance, _chebyshev_distance
from Constants import RIGHT, LEFT, UP, DOWN
from Utils import will_snake_eat_the_food


def _snake_at(x, y):
    s = Snake()
    s.segments = [(x, y)]
    return s


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
        # food at same position → all optimal checks fail → survival RIGHT is safe
        snake = _snake_at(10, 10)
        assert self.bot.decide_by_side(snake, (10, 10)) == RIGHT

    def test_survival_left_when_right_is_wall(self):
        # at right wall: survival RIGHT hits wall, survival LEFT is safe
        snake = _snake_at(39, 10)
        assert self.bot.decide_by_side(snake, (39, 10)) == LEFT

    def test_survival_up_when_right_and_left_blocked(self):
        # right wall + body blocking LEFT → survival UP is first safe option
        snake = Snake()
        snake.segments = [(39, 10), (38, 10), (38, 9)]
        assert self.bot.decide_by_side(snake, (39, 10)) == UP

    def test_survival_down_when_right_left_up_blocked(self):
        # right wall + body blocking LEFT + top wall → survival DOWN is first safe option
        snake = Snake()
        snake.segments = [(39, 0), (38, 0), (39, 1)]
        assert self.bot.decide_by_side(snake, (39, 0)) == DOWN

    def test_no_choice_returns_current_direction(self):
        # completely trapped at corner: all 4 moves are game over
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
        # trapped at corner: all 4 moves are game over → fallback to snake.direction
        snake = Snake()
        snake.segments = [(0, 0), (1, 0), (0, 1), (5, 5)]
        assert self.bot.decide_with_distance(snake, (15, 15)) == snake.direction


class TestDecideBfs:
    def test_stub_returns_current_direction(self):
        bot = SnakeBot()
        snake = _snake_at(10, 10)
        assert bot.decide_bfs(snake, (15, 10)) == snake.direction


class TestDecideDfs:
    def setup_method(self):
        self.bot = SnakeBot()

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
        # when head is already on the food, path is empty → falls back to decide_by_side
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