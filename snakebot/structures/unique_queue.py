from collections import deque

from snakebot.structures.exploration_node import ExplorationNode


class UniqueQueue:
    def __init__(self, first_item: ExplorationNode):
        self.items = deque([first_item])
        self.unique_set = {tuple(first_item.snake.segments)}

    def push(self, item: ExplorationNode):
        key = tuple(item.snake.segments)
        if key in self.unique_set:
            item.discard()
            return None
        self.items.append(item)
        self.unique_set.add(key)
        return None

    def has_unexplored_items(self):
        return any(item.is_unexplored() for item in self.items)

    def get_first_unexplored_item(self):
        while self.items and not self.items[0].is_unexplored():
            self.items.popleft()
        return self.items[0] if self.items else None

    def size(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0
