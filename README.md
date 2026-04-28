# SnakeBot

[![Tests](https://github.com/ArturVRSampaio/SnakeBot/actions/workflows/tests.yml/badge.svg)](https://github.com/ArturVRSampaio/SnakeBot/actions/workflows/tests.yml)

A self-playing Snake game where an AI bot autonomously navigates the snake to the food using pathfinding algorithms, rendered in real time with pygame.

## How it works

The active strategy is set via the `STRATEGY` constant in `snakebot/constants.py`. The bot computes a list of moves toward the food; the game loop follows them one per tick and replans when the food is reached or the list runs out.

## Strategies

| Strategy   | `STRATEGY` value | Time per food       | Space per food     | Can complete the game? |
|------------|-----------------|---------------------|--------------------|------------------------|
| Greedy     | `"greedy"`      | O(1)                | O(L)               | No                     |
| Distance   | `"distance"`    | O(1)                | O(L)               | No                     |
| DFS        | `"dfs"`         | O(3^d × L)          | O(3^d × L)         | Unlikely               |
| BFS        | `"bfs"`         | O(N × L)            | O(N × L)           | Unlikely               |

*N = total grid cells (W × H), L = current snake length, d = depth of the path found.*

### Greedy (`"greedy"`)

Checks the four cardinal directions and picks the one that moves the head closest to the food while avoiding immediate collisions. Falls back to any safe direction if the food-facing move is blocked.

- **Time / Space:** O(1) and O(L) — four deep-copies of the snake, constant work per move.
- **Completes the game? No.** Makes locally optimal moves with zero lookahead. As the snake grows it reliably cuts off its own escape routes and traps itself.

### Distance (`"distance"`)

Evaluates all four moves, scores each by Manhattan distance from the new head to the food, and picks the minimum. Skips moves that immediately end the game.

- **Time / Space:** O(1) and O(L) — same constant work as greedy, only the scoring function differs.
- **Completes the game? No.** Still purely reactive. Picks a slightly less naïve direction than greedy but has no path planning and falls into the same traps on longer snakes.

### DFS (`"dfs"`)

Explores the game-state space using a depth-first search over full snake snapshots. Each node holds a complete copy of the snake; a `UniqueStack` deduplicates states by body position in O(1) to avoid cycles. Returns the first path found and follows it.

- **Time:** O(3^d × L) per food — branching factor ≤ 3 (the snake cannot reverse), d is the depth of the path found, L is the cost of copying each snake state.
- **Space:** O(3^d × L) — the stack stores one full snake state per open node.
- **Completes the game? Unlikely.** DFS is complete: it will always find *a* path to the food if one exists. However, it finds the first path, not the safest one, so it frequently leads the snake into a position where no path to the *next* food exists. On long runs the snake tends to cut off large parts of the grid and eventually get trapped.

### BFS (`"bfs"`)

Explores the game-state space level by level using a FIFO queue of full snake snapshots. A `UniqueQueue` deduplicates states in O(1). Because BFS expands nodes in order of distance from the start, the first path found is guaranteed to be the shortest.

- **Time:** O(N × L) per food — visits at most N distinct states, each costing O(L) to copy.
- **Space:** O(N × L) — the queue holds all frontier states simultaneously, much heavier than DFS.
- **Completes the game? Unlikely.** Shortest path to each food is better than DFS's arbitrary path, but like DFS it makes no guarantee about the state left behind after eating. The snake can still paint itself into a corner.

## Project structure

```
main.py                               # Entry point
snakebot/
  constants.py                        # Grid dimensions, colors, directions, speed
  snake.py                            # Snake state and movement
  utils.py                            # Collision detection and food helpers
  bot.py                              # AI decision-making
  game.py                             # Game loop and rendering
  structures/
    exploration_node.py               # Wraps snake state for graph search
    unique_stack.py                   # Deduplicating stack for DFS
    unique_queue.py                   # Deduplicating queue for BFS
tests/
  test_snake.py                       # Snake movement and growth tests
  test_utils.py                       # Collision and food helper tests
  test_structures.py                  # ExplorationNode and UniqueStack tests
  test_bot.py                         # AI algorithm tests
.github/workflows/tests.yml          # CI — runs tests on push and PRs
pytest.ini                            # Test configuration
.coveragerc                           # Coverage configuration
```

## Requirements

- Python 3.12+
- pygame

Install dependencies:

```bash
pip install pygame
```

## Running

```bash
python main.py
```

## Tests

The test suite covers all game logic, AI algorithms, and data structures. It does **not** require pygame.

Install test dependencies:

```bash
pip install pytest pytest-cov
```

Run all tests:

```bash
python -m pytest
```

Run with verbose output:

```bash
python -m pytest -v
```

Run with coverage report:

```bash
python -m pytest --cov=snakebot --cov-report=term-missing
```

All logic files reach **100% line coverage**. `snakebot/game.py` and `main.py` are excluded as they are pygame UI entry points with no standalone logic.

### What is tested

| File                       | Coverage                                                                                        |
|----------------------------|-------------------------------------------------------------------------------------------------|
| `tests/test_snake.py`      | Movement in all directions, growth on food, tail dropping                                       |
| `tests/test_utils.py`      | Wall and self-collision detection, food detection, food spawn bounds                            |
| `tests/test_structures.py` | `ExplorationNode` status transitions; `UniqueStack` push, pop, deduplication, query methods     |
| `tests/test_bot.py`        | Distance functions, all `decide_by_side` branches, `decide_with_distance`, `decide_dfs`, `decide_bfs` |

## Configuration

Edit `snakebot/constants.py` to change game settings:

| Constant     | Default    | Description                                         |
|--------------|------------|-----------------------------------------------------|
| `WIDTH`      | 800        | Window width in pixels                              |
| `HEIGHT`     | 800        | Window height in pixels                             |
| `GRID_SIZE`  | 20         | Cell size in pixels                                 |
| `GAME_SPEED` | 100        | Ticks per second                                    |
| `STRATEGY`   | `"dfs"`    | Pathfinding algorithm: `"dfs"`, `"bfs"`, `"distance"`, `"greedy"` |