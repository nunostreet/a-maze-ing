from collections import deque
from .cell import DIRECTIONS
from .types import Grid, Coord, Path


def shortest_path(grid: Grid, start: Coord, end: Coord) -> Path:
    """
    Compute the shortest path between start and end positions
    in a maze using Breadth-First Search (BFS).

    Parameters:
        grid  : 2D list of integers representing the maze.
                Each cell encodes walls using bit flags.
        start : tuple[int, int] representing (x, y) entry position.
        end   : tuple[int, int] representing (x, y) exit position.

    Returns:
        A list of directions ["N", "E", "S", "W"] representing
        the shortest path from start to end.
        Returns an empty list if start == end or no path exists.
    """

    # If start and end are the same, no movement is required.
    if start == end:
        return []

    # Perform BFS
    parent, _ = bfs_parents_and_visited(grid, start)

    # If end was never reached
    if end not in parent and start != end:
        return []

    # Reconstruct path from end back to start
    current = end
    path = []

    while current != start:
        px, py = parent[current]

        # Compute movement direction
        dx = current[0] - px
        dy = current[1] - py

        # Convert coordinate difference to direction letter
        for direction, (ddx, ddy, _, _) in DIRECTIONS.items():
            if (dx, dy) == (ddx, ddy):
                path.append(direction)
                break
        current = (px, py)

    # Reverse to obtain path from start to end
    path.reverse()

    return path


def bfs_parents_and_visited(
    grid: Grid,
    start: Coord,
    blocked: set[Coord] | None = None
) -> tuple[dict[Coord, Coord], set[Coord]]:
    """
    Generic BFS helper:
    - returns parent map (child -> parent)
    - returns visited set from start
    """
    if blocked is None:
        blocked = set()

    if start in blocked:
        return {}, set()

    height = len(grid)
    width = len(grid[0])

    queue = deque([start])
    visited: set[Coord] = {start}
    parent: dict[Coord, Coord] = {}

    while queue:
        x, y = queue.popleft()

        for dx, dy, wall, opposite in DIRECTIONS.values():
            nx, ny = x + dx, y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if (nx, ny) in blocked:
                continue

            # passage open on both sides
            if grid[y][x] & wall == 0 and grid[ny][nx] & opposite == 0:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    return parent, visited
