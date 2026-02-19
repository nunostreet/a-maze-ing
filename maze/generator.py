from .cell import ALL_WALLS, DIRECTIONS


class MazeGenerator:
    def __init__(self, config):
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.seed = config.seed
        
        self.grid = []
        self.solution = []

    def generate(self) -> None:
        self._init_grid()

    def get_grid(self) -> list[list[int]]:
        self.grid = [
            [ALL_WALLS for _ in range (self.width)]
            for _ in range(self.height)
        ]
        return self.grid

    def get_solution(self) -> list[str]:
        ...