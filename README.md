*This project has been created as part of the 42 curriculum by nstreet-, pedde-al.*

# A-Maze-ing

## Description
A-Maze-ing is a Python project that generates and solves mazes.

Project goal:
- Generate valid mazes from a config file.
- Guarantee structural constraints (no isolated traversable zones, no forbidden open 3x3 areas, controlled blocked pattern cells).
- Compute a shortest path from entry to exit.
- Export the maze to file and provide an ASCII interactive visualization.

High-level overview:
- Core generator: `MazeGenerator` in `maze/generator.py`.
- Generation algorithms: DFS and randomized Prim (`maze/algorithms/`).
- Solver: BFS shortest path (`maze/solver.py`).
- Optional centered scalable `42` blocked pattern (`maze/pattern42.py`).
- CLI entrypoint: `a_maze_ing.py`.

## Instructions

### Prerequisites
- Python 3.10+
- `make`

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

### Run
```bash
make run
# or with a custom config path
make run CONFIG=path/to/config.txt
```

### Lint
```bash
make lint
make lint-strict
```

### Build the reusable package (`mazegen-*`)
```bash
make package
```

Generated artifacts:
- Build outputs in `dist/`:
  - `dist/mazegen_amazeing-1.0.0-py3-none-any.whl`
  - `dist/mazegen_amazeing-1.0.0.tar.gz`
- One selected distributable is also copied to repository root for evaluation:
  - default: `mazegen_amazeing-1.0.0-py3-none-any.whl`
  - or use tarball: `make package PACKAGE_KIND=tar`

## Config File Structure (Complete)
Expected format: one `KEY=VALUE` pair per line, optional comments with `#`.

Mandatory keys:
- `WIDTH=<int>`: maze width (`> 0`)
- `HEIGHT=<int>`: maze height (`> 0`)
- `ENTRY=x,y`: entry coordinate inside bounds
- `EXIT=x,y`: exit coordinate inside bounds and different from `ENTRY`
- `OUTPUT_FILE=<name>.txt`: output file path/name ending in `.txt`
- `PERFECT=True|False`: whether to keep a perfect maze (no extra cycles)
- `SEED=<int>`: deterministic generation seed

Optional keys:
- `ALGORITHM=DFS|PRIM` (default `DFS`)
- `CYCLE_DENSITY=<float>` in `[0.0, 0.3]` (used when `PERFECT=False`)

Example:
```txt
WIDTH=30
HEIGHT=20
ENTRY=0,0
EXIT=29,19
OUTPUT_FILE=output.txt
PERFECT=False
SEED=42
ALGORITHM=PRIM
CYCLE_DENSITY=0.15
```

## Maze Generation Algorithm Chosen
Primary chosen algorithm: **DFS (recursive backtracker)**.

Also implemented as an advanced feature:
- **Randomized Prim** (`ALGORITHM=PRIM`)

## Why This Algorithm
Why DFS was selected as primary:
- Simple, reliable, and easy to validate for perfect maze generation.
- Produces long corridors and clear backtracking behavior.
- Efficient for the project constraints and straightforward to maintain.

Why Prim was added:
- Provides a second valid topology style.
- Useful for experimentation and comparison.

## Reusable Code and How
Reusable module/package:
- Package: `mazegen-amazeing` (distribution name matching `mazegen-*`).
- Reusable API entrypoint: `maze.MazeGenerator`.

How to reuse:
```python
from maze import MazeGenerator

gen = MazeGenerator(
    width=30,
    height=20,
    entry=(0, 0),
    exit=(29, 19),
    seed=42,
    algorithm="DFS",
)
gen.generate()

grid = gen.get_grid()          # internal maze structure (bitmask per cell)
solution = gen.get_solution()  # shortest path as ["N", "E", "S", "W", ...]
```

Notes:
- The internal `grid` format is reusable programmatically and does not need to match output-file text format.
- Legacy compatibility is kept: `MazeGenerator(config_dict)` is still supported.

## Advanced Features Implemented
- Multiple generation algorithms: DFS and PRIM.
- Optional cycle injection (`PERFECT=False` with `CYCLE_DENSITY`).
- Optional centered scalable `42` blocked pattern.
- Structural post-validation and repair helpers.
- Interactive ASCII visualization with path animation and theme rotation.

## Team and Project Management

### Team Roles
- `nstreet-`: core maze module (`maze/`) including generation logic, algorithms, solver integration, and reusable API behavior.
- `pedde-al`: configuration parsing, output writing, and terminal visualization/interaction.

### Planning: Expected vs Actual
- Initial split was defined from the start:
  - one side focused on maze core/generation;
  - the other side focused on parsing, output, and visualization.
- This plan stayed stable until delivery, with minor iteration mostly on interfaces and validation details.
- Integration was smooth because both sides consistently aligned on what each part should receive and return.

### Retrospective
- What worked well:
  - clear ownership boundaries from day one;
  - continuous alignment on module inputs/outputs;
  - straightforward final integration between subsystems.
- What could be improved:
  - define stricter integration test checkpoints earlier;
  - lock a final packaging/release checklist sooner.

### Tools Used
Current technical tools:
- Python, Makefile
- flake8, mypy
- Git/GitHub

Collaboration/management tools:
- GitHub
- Google Drive
- Slack

## Resources
Classic references:
- DFS maze generation background: https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
- BFS shortest path examples: https://www.kaggle.com/code/mexwell/maze-runner-shortest-path-algorithms
- ANSI terminal colors: https://en.wikipedia.org/wiki/ANSI_escape_code

### AI Usage Disclosure
AI was used as an assistant for:
- debugging support;
- docstring quality/tuning;
- running bulk test ideas and edge-case checks;
- final code review support;
- robustness and improvement suggestions.

AI was **not** used to replace manual project decisions; final design/validation/integration choices were made by the team.
