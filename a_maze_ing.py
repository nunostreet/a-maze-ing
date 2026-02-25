#!/usr/bin/env python3
from maze.generator import MazeGenerator
from config.parser import parser
from render.ascii import menu


def main() -> None:
    config = parser()

    generator = MazeGenerator(config)
    generator.generate()
    generator.get_grid()

    generator.get_solution()
    menu(generator, config)


if __name__ == "__main__":
    main()
