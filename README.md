# SnakeBot

[![Tests](https://github.com/ArturVRSampaio/SnakeBot/actions/workflows/tests.yml/badge.svg)](https://github.com/ArturVRSampaio/SnakeBot/actions/workflows/tests.yml)

A self-playing Snake game where an AI bot autonomously navigates the snake to the food using pathfinding algorithms, rendered in real time with pygame.

## How it works

The bot uses **Depth-First Search (DFS)** to explore the game state space and find a path from the snake's head to the food. Each node in the search tree holds a full snapshot of the snake, and a custom `UniqueStack` prevents revisiting states with the same body position. Once a path is found, the game follows it move by move. If no path exists, the bot falls back to a greedy strategy that moves toward the food while avoiding immediate collisions.

Additional algorithms are implemented but not currently active:
- **Greedy (distance-based):** picks the direction that minimizes Manhattan distance to the food at each step.
- **BFS:** stub, not yet implemented.

## Project structure

```
Main.py                          # Entry point
SnakeGame.py                     # Game loop and rendering
Snake.py                         # Snake state and movement
SnakeBot.py                      # AI decision-making
Utils.py                         # Collision detection and food helpers
Constants.py                     # Grid dimensions, colors, directions, speed
Structures/
  ExplorationNode.py             # Wraps snake state for graph search
  UniqueStack.py                 # Deduplicating stack for DFS
tests/
  test_snake.py                  # Snake movement and growth tests
  test_utils.py                  # Collision and food helper tests
  test_structures.py             # ExplorationNode and UniqueStack tests
  test_snakebot.py               # AI algorithm tests
.github/workflows/tests.yml     # CI — runs tests on push and PRs
pytest.ini                       # Test and coverage configuration
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
python Main.py
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
python -m pytest --cov=. --cov-report=term-missing
```

All logic files (`Snake`, `SnakeBot`, `Utils`, `Structures`) are at **100% line coverage**. `Main.py` and `SnakeGame.py` are excluded from coverage as they are pygame UI entry points with no standalone logic.

### What is tested

| File                         | Coverage                                                                                          |
|------------------------------|---------------------------------------------------------------------------------------------------|
| `tests/test_snake.py`        | Movement in all directions, growth on food, tail dropping                                         |
| `tests/test_utils.py`        | Wall and self-collision detection, food detection, food spawn bounds                              |
| `tests/test_structures.py`   | `ExplorationNode` status transitions; `UniqueStack` push, pop, deduplication, query methods       |
| `tests/test_snakebot.py`     | Distance functions, all `decide_by_side` branches, `decide_with_distance`, `decide_dfs`, `decide_bfs` |

## Configuration

Edit `Constants.py` to change game settings:

| Constant     | Default | Description              |
|--------------|---------|--------------------------|
| `WIDTH`      | 800     | Window width in pixels   |
| `HEIGHT`     | 800     | Window height in pixels  |
| `GRID_SIZE`  | 20      | Cell size in pixels      |
| `GAME_SPEED` | 100     | Ticks per second         |