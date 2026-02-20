from .cell import ALL_WALLS, DIRECTIONS
from .solver import shortest_path
import random


class MazeGenerator:
    """Class responsible for generating and storing a maze."""

    def __init__(self, config) -> None:
        """
        Store configuration values needed for maze generation.
        """
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.seed = config.get("SEED")
        self._random = random.Random(self.seed)

        # Will store the 2D maze structure
        self.grid: list[list[int]] = []

        # Will store the computed shortest path
        self.solution: list[str] = []

    # --------- PUBLIC API --------- #

    def generate(self) -> None:
        """Generate the maze structure and compute its solution."""

        # Create a 2D grid (height rows, width columns)
        # Each cell starts with ALL_WALLS (0b1111)
        self._init_grid()
        self._generate_dfs()
        
        # Compute shortest path using BGS
        self.solution = shortest_path(self.grid, self.entry, self.exit)

    def _init_grid(self) -> None:
        """Initialize grid with all walls closed."""
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _generate_dfs(self) -> None:
        """Generate a perfect maze using DFS (recursive backtracker)."""

        def in_bounds(x: int, y: int) -> bool:
            return 0 <= x < self.width and 0 <= y < self.height
        
        x, y = 0, 0

        # Here we create the set to store all visited cells
        # Set will help us avoid getting duplicates
        visited: set[tuple[int, int]] = {(x, y)}
        # We also need to create a stack which will help us check for neighbors.
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
                nx, ny, wall, opposite = self._random.choice(neighbors)

                self.grid[y][x] &= ~wall
                self.grid[ny][nx] &= ~opposite

                visited.add((nx, ny))
                stack.append((nx, ny))

            # Cell only leaves stack if no neighbors left
            else:
                stack.pop()

    def get_grid(self) -> list[list[int]]:
        """
        Return the current maze grid.
        This method does NOT modify the grid.
        """
        return self.grid

    def get_solution(self) -> list[str]:
        """
        Return the shortest path (if computed).
        """
        return self.solution
    

    # LINK https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
    # LINK https://www.kaggle.com/code/mexwell/maze-runner-shortest-path-algorithms
