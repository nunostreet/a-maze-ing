from abc import ABC, abstractmethod
from maze.types import Grid, RNG


class MazeAlgorithm(ABC):
    """Abstract base class for maze generation algorithms."""

    @abstractmethod
    def generate(self, grid: Grid, width: int, height: int, rng: RNG) -> None:
        """Modify the grid in-place to generate a maze."""
        pass
