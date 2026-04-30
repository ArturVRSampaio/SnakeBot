# SnakeBot

[![Tests](https://github.com/ArturVRSampaio/SnakeBot/actions/workflows/tests.yml/badge.svg)](https://github.com/ArturVRSampaio/SnakeBot/actions/workflows/tests.yml)

A self-playing Snake game where an AI bot autonomously navigates the snake to the food using pathfinding algorithms, rendered in real time with pygame.

## How it works

The active strategy is set via the `STRATEGY` constant in `snakebot/constants.py`. The bot computes a list of moves toward the food; the game loop follows them one per tick and replans when the food is reached or the list runs out.

## Strategies

| Strategy           | `STRATEGY` value   | Time per food    | Space           | Can complete the game? |
|--------------------|--------------------|------------------|-----------------|------------------------|
| Greedy             | `"greedy"`         | O(1)             | O(L)            | No                     |
| Distance           | `"distance"`       | O(1)             | O(L)            | No                     |
| DFS                | `"dfs"`            | O(3^d × L)       | O(3^d × L)      | Unlikely               |
| BFS                | `"bfs"`            | O(N × L)         | O(N × L)        | Unlikely               |
| IDDFS              | `"iddfs"`          | O(N × L)         | O(N × L)        | Unlikely               |
| Bidirectional BFS  | `"bidirectional"`  | O(4^(d/2))       | O(4^(d/2))      | Unlikely               |
| Hamiltonian        | `"hamiltonian"`    | O(1)             | O(N)            | **Yes**                |

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

### IDDFS (`"iddfs"`)

Runs depth-limited DFS repeatedly with increasing depth limits (1, 2, 3, …) until the food is found. Finds the shortest path like BFS. A transposition table records each state's best-seen remaining depth budget, so a state is only re-explored when visited with strictly more depth available than before. This eliminates the exponential re-exploration of naive IDDFS, bounding each iteration to O(N) unique state visits.

- **Time:** O(N × L) per food — a transposition table records each state's best remaining depth, bounding unique state visits to N per depth iteration. Total work is O(d × N × L) but amortized to O(N × L) since each state is visited at most once across all iterations.
- **Space:** O(N × L) — the transposition table grows to at most N entries, each holding an O(L) state key.
- **Completes the game? Unlikely.** Like DFS and BFS, it finds the shortest path to each food but doesn't plan for survival afterward.

### Bidirectional BFS (`"bidirectional"`)

Runs two BFS searches simultaneously — forward from the snake's head and backward from the food — stopping when their frontiers overlap. The meeting point is at roughly d/2 steps from each end, reducing the search radius dramatically.

The forward frontier avoids the snake's current body. The backward frontier explores grid positions only (no body tracking), since reverse snake-move reconstruction is non-trivial. The two halves of the path are joined at the meeting point.

- **Time:** O(4^(d/2)) per food — each frontier expands to depth d/2, vs O(N × L) for full-state BFS.
- **Space:** O(4^(d/2)) — both frontiers combined, no per-node snake-state copies.
- **Completes the game? Unlikely.** The backward portion of the combined path does not account for the snake's body at each step, so the snake may occasionally navigate into its own body on longer snakes. Short-path cases are reliably correct.

### Hamiltonian (`"hamiltonian"`)

Pre-computes a fixed boustrophedon (zigzag) circuit that visits every cell exactly once: row 0 left-to-right, row 1 right-to-left, row 2 left-to-right, and so on. At runtime the bot does a single O(1) dict lookup to find the current head in the circuit and returns the direction to the next cell.

- **Time / Space:** O(1) per move — direction lookup in a pre-built index; O(N) one-time startup cost to build the path.
- **Completes the game? Yes.** The circuit covers every cell, so the snake will reach any food position on every pass. It is the only strategy here that guarantees completing the game.

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
| `STRATEGY`   | `"dfs"`    | Pathfinding algorithm: `"dfs"`, `"bfs"`, `"iddfs"`, `"bidirectional"`, `"distance"`, `"greedy"`, `"hamiltonian"` |