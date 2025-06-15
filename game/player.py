import pygame
from constants import CELL_SIZE, PLAYER_SIZE

class Player:
    def __init__(self, x, y, exit_pos):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.exit_pos = exit_pos
        self.has_reached_exit = False

    @property
    def grid_pos(self):
        """Возвращает текущую позицию в клетках лабиринта (колонка, строка)"""
        return (self.rect.x // CELL_SIZE, self.rect.y // CELL_SIZE)

    def move(self, dx, dy, maze_grid):
        """Движение игрока с проверкой стен"""
        new_x = self.rect.x + dx * CELL_SIZE
        new_y = self.rect.y + dy * CELL_SIZE
        grid_x, grid_y = new_x // CELL_SIZE, new_y // CELL_SIZE

        if 0 <= grid_x < len(maze_grid[0]) and 0 <= grid_y < len(maze_grid):
            if maze_grid[grid_y][grid_x] == 0:  # Если клетка проходима
                self.rect.x = new_x
                self.rect.y = new_y
                self._check_exit_reached(grid_x, grid_y)
                return True
        return False

    def _check_exit_reached(self, grid_x, grid_y):
        """Проверяет, достиг ли игрок выхода"""
        if (grid_x, grid_y) == self.exit_pos:
            self.has_reached_exit = True

    def teleport(self, x, y):
        """Телепортация игрока в указанные координаты"""
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self._check_exit_reached(x, y)