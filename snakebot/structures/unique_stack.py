from snakebot.structures.exploration_node import ExplorationNode


class UniqueStack:
    def __init__(self, firstItem: ExplorationNode):
        self.items = []
        self.items.append(firstItem)
        self.unique_set = {tuple(firstItem.snake.segments)}

    def push(self, item: ExplorationNode):
        key = tuple(item.snake.segments)
        if key in self.unique_set:
            item.discard()
            return None

        self.items.append(item)
        self.unique_set.add(key)
        return None

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def has_not_discarted_items(self):
        return any(item.status != "discarded" for item in self.items)

    def has_unexplored_items(self):
        return any(item.is_unexplored() for item in self.items)

    def get_last_unexplored_item(self):
        while self.items and self.items[-1].is_discarded():
            self.items.pop()
        for item in reversed(self.items):
            if item.status == "unexplored":
                return item
        return None

    def get_explored_items(self):
        return [item for item in self.items if item.status == "explored"]

    def get_last_not_discarded_item(self):
        for item in reversed(self.items):
            if item.status != "discarded":
                return item
        return None

    def count_unexplored_items(self):
        return sum(1 for item in self.items if item.status == "unexplored")

    def count_discarted_items(self):
        return sum(1 for item in self.items if item.status == "discarded")

    def count_explored_items(self):
        return sum(1 for item in self.items if item.status == "explored")
