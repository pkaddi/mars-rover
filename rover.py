from enum import Enum
from position import Position
from direction import Direction
from plateau import Plateau
from exceptions import OutOfPlateau, InvalidCommand


class Command(Enum):
    MOVE = "M"
    LEFT = "L"
    RIGHT = "R"

    @staticmethod
    def from_str(s):
        if s not in [c.value for c in Command]:
            raise InvalidCommand(f"Invalid Command input:{s}")
        return Command(s)


class Rover:
    def __init__(self, plateau: Plateau, position: Position, direction: Direction):
        self.plateau = plateau
        if not self.plateau.within_bounds(position):
            raise OutOfPlateau("Rover landing position is outside the plateau")
        self.position = position
        self.direction = direction

    def __move(self):
        new_position = self.position + Position(self.direction.x, self.direction.y)
        if not self.plateau.within_bounds(new_position):
            raise OutOfPlateau("Rover is outside the plateau")
        self.position = new_position

    def __right(self):
        self.direction = Direction((self.direction + 1) % 4)

    def __left(self):
        self.direction = Direction((self.direction - 1) % 4)

    @property
    def __commands(self):
        return {
            Command.MOVE: self.__move,
            Command.LEFT: self.__left,
            Command.RIGHT: self.__right,
        }

    @property
    def state(self):
        return (self.position, self.direction)

    def run_commands(self, command: str):
        for c in command:
            self.__commands[Command.from_str(c)]()
        return self.state
