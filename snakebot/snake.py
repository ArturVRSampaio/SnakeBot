from snakebot.constants import GRID_WIDTH, GRID_HEIGHT, RIGHT


class Snake:

    def __init__(self):
        self.segments = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.eaten = False

    def head(self):
        return self.segments[0]

    def add_segment(self):
        self.eaten = True

    def move(self):
        new_head = (self.head()[0] + self.direction[0], self.head()[1] + self.direction[1])
        self.segments.insert(0, new_head)
        if self.eaten:
            self.eaten = False
        else:
            self.segments.pop()
