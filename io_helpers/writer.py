def write_maze(grid: list[list[int]], entry: tuple[int, int],
               exit: tuple[int, int], path: list[str],
               output_file: str) -> None:
    """Write maze data to a text file in hexadecimal format.

    Args:
        grid: 2D list of cells encoded as wall bitmasks.
        entry: Entry coordinates ``(x, y)``.
        exit: Exit coordinates ``(x, y)``.
        path: Shortest path directions.
        output_file: Destination filename.

    Returns:
        None.
    """
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
        file.write(f"{''.join(path)}\n")
