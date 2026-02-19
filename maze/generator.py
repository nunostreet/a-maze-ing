from .cell import ALL_WALLS


class MazeGenerator:
    """Class responsible for generating and storing a maze."""

    def __init__(self, config) -> None:
        """
        Store configuration values needed for maze generation.
        Nothing is generated here.
        """
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.seed = config.seed

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
