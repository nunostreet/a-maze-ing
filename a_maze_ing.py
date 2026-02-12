#!/usr/bin/env python3
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    print(f"Config file received: {config_file}")
    print("A-Maze-ing started successfully!")


if __name__ == "__main__":
    main()
