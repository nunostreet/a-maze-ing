from .cell import ALL_WALLS, DIRECTIONS
from .solver import shortest_path, bfs_parents_and_visited
from .pattern42 import apply_42_pattern
from .algorithms.dfs import DFSAlgorithm
from .algorithms.prim import PrimAlgorithm
from .types import PatternCells, Coord
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
        self.max_attempts = config.get("MAX_ATTEMPTS", 50)

        # Optional cycle density (only used if PERFECT=False)
        self.cycle_density = config.get("CYCLE_DENSITY", 0.1)

        # Will store the 2D maze structure
        self.grid: list[list[int]] = []

        # Will store the computed shortest path
        self.solution: list[str] = []
        self.pattern_cells: PatternCells = set()

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

        for attempt in range(self.max_attempts):
            rng = self._rng_for_attempt(attempt)

            # STEP 1: Create a 2D grid (height rows, width columns)
            # Each cell starts with ALL_WALLS (0b1111)
            self._init_grid()

            # STEP 2: Generate perfect maze
            self.algorithm.generate(
                self.grid,
                self.width,
                self.height,
                rng
            )

            # STEP 3: Add cycles if requested
            if not self.perfect:
                self._add_cycles_with_rng(rng)

            # STEP 4: Apply the 42 pattern on top
            self.pattern_cells = apply_42_pattern(self.grid)
            if not self.pattern_cells:
                continue

            # STEP 5: Check no cells were blocked because of 42 pattern
            self._ensure_only_pattern_cells_are_fully_blocked()
            if not self._only_pattern_cells_fully_blocked():
                continue

            # STEP 6: Ensure there are no isolated blocks:
            self._ensure_no_isolated_blocks()
            if not self._check_isolated_cells():
                continue

            # ADICIONAR O CHECK 3X3

            # STEP 7: Compute shortest path using BFS and check solution exists
            self.solution = shortest_path(self.grid, self.entry, self.exit)
            if self.solution or self.entry == self.exit:
                return

        # Raise error if max attemps were reached
        raise RuntimeError("Could not generate a valid maze with 42 pattern")

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

    def get_pattern_cells(self) -> PatternCells:
        """Return cells belonging to the rendered 42 pattern."""
        return set(self.pattern_cells)

    # ================================================
    # Internal helpers
    # ================================================

    def _init_grid(self) -> None:
        """Initialize grid with all walls closed."""
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    # ===========================
    # Helper para STEP 2
    # ===========================

    def _rng_for_attempt(self, attempt: int) -> random.Random:
        # Deterministic retries when seed exists
        if self.seed is not None:
            return random.Random(self.seed + attempt)
        # Non-deterministic retries when seed is not provided
        return random.Random()

    # ===========================
    # Helper para STEP 3
    # ===========================

    def _add_cycles_with_rng(self, rng: random.Random) -> None:
        """Adds random extra connections to create cycles if PERFECT=False."""

        for y in range(self.height):
            for x in range(self.width):

                # Try all possible directions from the current cell
                for direction in ("E", "S"):
                    dx, dy, wall, opposite = DIRECTIONS[direction]

                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if rng.random() < self.cycle_density:
                            self.grid[y][x] &= ~wall
                            self.grid[ny][nx] &= ~opposite

    # ===========================
    # Helper para STEP 5
    # ===========================

    def _ensure_only_pattern_cells_are_fully_blocked(self) -> None:
        """Ensure no non-pattern cell remains fully blocked."""
        for y in range(self.height):
            for x in range(self.width):
                # Skip if cell is in pattern cells
                if (x, y) in self.pattern_cells:
                    continue
                # Skip if it's not all walls
                if self.grid[y][x] != ALL_WALLS:
                    continue
                # Open one of the walls and continue
                for direction in ("N", "E", "S", "W"):
                    dx, dy, wall, opposite = DIRECTIONS[direction]

                    nx = x + dx
                    ny = y + dy

                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue
                    if (nx, ny) in self.pattern_cells:
                        continue

                    self.grid[y][x] &= ~wall
                    self.grid[ny][nx] &= ~opposite
                    break

    def _only_pattern_cells_fully_blocked(self) -> bool:
        """Return True iff only pattern cells are fully blocked (ALL_WALLS)."""
        for y in range(self.height):
            for x in range(self.width):
                if (
                    (x, y) not in self.pattern_cells
                    and self.grid[y][x] == ALL_WALLS
                ):
                    return False

        return True

    # ===========================
    # Helper para STEP 6
    # ===========================

    def _check_valid_cells(self) -> set[Coord]:
        """Cells that are allowed to be traversed (except pattern)."""
        return {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.pattern_cells
        }

    def _check_isolated_cells(self) -> bool:
        valid_cells = self._check_valid_cells()
        if not valid_cells:
            return True

        # If ENTRY is blocked by pattern, maze is invalid for this attempt
        if self.entry not in valid_cells:
            return False

        _, visited = bfs_parents_and_visited(
            self.grid,
            self.entry,
            blocked=self.pattern_cells
        )
        return visited == valid_cells

    def _ensure_no_isolated_blocks(self) -> None:
        """
        Connect disconnected valid components to the ENTRY component by
        opening one wall at a time between adjacent components.
        """
        valid_cells = self._check_valid_cells()
        if not valid_cells or self.entry not in valid_cells:
            return

        _, visited = bfs_parents_and_visited(
            self.grid,
            self.entry,
            blocked=self.pattern_cells
        )

        while visited != valid_cells:
            isolated = valid_cells - visited
            connected = False

            for x, y in visited:
                for direction in ("N", "E", "S", "W"):
                    dx, dy, wall, opposite = DIRECTIONS[direction]

                    nx = x + dx
                    ny = y + dy

                    if (nx, ny) not in isolated:
                        continue

                    self.grid[y][x] &= ~wall
                    self.grid[ny][nx] &= ~opposite
                    connected = True
                    break

                if connected:
                    break

            if not connected:
                break

            _, visited = bfs_parents_and_visited(
                self.grid,
                self.entry,
                blocked=self.pattern_cells
            )
