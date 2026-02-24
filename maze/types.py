# maze/types.py
from __future__ import annotations
from typing import TypedDict
import random

Coord = tuple[int, int]
Grid = list[list[int]]
Move = str
Path = list[Move]
PatternCells = set[Coord]


class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: Coord
    EXIT: Coord
    PERFECT: bool
    SEED: int | None
    CYCLE_DENSITY: float
    ALGORITHM: str


RNG = random.Random
