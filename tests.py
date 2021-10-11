import unittest
from plateau import Plateau
from position import Position
from direction import Direction
from rover import Rover, Command
from exceptions import *
from main import parse_plateau, parse_position_direction, parse_commands


class TestMain(unittest.TestCase):
    def test_parser_plateau(self):
        plateau = Plateau(5, 5)
        self.assertEqual(parse_plateau("Plateau:5 5"), Plateau(5, 5))
        with self.assertRaises(ParserError):
            parse_plateau("Platea:5 5")
        with self.assertRaises(ParserError):
            parse_plateau("Plateau:5 a")

    def test_parser_position_direction(self):
        p = Position(1, 2)
        d = Direction.from_str("N")
        self.assertEqual(parse_position_direction("Rover1 Landing:1 2 N"), (p, d))
        with self.assertRaises(ParserError):
            parse_position_direction("Rover1 Landin:1 2 N")
        with self.assertRaises(ParserError):
            parse_position_direction("Rover1 Landing:1 a 3")

    def test_commands(self):
        self.assertEqual(
            parse_commands("Rover1 Instructions:LMLMLMLMM"), ("Rover1", "LMLMLMLMM")
        )
        with self.assertRaises(ParserError):
            parse_commands("Rover1 Instruction:LMLMLMLMM")

    def test_rover(self):
        pl = Plateau(5, 5)
        p = Position(1, 2)
        d = Direction.from_str("N")
        r = Rover(pl, p, d)
        r.run_commands("LMLMLMLMM")
        self.assertEqual(
            (r.state[0], r.state[1]), (Position(1, 3), Direction.from_str("N"))
        )


class TestRover(unittest.TestCase):
    def test_rover_turn(self):
        rover = Rover(Plateau(5, 5), Position(1, 2), Direction.from_str("N"))
        rover.run_commands("L")
        self.assertEqual(rover.state[1], Direction.from_str("W"))
        rover.run_commands("R")
        self.assertEqual(rover.state[1], Direction.from_str("N"))

    def test_rover_move(self):
        rover = Rover(Plateau(5, 5), Position(1, 2), Direction.from_str("N"))
        rover.run_commands("M")
        self.assertEqual(rover.state[0], Position(1, 3))
        rover = Rover(Plateau(5, 5), Position(1, 2), Direction.from_str("W"))
        rover.run_commands("M")
        self.assertEqual(rover.state[0], Position(0, 2))

    def test_rover_commands(self):
        rover = Rover(Plateau(5, 5), Position(1, 2), Direction.from_str("N"))
        rover.run_commands("LMLMLMLMM")
        self.assertEqual(
            (rover.state[0], rover.state[1]), (Position(1, 3), Direction.from_str("N"))
        )
        rover = Rover(Plateau(5, 5), Position(3, 3), Direction.from_str("E"))
        rover.run_commands("MMRMMRMRRM")
        self.assertEqual(
            (rover.state[0], rover.state[1]), (Position(5, 1), Direction.from_str("E"))
        )

    def test_rover_outofplateau(self):
        rover = Rover(Plateau(5, 5), Position(5, 5), Direction.from_str("N"))
        with self.assertRaises(OutOfPlateau):
            rover.run_commands("M")
        rover = Rover(Plateau(5, 5), Position(0, 0), Direction.from_str("S"))
        with self.assertRaises(OutOfPlateau):
            rover.run_commands("M")

    def test_invalid_command(self):
        with self.assertRaises(InvalidCommand):
            Command.from_str("T")


class PlateauTests(unittest.TestCase):
    def test_bounds(self):
        plateau = Plateau(5, 5)
        self.assertEqual(plateau.within_bounds(Position(1, 2)), True)
        self.assertEqual(plateau.within_bounds(Position(1, 6)), False)
        self.assertEqual(plateau.within_bounds(Position(6, 1)), False)
        self.assertEqual(plateau.within_bounds(Position(-1, 0)), False)
        self.assertEqual(plateau.within_bounds(Position(0, -1)), False)


class DirectionTests(unittest.TestCase):
    def test_x_for_ns(self):
        self.assertEqual(0, Direction.from_str("N").x)
        self.assertEqual(0, Direction.from_str("S").x)

    def test_y_for_ew(self):
        self.assertEqual(0, Direction.from_str("E").y)
        self.assertEqual(0, Direction.from_str("W").y)

    def test_y_for_ns(self):
        self.assertEqual(1, Direction.from_str("N").y)
        self.assertEqual(-1, Direction.from_str("S").y)

    def test_x_for_ew(self):
        self.assertEqual(1, Direction.from_str("E").x)
        self.assertEqual(-1, Direction.from_str("W").x)

    def test_invalid_direction(self):
        with self.assertRaises(InvalidDirection):
            Direction.from_str("T")
