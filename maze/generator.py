from .cell import ALL_WALLS, DIRECTIONS
from .solver import shortest_path
from .pattern42 import apply_42_pattern
from .algorithms.dfs import DFSAlgorithm
from .algorithms.prim import PrimAlgorithm
import copy
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

        # Optional cycle density (only used if PERFECT=False)
        self.cycle_density = config.get("CYCLE_DENSITY", 0.1)

        self._random = random.Random(self.seed)

        # Will store the 2D maze structure
        self.grid: list[list[int]] = []

        # Will store the computed shortest path
        self.solution: list[str] = []

        algo_name = config.get("ALGORITHM", "DFS")

        algorithms = {
            "DFS": DFSAlgorithm,
            "PRIM": PrimAlgorithm
        }

        if algo_name not in algorithms:
            raise ValueError(f"Unknown algorithm: {algo_name}")

        self.algorithm = algorithms[algo_name]()

    # ================================================
    # PUBLIC API
    # ================================================

    def generate(self) -> None:
        """Generate the maze structure and compute its solution."""

        # STEP 1: Create a 2D grid (height rows, width columns)
        # Each cell starts with ALL_WALLS (0b1111)
        self._init_grid()

        # STEP 2: Generate perfect maze
        self.algorithm.generate(
            self.grid,
            self.width,
            self.height,
            self._random
        )

        # STEP 3: Add cycles if requested
        if not self.perfect:
            self._add_cycles()

        # STEP 4: Try to apply the 42 pattern safely
        original_grid = copy.deepcopy(self.grid)

        apply_42_pattern(self.grid)

        # STEP 5: Compute shortest path using BFS
        solution = shortest_path(self.grid, self.entry, self.exit)

        # STEP 6: If 42 broke connectivity, revert
        if not solution and self.entry != self.exit:
            self.grid = original_grid
            self.solution = shortest_path(
                self.grid,
                self.entry,
                self.exit
            )
        else:
            self.solution = solution

    def get_grid(self) -> list[list[int]]:
        """
        Return the current maze grid.
        This method does NOT modify the grid.
        """
        return [row[:] for row in self.grid]

    def get_solution(self) -> list[str]:
        """
        Return the shortest path (if computed).
        """
        return list(self.solution)

    # ================================================
    # Internal helpers
    # ================================================

    def _init_grid(self) -> None:
        """Initialize grid with all walls closed."""
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _add_cycles(self) -> None:
        """Adds random extra connections to create cycles if PERFECT=False."""

        for y in range(self.height):
            for x in range(self.width):

                # Try all possible directions from the current cell
                for direction in ("E", "S"):
                    dx, dy, wall, opposite = DIRECTIONS[direction]

                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self._random.random() < self.cycle_density:
                            self.grid[y][x] &= ~wall
                            self.grid[ny][nx] &= ~opposite
