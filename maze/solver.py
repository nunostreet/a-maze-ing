from .cell import DIRECTIONS
from collections import deque


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
        x, y = queue.popleft()

        # Stop BFS as soon as we reach the target
        if (x, y) == end:
            break

        # Explore all possible directions
        for dx, dy, wall, opposite in DIRECTIONS.values():
            nx = x + dx
            ny = y + dy

            # Check if neighbor is inside maze boundaries
            if 0 <= nx < width and 0 <= ny < height:

                # Check both sides of the wall
                # if bit is 0, passage is open
                if grid[y][x] & wall == 0 and (grid[ny][nx] & opposite) == 0:

                    # Visit only unvisited cells
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

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
