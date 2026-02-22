from .base import MazeAlgorithm
from ..cell import DIRECTIONS
from ..types import Grid, RNG


class DFSAlgorithm(MazeAlgorithm):
    def generate(self, grid: Grid, width: int, height: int, rng: RNG) -> None:
        """Generate a perfect maze using DFS (recursive backtracker)."""

        def in_bounds(x: int, y: int) -> bool:
            return 0 <= x < width and 0 <= y < height

        x, y = 0, 0

        # Here we create the set to store all visited cells
        # Set will help us avoid getting duplicates
        visited: set[tuple[int, int]] = {(x, y)}
        # We also need to create a stack to help check for neighbors.
        stack: list[tuple[int, int]] = [(x, y)]

        # While we have cells in the current path
        while stack:
            # This is our starting point to create the maze
            x, y = stack[-1]
            neighbors = []

            # For each entry in the dictionary, get the associate values
            for dx, dy, wall, opposite in DIRECTIONS.values():
                nx = x + dx
                ny = y + dy

                # We test all valid directions and store in neighbors
                if in_bounds(nx, ny) and (nx, ny) not in visited:
                    neighbors.append((nx, ny, wall, opposite))

            if neighbors:
                # We choose one of the random cells in neigbhors
                nx, ny, wall, opposite = rng.choice(neighbors)

                grid[y][x] &= ~wall
                grid[ny][nx] &= ~opposite

                visited.add((nx, ny))
                stack.append((nx, ny))

            # Cell only leaves stack if no neighbors left
            else:
                stack.pop()
