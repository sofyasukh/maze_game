# Используем абсолютный импорт
from constants import BLUE, PURPLE, YELLOW, CELL_SIZE
import random

class Bonus:
    def __init__(self, maze_grid):
        self.type = random.choice(['freeze', 'teleport', 'path_hint'])
        self.color = {
            'freeze': BLUE,
            'teleport': PURPLE,
            'path_hint': YELLOW
        }[self.type]
        self.pos = self._place_bonus(maze_grid)
        self.active = False

    def _place_bonus(self, grid):
        empty_cells = [
            (x, y) for y in range(len(grid)) 
            for x in range(len(grid[0])) 
            if grid[y][x] == 0
        ]
        return random.choice(empty_cells)