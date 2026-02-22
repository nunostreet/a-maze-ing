from .cell import ALL_WALLS, DIRECTIONS


def apply_42_pattern(grid: list[list[int]]) -> None:
    """Apply a scalable, centered '42' pattern to the maze grid."""

    height = len(grid)
    width = len(grid[0])

    # Determine scaled digit height
    digit_height = height // 3

    # Ensure minimum structural height
    if digit_height < 5:
        return

    # Determine scaled digit width (with structural minimum)
    digit_width = max(3, digit_height // 2)

    total_width = digit_width * 2 + 2

    # Ensure it fits with at least 1-cell margin on each side
    if total_width > width - 2:
        return

    # Compute centered position
    start_y = (height - digit_height) // 2
    start_x = (width - total_width) // 2

    # Collect pattern cells
    pattern_cells: set[tuple[int, int]] = set()

    _number_4(
        pattern_cells,
        start_x,
        start_y,
        digit_width,
        digit_height)

    _number_2(
        pattern_cells,
        start_x + digit_width + 2,
        start_y,
        digit_width,
        digit_height)

    for x, y in pattern_cells:
        grid[y][x] = ALL_WALLS

        for dx, dy, wall, opposite in DIRECTIONS.values():
            nx = x + dx
            ny = y + dy

            if 0 <= nx < width and 0 <= ny < height:
                grid[ny][nx] |= opposite


def _number_4(cells, x0, y0, w, h):
    mid = y0 + h // 2

    for y in range(y0, y0 + h):
        # Left vertical bar
        if y <= mid:
            cells.add((x0, y))

        # Right vertical bar
        cells.add((x0 + w - 1, y))

    # Middle horizontal bar
    for x in range(x0, x0 + w):
        cells.add((x, mid))


def _number_2(cells, x0, y0, w, h):
    top = y0
    mid = y0 + h // 2
    bot = y0 + h - 1

    # Top horizontal
    for x in range(x0, x0 + w):
        cells.add((x, top))

    # Middle horizontal
    for x in range(x0, x0 + w):
        cells.add((x, mid))

    # Bottom horizontal
    for x in range(x0, x0 + w):
        cells.add((x, bot))

    # Right vertical bar
    for y in range(top + 1, mid):
        cells.add((x0 + w - 1, y))

    # Left vertical bar
    for y in range(mid + 1, bot):
        cells.add((x0, y))
