from collections import deque
from .cell import DIRECTIONS
from .types import Grid, Coord, Path


def shortest_path(grid: Grid, start: Coord, end: Coord) -> Path:
    """Compute the shortest path from ``start`` to ``end`` using BFS.

    Args:
        grid: Maze grid encoded as wall bitmasks.
        start: Entry coordinate ``(x, y)``.
        end: Exit coordinate ``(x, y)``.

    Returns:
        List of direction letters from start to end. Returns an empty list
        when ``start == end`` or when no path exists.
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
    """Run BFS and return both parent links and visited coordinates.

    Args:
        grid: Maze grid encoded as wall bitmasks.
        start: Start coordinate ``(x, y)``.
        blocked: Coordinates that BFS should treat as unavailable.

    Returns:
        Tuple ``(parent, visited)`` where ``parent`` maps a node to its
        predecessor and ``visited`` contains all reached coordinates.
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
