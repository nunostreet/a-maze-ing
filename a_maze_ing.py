#!/usr/bin/env python3
import sys
from maze.generator import MazeGenerator


def main() -> None:
    config = {
    "WIDTH": 5,
    "HEIGHT": 5,
    "ENTRY": (0, 0),
    "EXIT": (4, 4),
    "PERFECT": True,
    "SEED": 99,
}

    generator = MazeGenerator(config)
    generator.generate()

    print("Grid:")
    for row in generator.get_grid():
        print(row)

    print("Solution:")
    print(generator.get_solution())


if __name__ == "__main__":
    main()
