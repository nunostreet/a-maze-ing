from .cell import ALL_WALLS
import random


class MazeGenerator:
    """Class responsible for generating and storing a maze."""

    def __init__(self, config) -> None:
        """
        Store configuration values needed for maze generation.
        Nothing is generated here.
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

    def generate(self) -> None:
        """
        Generate the maze structure.

        For now, this only initializes the grid
        with all walls closed.
        Later, this method will:
        - Run the DFS algorithm
        - Apply 42 pattern
        - Compute shortest path
        """

        # Create a 2D grid (height rows, width columns)
        # Each cell starts with ALL_WALLS (0b1111)
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

        # LINK https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
        # LINK https://www.kaggle.com/code/mexwell/maze-runner-shortest-path-algorithms

        x = 0
        y = 0

        def in_bounds(x, y) -> bool:
            return 0 <= x < self.width and 0 <= y < self.height

        # Here we create the set to store all visited cells.
        # Set will help us avoid getting duplicates
        visited: set[tuple[int, int]] = set()
        # We also need to create a stack which will help us check for neighbors.
        stack: list[tuple[int, int]] = []

        visited.add((x, y))
        stack.append((x, y))

        while stack:
            x, y = stack[-1]

            if not in_bounds(x, y) or visited((x,y))




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
