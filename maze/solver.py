from .cell import DIRECTIONS
from collections import deque


# Mapping from coordinate differences to cardinal directions.
# Used when reconstructing the path.
DIR_MAP = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}


def shortest_path(grid, start, end) -> list[str]:
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

    # BFS initialization
    queue = deque([start])
    visited = {start}
    parent = {}

    height = len(grid)
    width = len(grid[0])

    # Perform BFS
    while queue:
        current = queue.popleft()

        # Stop BFS as soon as we reach the target
        if current == end:
            break

        x, y = current

        # Explore all possible directions
        for dx, dy, wall, opposite in DIRECTIONS.values():
            nx = x + dx
            ny = y + dy

            # Check if neighbor is inside maze boundaries
            if 0 <= nx < width and 0 <= ny < height:

                # Check if there is no wall in this direction
                # if bit is 0, passage is open
                if grid[y][x] & wall == 0:

                    # Visit only unvisited cells
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = current
                        queue.append((nx, ny))

    # If end was never reached
    if end not in parent and start != end:
        return []

    # Reconstruct path from end back to start
    current = end
    directions = []

    while current != start:
        prev = parent[current]

        # Compute movement direction
        dx = current[0] - prev[0]
        dy = current[1] - prev[1]

        # Convert coordinate difference to direction letter
        directions.append(DIR_MAP[(dx, dy)])

        current = prev

    # Reverse to obtain path from start to end
    directions.reverse()

    return directions
