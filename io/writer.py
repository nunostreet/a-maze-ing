def write_maze(grid: list[list[int]], entry: tuple[int, int],
               exit: tuple[int, int], path: str,
               output_file: str) -> None:
    """Write the maze to a file in hexadecimal format.
    Args:
        grid: 2D list of integers representing the maze.
        entry: Entry coordinates (x, y).
        exit: Exit coordinates (x, y).
        path: Shortest path from entry to exit.
        output_file: Output filename.
    """
    try:
        if not grid:
            raise ValueError("Grid cannot be empty")
        if not path:
            raise ValueError("Path cannot be empty")
        with open(output_file, 'w') as file:
            for row in grid:
                line = ''.join(format(cell, 'X') for cell in row)
                file.write(line + '\n')
            file.write('\n')
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}\n")
            file.write(f"{path}\n")
    except Exception as e:
        print(e)
