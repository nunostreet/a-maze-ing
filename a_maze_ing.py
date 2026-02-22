#!/usr/bin/env python3
from maze.generator import MazeGenerator


def main() -> None:
    config = {
        "WIDTH": 15,
        "HEIGHT": 15,
        "ENTRY": (1, 1),
        "EXIT": (13, 13),
        "PERFECT": True,
        "SEED": 1,
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
