from abc import ABC, abstractmethod
from ..types import Grid, RNG


class MazeAlgorithm(ABC):
    """Base interface for maze generation strategies."""

    @abstractmethod
    def generate(self, grid: Grid, width: int, height: int, rng: RNG) -> None:
        """Generate a maze by mutating the given grid in place.

        Args:
            grid: Grid of cells encoded as wall bitmasks.
            width: Maze width in cells.
            height: Maze height in cells.
            rng: Random generator used by the algorithm.

        Returns:
            None.
        """
        pass
