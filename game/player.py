import pygame
from constants import CELL_SIZE, PLAYER_SIZE

class Player:
    def __init__(self, x, y, exit_pos):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.exit_pos = exit_pos
        self.has_reached_exit = False

    def move(self, dx, dy, maze_grid):
        # Логика движения
        pass