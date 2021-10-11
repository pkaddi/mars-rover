import fileinput
import re
from plateau import Plateau
from position import Position
from direction import Direction
from rover import Rover
from exceptions import ParserError


def parse_plateau(line):
    s = re.match("Plateau:([0-9]+) ([0-9]+)$", line)
    if not s:
        raise ParserError(f"Invalid plateau input: {line}")
    return Plateau(int(s.group(1)), int(s.group(2)))


def parse_position_direction(line):
    s = re.match(
        "Rover[0-9]+ Landing:([0-9]+) ([0-9]+) (N|E|S|W)",
        line,
    )
    if not s:
        raise ParserError(f"Invalid rover landing input: {line}")
    return Position(int(s.group(1)), int(s.group(2))), Direction.from_str(s.group(3))


def parse_commands(line):
    s = re.match("^\s*(.*?)\s+Instructions:((L|R|M)+)$", line)
    if not s:
        raise ParserError(
            f"""Invalid rxover instruction. It must contain only ('L','R','M')."""
            f"""The error input: {line}"""
        )
    return s.group(1), s.group(2)


if __name__ == "__main__":
    lines = list(fileinput.input())

    plateau = parse_plateau(lines[0])
    for i in range(1, int(len(lines) / 2) + 1):
        landing = lines[2 * i - 1]
        instruction = lines[2 * i]

        position, direction = parse_position_direction(landing)
        rover = Rover(plateau, position, direction)
        rover_name, commands = parse_commands(instruction)

        rover.run_commands(commands)
        print(
            f"{rover_name}:{ rover.state[0].x} {rover.state[0].y} {rover.state[1].name}"
        )
