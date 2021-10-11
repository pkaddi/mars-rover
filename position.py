class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Position(self.x + o.x, self.y + o.y)

    def __eq__(self, o):
        if self.x == o.x and self.y == o.y:
            return True
        return False
