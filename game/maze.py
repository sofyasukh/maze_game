import random
from constants import CELL_SIZE

class Maze:
    def __init__(self, width, height):
        self.width = width // CELL_SIZE
        self.height = height // CELL_SIZE
        self.grid = self._generate_maze()

    def _generate_maze(self):
        # Генерация лабиринта
        pass