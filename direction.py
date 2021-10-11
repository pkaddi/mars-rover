from enum import IntEnum
from exceptions import InvalidDirection


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @property
    def x(self) -> int:
        if self in (Direction.N, Direction.S):
            return 0
        if self == Direction.E:
            return 1
        return -1

    @property
    def y(self) -> int:
        if self in (Direction.E, Direction.W):
            return 0
        if self == Direction.N:
            return 1
        return -1

    @staticmethod
    def from_str(s):
        if s not in [d.name for d in Direction]:
            raise InvalidDirection(f"Invalid direction input:{s}")
        return Direction[s]
