import os
import random
from time import sleep
from typing import Any
from maze.types import PatternCells
from maze.generator import MazeGenerator
from maze.cell import NORTH, SOUTH, WEST


def render(grid: list[list[int]],
           entry: tuple[int, int],
           exit: tuple[int, int],
           path: list[str] | None,
           colors: dict[str, str],
           forty_coord: PatternCells) -> None:
    """Render the maze in the terminal using ANSI colors.

        Args:
            grid: 2D list of integers representing the maze.
            entry: Entry coordinates (x, y).
            exit: Exit coordinates (x, y).
            path: List of directions representing the shortest path.
            colors: Dictionary of ANSI color codes for rendering.
            forty_coord: Coordinates occupied by the 42 pattern.

        Returns:
            None.
        """

    # conversão de (x, y) para (y, x) ou (row, column)
    now_coord = (entry[1], entry[0])

    # lista de coordendas N, E, S, W
    path_coord = [now_coord]

    RESET = "\033[0m"

    # percorrer o path e passar de letras para coordenadas
    if path:
        for letter in path:
            row, column = now_coord

            # para cima
            if letter == 'N':
                now_coord = (row - 1, column)

            # para a direita
            elif letter == 'E':
                now_coord = (row, column + 1)

            # para a esquerda
            elif letter == 'W':
                now_coord = (row, column - 1)

            # para baixo
            elif letter == 'S':
                now_coord = (row + 1, column)

            path_coord.append(now_coord)

    for row, rowe in enumerate(grid):
        top_line = ""
        mid_line = ""
        for column, cell in enumerate(rowe):

            # se row e collom forem coordenadas de entrada
            if (row, column) == (entry[1], entry[0]):
                cell_bg = colors['entry_bg']

            # se row e collom forem coordenadas de saida
            elif (row, column) == (exit[1], exit[0]):
                cell_bg = colors['exit_bg']

            # se row e collom estiverem no caminho de path
            elif path_coord and (row, column) in path_coord:
                cell_bg = colors['path']

            # se collom e row estiverem nas coordenadas de pattern 42
            elif (column, row) in forty_coord:
                cell_bg = colors['pattern42']

            else:
                cell_bg = RESET

            # TOP LINE: Canto + Parede Norte (Sempre 2 + 2 espaços)
            top_line += f"{colors['wall']}  {RESET}"
            if cell & NORTH:
                top_line += f"{colors['wall']}  {RESET}"
            else:
                # Caminho vertical
                is_path = (path_coord and (row, column) in path_coord
                           and (row - 1, column) in path_coord)
                top_line += f"{colors['path']}  {RESET}" if is_path else "  "

            # MID LINE: Parede Oeste + Corpo (Sempre 2 + 2 espaços)
            if cell & WEST:
                mid_line += f"{colors['wall']}  {RESET}"
            else:
                # Caminho horizontal
                is_path = (path_coord and (row, column) in path_coord
                           and (row, column - 1) in path_coord)
                mid_line += f"{colors['path']}  {RESET}" if is_path else "  "

            mid_line += f"{cell_bg}  {RESET}"

        # Paredes externas direitas
        top_line += f"{colors['wall']}  {RESET}"
        mid_line += f"{colors['wall']}  {RESET}"
        print(top_line)
        print(mid_line)

    # 3. BOTTOM LINE: Fecho do labirinto
    bottom_line = ""
    for cell in grid[-1]:
        bottom_line += f"{colors['wall']}  {RESET}"
        if cell & SOUTH:
            bottom_line += f"{colors['wall']}  {RESET}"
        else:
            bottom_line += "  "
    # canto direito inferior
    bottom_line += f"{colors['wall']}  {RESET}"
    print(bottom_line)


def animate_path(grid: list[list[int]],
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 path: list[str],
                 colors: dict[str, str],
                 forty_coord: PatternCells) -> None:
    """Animate the shortest path from entry to exit cell by cell.

    Args:
        grid: 2D list of integers representing the maze.
        entry: Entry coordinates (x, y).
        exit: Exit coordinates (x, y).
        path: Sequence of direction letters for the solution.
        colors: Dictionary of ANSI color codes for rendering.
        forty_coord: Coordinates occupied by the 42 pattern.

    Returns:
        None.
    """
    for i in range(1, len(path)):
        os.system('clear')
        # slicing:[start:stop:step] -> path[:i] -> do inicio até i, i vai +
        render(grid, entry, exit, path[:i], colors, forty_coord)
        sleep(0.05)


# menu
def menu(generator: MazeGenerator, config: dict[str, Any]) -> None:
    """Display the interactive menu and handle user interactions.

    Args:
        generator: MazeGenerator instance used to generate and retrieve mazes.
        config: Parsed configuration dictionary with maze parameters.

    Returns:
        None.
    """
    show_path = False
    theme_index = 0
    forty_coord = generator.get_pattern_cells()

    themes = [
        {
            'wall': '\033[47m',      # Paredes Brancas
            'path': '\033[44m',      # Path Azul
            'entry_bg': '\033[41m',  # Entry Vermelho
            'exit_bg': '\033[42m',   # Exit Verde
            'pattern42': '\033[45m'  # 42 pattern rosa
        },
        {
            'wall': '\033[44m',      # Paredes Azul
            'path': '\033[46m',      # Path azul claro
            'entry_bg': '\033[41m',  # Entry Vermelho
            'exit_bg': '\033[42m',   # Exit Verde
            'pattern42': '\033[47m'  # 42 pattern branco
        },
        {
            'wall': '\033[46m',      # Paredes azul claro
            'path': '\033[45m',      # Path Rosa
            'entry_bg': '\033[41m',  # Entry Vermelho
            'exit_bg': '\033[42m',   # Exit Verde
            'pattern42': '\033[41m'  # 42 pattern vermelho
        },
    ]

    while True:
        os.system('clear')

        grid = generator.get_grid()
        path = generator.get_solution() if show_path else None
        render(grid,
               config['ENTRY'],
               config['EXIT'],
               path,
               themes[theme_index],
               forty_coord)

        if generator.pattern_warning:
            print(generator.pattern_warning)

        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            choice = input("Choice? (1-4):")
        except EOFError:
            break

        if choice == '1':

            generator.seed = random.randint(0, 99999)
            generator.generate()
            forty_coord = generator.get_pattern_cells()
            show_path = False

        elif choice == '2':

            show_path = not show_path

            if show_path:
                path = generator.get_solution()
                animate_path(grid,
                             config['ENTRY'],
                             config['EXIT'],
                             path,
                             themes[theme_index],
                             forty_coord)

        elif choice == '3':
            theme_index = (theme_index + 1) % len(themes)
        elif choice == '4':
            break
        else:
            print("Invalid Choice")
