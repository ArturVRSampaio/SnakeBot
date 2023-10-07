from Structures.ExplorationNode import ExplorationNode


class UniqueStack:
    def __init__(self):
        self.items = []
        self.unique_set = set()

    def push(self, item):
        if not isinstance(item, ExplorationNode):
            raise ValueError("Item must be an instance of ExplorationNode.")

        # Check if the same snake is already in the stack
        for existing_item in self.items:
            if existing_item.snake.segments == item.snake.segments:
                return existing_item

        self.items.append(item)
        self.unique_set.add(item)
        return item

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
        return None  # No unexplored items found

    def get_explored_items(self):
        return [item for item in self.items if item.status == "explored"]

    def get_last_not_discarded_item(self):
        for item in reversed(self.items):
            if item.status != "discarded":
                return item
        return None  # No non-discarded items found

    def count_unexplored_items(self):
        return sum(1 for item in self.items if item.status == "unexplored")

    def count_discarted_items(self):
        return sum(1 for item in self.items if item.status == "discarded")

    def count_explored_items(self):
        return sum(1 for item in self.items if item.status == "explored")


