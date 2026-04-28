# SnakeBot

A self-playing Snake game where an AI bot autonomously navigates the snake to the food using pathfinding algorithms, rendered in real time with pygame.

## How it works

The bot uses **Depth-First Search (DFS)** to explore the game state space and find a path from the snake's head to the food. Each node in the search tree holds a full snapshot of the snake, and a custom `UniqueStack` prevents revisiting states with the same body position. Once a path is found, the game follows it move by move. If no path exists, the bot falls back to a greedy strategy that moves toward the food while avoiding immediate collisions.

Additional algorithms are implemented but not currently active:
- **Greedy (distance-based):** picks the direction that minimizes Manhattan distance to the food at each step.
- **BFS:** stub, not yet implemented.

## Project structure

```
Main.py                     # Entry point
SnakeGame.py                # Game loop and rendering
Snake.py                    # Snake state and movement
SnakeBot.py                 # AI decision-making
Utils.py                    # Collision detection and food helpers
Constants.py                # Grid dimensions, colors, directions, speed
Structures/
  ExplorationNode.py        # Wraps snake state for graph search
  UniqueStack.py            # Deduplicating stack for DFS
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

## Configuration

Edit `Constants.py` to change game settings:

| Constant     | Default | Description              |
|--------------|---------|--------------------------|
| `WIDTH`      | 800     | Window width in pixels   |
| `HEIGHT`     | 800     | Window height in pixels  |
| `GRID_SIZE`  | 20      | Cell size in pixels      |
| `GAME_SPEED` | 100     | Ticks per second         |