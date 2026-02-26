import random
from typing import Any
from .cell import ALL_WALLS, DIRECTIONS
from .solver import shortest_path, bfs_parents_and_visited
from .pattern42 import apply_42_pattern
from .algorithms.dfs import DFSAlgorithm
from .algorithms.prim import PrimAlgorithm
from .types import PatternCells, Coord


class MazeGenerator:
    """Generate mazes and expose grid, path, and pattern artifacts."""

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        *,
        width: int | None = None,
        height: int | None = None,
        entry: Coord | None = None,
        exit: Coord | None = None,
        perfect: bool = True,
        seed: int | None = None,
        max_attempts: int = 50,
        cycle_density: float = 0.1,
        algorithm: str = "DFS",
    ) -> None:
        """Initialize a maze generator.

        Args:
            config: Optional legacy configuration map. When provided, values
                are read from this dictionary.
            width: Maze width in cells.
            height: Maze height in cells.
            entry: Entry coordinate (x, y).
            exit: Exit coordinate (x, y).
            perfect: If True, generate a perfect maze (no extra cycles).
            seed: Optional random seed.
            max_attempts: Maximum generation retries before failing.
            cycle_density: Extra cycle probability when perfect is False.
            algorithm: Generation algorithm name ("DFS" or "PRIM").

        Returns:
            None.
        """
        if config is not None:
            width = int(config["WIDTH"])
            height = int(config["HEIGHT"])
            entry = config["ENTRY"]
            exit = config["EXIT"]
            perfect = bool(config["PERFECT"])
            seed = config.get("SEED")
            max_attempts = int(config.get("MAX_ATTEMPTS", max_attempts))
            cycle_density = float(config.get("CYCLE_DENSITY", cycle_density))
            algorithm = str(config.get("ALGORITHM", algorithm))

        if width is None or height is None or entry is None or exit is None:
            raise ValueError(
                "width, height, entry & exit required if config not provided."
            )

        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")
        if max_attempts <= 0:
            raise ValueError("max_attempts must be a positive integer")
        if not (0.0 <= cycle_density <= 1.0):
            raise ValueError("cycle_density must be between 0.0 and 1.0")
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("entry is outside maze bounds")
        if not (0 <= exit[0] < width and 0 <= exit[1] < height):
            raise ValueError("exit is outside maze bounds")
        if entry == exit:
            raise ValueError("entry and exit must be different coordinates")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.max_attempts = max_attempts
        self.cycle_density = cycle_density

        # Will store the 2D maze structure
        self.grid: list[list[int]] = []

        # Will store the computed shortest path
        self.solution: list[str] = []
        self.pattern_cells: PatternCells = set()

        # Storing warnings
        self.pattern_warning: str | None = None

        algo_name = algorithm.upper()

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
        """Build a valid maze grid and compute the shortest solution path.

        Retries generation until all structural constraints are satisfied, or
        raises an error after the configured attempt limit.

        Returns:
            None.
        """

        allow_pattern = self._can_fit_42_pattern()
        use_pattern = allow_pattern

        self.pattern_warning = None

        if not allow_pattern:
            self.pattern_warning = "42 pattern omitted: maze too small."

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
            if use_pattern:
                candidate_pattern = apply_42_pattern(self.grid)
                if not candidate_pattern:
                    self.pattern_cells = set()
                    use_pattern = False
                elif (
                    self.entry in candidate_pattern
                        or self.exit in candidate_pattern
                        ):
                    self.pattern_warning = "42 pattern omitted: " \
                        "ENTRY/EXIT overlaps the pattern"
                else:
                    self.pattern_cells = candidate_pattern
            else:
                self.pattern_cells = set()

            # STEP 5: Check no cells were blocked because of 42 pattern
            self._ensure_only_pattern_cells_are_fully_blocked()
            if not self._only_pattern_cells_fully_blocked():
                continue

            # STEP 6: Ensure there are no isolated blocks:
            self._ensure_no_isolated_blocks()
            if not self._check_isolated_cells():
                continue

            # STEP 7: Ensure there are no forbidden 3x3 open areas
            if self._has_open_3x3():
                continue

            # STEP 8: Compute shortest path using BFS and check solution exists
            self.solution = shortest_path(self.grid, self.entry, self.exit)
            if self.solution or self.entry == self.exit:
                return

        # Raise error if max attemps were reached
        raise RuntimeError("Could not generate a valid maze.")

    def get_grid(self) -> list[list[int]]:
        """Return a defensive copy of the current maze grid.

        Returns:
            2D list of cell wall bitmasks.
        """
        return [row[:] for row in self.grid]

    def get_solution(self) -> list[str]:
        """Return a copy of the shortest path from entry to exit.

        Returns:
            List of move symbols (for example ``"N"``, ``"E"``, ``"S"``,
            ``"W"``). May be empty when no path is available yet.
        """
        return list(self.solution)

    def get_pattern_cells(self) -> PatternCells:
        """Return a copy of coordinates occupied by the ``42`` pattern.

        Returns:
            Set of pattern coordinates.
        """
        return set(self.pattern_cells)

    # ================================================
    # Internal helpers
    # ================================================

    def _init_grid(self) -> None:
        """Initialize the internal grid with all walls closed.

        Returns:
            None.
        """
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    # ===========================
    # Helper para STEP 2
    # ===========================

    def _rng_for_attempt(self, attempt: int) -> random.Random:
        """Build a random generator for the current attempt.

        Args:
            attempt: Zero-based retry number.

        Returns:
            A deterministic RNG when SEED is set, otherwise a fresh RNG.
        """
        # Deterministic retries when seed exists
        if self.seed is not None:
            return random.Random(self.seed + attempt)
        # Non-deterministic retries when seed is not provided
        return random.Random()

    # ===========================
    # Helper para STEP 3
    # ===========================

    def _add_cycles_with_rng(self, rng: random.Random) -> None:
        """Add random passages to introduce cycles in non-perfect mazes.

        Args:
            rng: Random generator used to decide extra openings.

        Returns:
            None.
        """

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
    # Helper para STEP 4
    # ===========================

    def _can_fit_42_pattern(self) -> bool:
        """Check whether current dimensions can host the ``42`` pattern.

        Returns:
            True when the pattern fits with required margins, False otherwise.
        """
        digit_height = self.height // 3
        if digit_height < 5:
            return False

        digit_width = max(3, digit_height // 2)
        total_width = digit_width * 2 + 2
        return bool(total_width <= self.width - 2)

    # ===========================
    # Helper para STEP 5
    # ===========================

    def _ensure_only_pattern_cells_are_fully_blocked(self) -> None:
        """Open any fully blocked non-pattern cell by carving one valid edge.

        Returns:
            None.
        """
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
        """Validate that only pattern cells remain fully blocked.

        Returns:
            True when every ``ALL_WALLS`` cell belongs to the pattern.
        """
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
        """Collect traversable coordinates excluding blocked pattern cells.

        Returns:
            Set of valid coordinates.
        """
        return {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.pattern_cells
        }

    def _check_isolated_cells(self) -> bool:
        """Check whether all traversable cells are connected.

        Returns:
            True if every non-pattern cell is reachable from ENTRY,
            False otherwise.
        """
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
        """Connect disconnected traversable components to the entry component.

        Returns:
            None.
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

    # ===========================
    # Helper para STEP 7
    # ===========================

    def _is_passage_open(
        self,
        x: int,
        y: int,
        nx: int,
        ny: int
    ) -> bool:
        """Check whether two adjacent cells are mutually open.

        Args:
            x: Source cell x coordinate.
            y: Source cell y coordinate.
            nx: Neighbor cell x coordinate.
            ny: Neighbor cell y coordinate.

        Returns:
            True when passage is open in both cells, False otherwise.
        """
        dx = nx - x
        dy = ny - y

        for ddx, ddy, wall, opposite in DIRECTIONS.values():
            if (dx, dy) == (ddx, ddy):
                return (
                    (self.grid[y][x] & wall) == 0
                    and (self.grid[ny][nx] & opposite) == 0
                )
        return False

    def _is_open_3x3_window(self, x0: int, y0: int) -> bool:
        """Check if a 3x3 window is fully open and pattern-free.

        Args:
            x0: Leftmost x coordinate of the window.
            y0: Top y coordinate of the window.

        Returns:
            True when all internal adjacencies are open and no cell belongs
            to the ``42`` pattern.
        """
        window_cells: set[Coord] = {
            (x0 + dx, y0 + dy)
            for dy in range(3)
            for dx in range(3)
        }

        if any(cell in self.pattern_cells for cell in window_cells):
            return False

        # Check 6 horizontal internal adjacencies.
        for y in range(y0, y0 + 3):
            for x in range(x0, x0 + 2):
                if not self._is_passage_open(x, y, x + 1, y):
                    return False

        # Check 6 vertical internal adjacencies.
        for x in range(x0, x0 + 3):
            for y in range(y0, y0 + 2):
                if not self._is_passage_open(x, y, x, y + 1):
                    return False

        return True

    def _has_open_3x3(self) -> bool:
        """Detect whether the maze contains a forbidden open 3x3 area.

        Returns:
            True when at least one invalid 3x3 open area exists.
        """
        for y0 in range(self.height - 2):
            for x0 in range(self.width - 2):
                if self._is_open_3x3_window(x0, y0):
                    return True
        return False
