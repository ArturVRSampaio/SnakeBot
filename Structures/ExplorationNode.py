class ExplorationNode:
    def __init__(self, snake, parent = None):
        self.parent = parent
        self.snake = snake
        self.status = "unexplored"  # Default status is unexplored

    def explore(self):
        self.status = "explored"

    def discard(self):
        self.status = "discarded"

    def is_explored(self):
        return self.status == "explored"

    def is_discarded(self):
        return self.status == "discarded"

    def is_unexplored(self):
        return self.status == "unexplored"
