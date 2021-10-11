class Plateau:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)

    def within_bounds(self, position):
        return 0 <= position.x <= self.width and 0 <= position.y <= self.height

    def __eq__(self, o):
        if self.width == o.width and self.height == o.height:
            return True
        return False
