import math
import copy
import heapq
from collections import deque

from snakebot.structures.exploration_node import ExplorationNode
from snakebot.structures.unique_stack import UniqueStack
from snakebot.structures.unique_queue import UniqueQueue
from snakebot.utils import is_game_over, will_snake_eat_the_food
from snakebot.constants import DIRECTIONS, UP, DOWN, LEFT, RIGHT, STRATEGY, GRID_WIDTH, GRID_HEIGHT


class SnakeBot:

    def decide(self, snake, food, render_callback=None):
        if STRATEGY == "dfs":
            return self.decide_dfs(snake, food, render_callback)
        elif STRATEGY == "bfs":
            return self.decide_bfs(snake, food, render_callback)
        elif STRATEGY == "distance":
            return [self.decide_with_distance(snake, food)]
        elif STRATEGY == "greedy":
            return [self.decide_by_side(snake, food)]
        elif STRATEGY == "iddfs":
            return self.decide_iddfs(snake, food, render_callback)
        elif STRATEGY == "bidirectional":
            return self.decide_bidirectional_bfs(snake, food, render_callback)
        elif STRATEGY == "astar":
            return self.decide_astar(snake, food, render_callback)
        elif STRATEGY == "dstar":
            return self.decide_dstar(snake, food, render_callback)
        elif STRATEGY == "hamiltonian":
            return [self.decide_hamiltonian(snake)]
        else:
            raise ValueError(f"Unknown strategy: '{STRATEGY}'. Valid options: 'dfs', 'bfs', 'iddfs', 'bidirectional', 'astar', 'dstar', 'distance', 'greedy', 'hamiltonian'")

    def decide_dfs(self, snake, food, render_callback=None):
        stack = UniqueStack(ExplorationNode(snake))

        while stack.has_unexplored_items():
            node = stack.get_last_unexplored_item()

            if render_callback:
                render_callback(node.snake)

            if is_game_over(node.snake):
                node.discard()
            elif will_snake_eat_the_food(node.snake, food):
                node.explore()
                path = []

                while node.parent:
                    path.append(node.snake.direction)
                    node = node.parent

                if not path:
                    path.append(self.decide_by_side(snake, food))

                return path
            else:
                node.explore()

                for direction in DIRECTIONS:
                    new_snake = copy.deepcopy(node.snake)
                    new_snake.direction = direction
                    new_snake.move()

                    new_node = ExplorationNode(new_snake, node)
                    stack.push(new_node)

        return [snake.direction]

    def decide_bfs(self, snake, food, render_callback=None):
        queue = UniqueQueue(ExplorationNode(snake))

        while queue.has_unexplored_items():
            node = queue.get_first_unexplored_item()

            if render_callback:
                render_callback(node.snake)

            if is_game_over(node.snake):
                node.discard()
            elif will_snake_eat_the_food(node.snake, food):
                node.explore()
                path = []

                while node.parent:
                    path.append(node.snake.direction)
                    node = node.parent

                if not path:
                    path.append(self.decide_by_side(snake, food))

                return path
            else:
                node.explore()

                for direction in DIRECTIONS:
                    new_snake = copy.deepcopy(node.snake)
                    new_snake.direction = direction
                    new_snake.move()

                    new_node = ExplorationNode(new_snake, node)
                    queue.push(new_node)

        return [snake.direction]

    def decide_iddfs(self, snake, food, render_callback=None):
        for depth_limit in range(1, GRID_WIDTH * GRID_HEIGHT + 1):
            result = self._iddfs_search(
                ExplorationNode(snake), food, depth_limit, {}, render_callback
            )
            if result is not None:
                return result
        return [snake.direction]

    def _iddfs_search(self, node, food, depth, trans_table, render_callback):
        if render_callback:
            render_callback(node.snake)

        if is_game_over(node.snake):
            return None

        if will_snake_eat_the_food(node.snake, food):
            path = []
            current = node
            while current.parent:
                path.append(current.snake.direction)
                current = current.parent
            if not path:
                path.append(self.decide_by_side(node.snake, food))
            return path

        if depth == 0:
            return None

        key = tuple(node.snake.segments)
        if key in trans_table and trans_table[key] >= depth:
            return None
        trans_table[key] = depth

        for direction in DIRECTIONS:
            new_snake = copy.deepcopy(node.snake)
            new_snake.direction = direction
            new_snake.move()
            child = ExplorationNode(new_snake, node)
            result = self._iddfs_search(child, food, depth - 1, trans_table, render_callback)
            if result is not None:
                return result

        return None

    def decide_bidirectional_bfs(self, snake, food, render_callback=None):
        head = snake.head()
        if head == food:
            return [self.decide_by_side(snake, food)]

        # Use current body (minus tail) as a static obstacle.
        # The tail vacates on the first move, so it's safe to enter on step 1.
        body_obstacle = set(snake.segments[:-1])

        forward_queue = deque([head])
        forward_parent = {head: None}

        backward_queue = deque([food])
        backward_parent = {food: None}

        meeting = None

        while (forward_queue or backward_queue) and meeting is None:
            if forward_queue:
                pos = forward_queue.popleft()
                for dx, dy in DIRECTIONS:
                    nxt = (pos[0] + dx, pos[1] + dy)
                    if (nxt not in forward_parent
                            and nxt not in body_obstacle
                            and 0 <= nxt[0] < GRID_WIDTH
                            and 0 <= nxt[1] < GRID_HEIGHT):
                        forward_parent[nxt] = pos
                        forward_queue.append(nxt)
                        if render_callback:
                            ghost = copy.deepcopy(snake)
                            ghost.segments = [nxt]
                            render_callback(ghost)
                        if nxt in backward_parent:
                            meeting = nxt
                            break

            if meeting is not None:
                break

            if backward_queue:
                pos = backward_queue.popleft()
                for dx, dy in DIRECTIONS:
                    nxt = (pos[0] + dx, pos[1] + dy)
                    if (nxt not in backward_parent
                            and 0 <= nxt[0] < GRID_WIDTH
                            and 0 <= nxt[1] < GRID_HEIGHT):
                        backward_parent[nxt] = pos
                        backward_queue.append(nxt)
                        if nxt in forward_parent:
                            meeting = nxt
                            break

        if meeting is None:
            return [snake.direction]

        # Forward path: head → meeting
        forward_path = []
        pos = meeting
        while forward_parent[pos] is not None:
            prev = forward_parent[pos]
            forward_path.append((pos[0] - prev[0], pos[1] - prev[1]))
            pos = prev
        forward_path.reverse()

        # Backward path: meeting → food
        backward_path = []
        pos = meeting
        while backward_parent[pos] is not None:
            nxt = backward_parent[pos]
            backward_path.append((nxt[0] - pos[0], nxt[1] - pos[1]))
            pos = nxt

        full_path = forward_path + backward_path
        if not full_path:
            return [self.decide_by_side(snake, food)]

        return list(reversed(full_path))

    def decide_astar(self, snake, food, render_callback=None):
        start_node = ExplorationNode(snake)
        start_key = tuple(snake.segments)
        h = _manhattan_distance(snake.head(), food)

        counter = 0
        open_heap = [(h, counter, 0, start_node)]
        best_g = {start_key: 0}

        while open_heap:
            f, _, g, node = heapq.heappop(open_heap)

            if render_callback:
                render_callback(node.snake)

            key = tuple(node.snake.segments)
            if best_g.get(key, float('inf')) < g:
                continue

            if is_game_over(node.snake):
                continue

            if will_snake_eat_the_food(node.snake, food):
                path = []
                current = node
                while current.parent:
                    path.append(current.snake.direction)
                    current = current.parent
                if not path:
                    path.append(self.decide_by_side(node.snake, food))
                return path

            node.explore()

            for direction in DIRECTIONS:
                new_snake = copy.deepcopy(node.snake)
                new_snake.direction = direction
                new_snake.move()
                new_key = tuple(new_snake.segments)
                new_g = g + 1

                if new_g < best_g.get(new_key, float('inf')):
                    best_g[new_key] = new_g
                    new_h = _manhattan_distance(new_snake.head(), food)
                    counter += 1
                    new_node = ExplorationNode(new_snake, node)
                    heapq.heappush(open_heap, (new_g + new_h, counter, new_g, new_node))

        return [snake.direction]

    def decide_dstar(self, snake, food, render_callback=None):
        head = snake.head()
        if head == food:
            return [self.decide_by_side(snake, food)]

        # Exclude head (search origin). Exclude tail only when it will vacate;
        # when eaten=True the snake grows and the tail stays this move.
        body_obstacle = set(snake.segments[1:] if snake.eaten else snake.segments[1:-1])
        INF = float('inf')

        g = {}
        rhs = {food: 0}

        def get_g(s): return g.get(s, INF)
        def get_rhs(s): return rhs.get(s, INF)
        def h(s): return _manhattan_distance(s, head)
        def calc_key(s):
            m = min(get_g(s), get_rhs(s))
            return (m + h(s), m)

        def passable(pos):
            return (0 <= pos[0] < GRID_WIDTH
                    and 0 <= pos[1] < GRID_HEIGHT
                    and pos not in body_obstacle)

        def neighbors(s):
            for dx, dy in DIRECTIONS:
                nxt = (s[0] + dx, s[1] + dy)
                if passable(nxt):
                    yield nxt

        counter = 0
        heap = []
        in_heap = {}

        def push(s):
            nonlocal counter
            k = calc_key(s)
            counter += 1
            heapq.heappush(heap, (k, counter, s))
            in_heap[s] = k

        def update_vertex(u):
            if u != food:
                rhs[u] = min((get_g(nb) + 1 for nb in neighbors(u)), default=INF)
            if get_g(u) != get_rhs(u):
                push(u)

        push(food)

        while heap:
            # Discard stale entries (superseded by a later push with a different key).
            while heap and in_heap.get(heap[0][2]) != heap[0][0]:
                heapq.heappop(heap)
            if not heap:
                break

            k, _, u = heap[0]

            if k >= calc_key(head) and get_rhs(head) == get_g(head):
                break

            heapq.heappop(heap)
            del in_heap[u]

            if render_callback:
                ghost = copy.deepcopy(snake)
                ghost.segments = [u]
                render_callback(ghost)

            if get_g(u) > get_rhs(u):
                g[u] = get_rhs(u)
                for nb in neighbors(u):
                    update_vertex(nb)
            else:
                g[u] = INF
                update_vertex(u)
                for nb in neighbors(u):
                    update_vertex(nb)

        if get_g(head) >= INF:
            return [self.decide_by_side(snake, food)]

        # Return only the first step. The g-value map is computed against the
        # current static body, but the body shifts every move, so a multi-step
        # path would cross cells that become occupied on later ticks.
        # Returning one step forces a fresh replan each move with the updated body.
        best = min(
            (nxt for dx, dy in DIRECTIONS
             for nxt in [(head[0] + dx, head[1] + dy)]
             if passable(nxt)),
            key=get_g,
            default=None
        )
        if best is None:
            return [self.decide_by_side(snake, food)]
        return [(best[0] - head[0], best[1] - head[1])]

    def decide_hamiltonian(self, snake):
        head = snake.head()
        idx = _HAMILTONIAN_INDEX.get(head, 0)
        next_pos = _HAMILTONIAN_PATH[(idx + 1) % len(_HAMILTONIAN_PATH)]
        return (next_pos[0] - head[0], next_pos[1] - head[1])

    def decide_with_distance(self, snake, food):
        paths = []
        for direction in DIRECTIONS:
            new_snake = copy.deepcopy(snake)
            new_snake.direction = direction
            new_snake.move()
            if not is_game_over(new_snake):
                paths.append([new_snake.direction, _manhattan_distance(new_snake.head(), food)])

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


def _build_hamiltonian_path():
    # Row 0: full width left to right.
    # Rows 1..H-1: serpentine over columns 1..W-1 only.
    # Column 0: walk back up from (0,H-1) to (0,1) to close the cycle at (0,0).
    path = []
    for x in range(GRID_WIDTH):
        path.append((x, 0))
    for y in range(1, GRID_HEIGHT):
        if y % 2 == 1:
            for x in range(GRID_WIDTH - 1, 0, -1):
                path.append((x, y))
        else:
            for x in range(1, GRID_WIDTH):
                path.append((x, y))
    for y in range(GRID_HEIGHT - 1, 0, -1):
        path.append((0, y))
    return tuple(path)


_HAMILTONIAN_PATH = _build_hamiltonian_path()
_HAMILTONIAN_INDEX = {pos: i for i, pos in enumerate(_HAMILTONIAN_PATH)}


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
