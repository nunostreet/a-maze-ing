from .base import MazeAlgorithm
from ..cell import DIRECTIONS
from ..types import Grid, RNG


class PrimAlgorithm(MazeAlgorithm):
    """Generate mazes with randomized Prim's algorithm."""

    def generate(self, grid: Grid, width: int, height: int, rng: RNG) -> None:
        """Generate a perfect maze using randomized Prim's algorithm.

        Args:
            grid: Grid of cells encoded as wall bitmasks.
            width: Maze width in cells.
            height: Maze height in cells.
            rng: Random generator used for wall selection.

        Returns:
            None.
        """

        def in_bounds(x: int, y: int) -> bool:
            """Check whether a coordinate is inside the maze boundaries.

            Args:
                x: Horizontal coordinate.
                y: Vertical coordinate.

            Returns:
                True when the coordinate is valid, False otherwise.
            """
            return 0 <= x < width and 0 <= y < height

        start = (0, 0)

        # Here we create the set to store all visited cells
        # Set will help us avoid getting duplicates
        visited: set[tuple[int, int]] = {start}
        # We also need to create a stack to help check for neighbors.
        walls = []

        # Add initial walls
        x, y = start
        for dx, dy, wall, opposite in DIRECTIONS.values():
            nx = x + dx
            ny = y + dy
            if in_bounds(nx, ny):
                walls.append((x, y, nx, ny, wall, opposite))

        while walls:
            # We pick a random wall
            index = rng.randrange(len(walls))
            x, y, nx, ny, wall, opposite = walls.pop(index)

            if (nx, ny) not in visited:
                grid[y][x] &= ~wall
                grid[ny][nx] &= ~opposite

                visited.add((nx, ny))

                # Add new walls
                for dx, dy, w, opp in DIRECTIONS.values():
                    nnx, nny = nx + dx, ny + dy
                    if in_bounds(nnx, nny) and (nnx, nny) not in visited:
                        walls.append((nx, ny, nnx, nny, w, opp))
