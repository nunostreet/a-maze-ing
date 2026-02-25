#!/usr/bin/env python3
from maze.generator import MazeGenerator
from io_helpers.parser import parser
from io_helpers.writer import write_maze
from render.ascii import menu


def main() -> int:
    """
    Run the application and return a process exit code.
    """
    try:
        config = parser()
        if config is None:
            return 1

        generator = MazeGenerator(config)
        generator.generate()

        grid = generator.get_grid()
        solution = generator.get_solution()
        write_maze(
            grid,
            config["ENTRY"],
            config["EXIT"],
            solution,
            config["OUTPUT_FILE"],
        )

        menu(generator, config)
        return 0

    except (ValueError, RuntimeError, OSError) as exc:
        print(exc)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
