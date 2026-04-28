from snakebot.structures.exploration_node import ExplorationNode


class UniqueStack:
    def __init__(self, firstItem: ExplorationNode):
        self.items = []
        self.items.append(firstItem)
        self.unique_set = set()

    def push(self, item: ExplorationNode):
        for existing_item in self.items:
            if existing_item.snake.segments == item.snake.segments:
                item.discard()
                return None

        self.items.append(item)
        self.unique_set.add(item)
        return None

    def pop(self):
        if not self.is_empty():
            popped_item = self.items.pop()
            self.unique_set.remove(popped_item)
            return popped_item

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def has_not_discarted_items(self):
        return any(item.status != "discarded" for item in self.items)

    def get_last_unexplored_item(self):
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
