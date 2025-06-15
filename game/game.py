import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE
from .maze import Maze
from .player import Player

class Game:
    def __init__(self, screen, difficulty, completion_callback):
        self.screen = screen
        self.difficulty = difficulty
        self.completion_callback = completion_callback
        self.maze = Maze(screen.get_width(), screen.get_height())
        self.player = Player(CELL_SIZE, CELL_SIZE, (self.maze.width-2, self.maze.height-2))
        self.running = True

    def update(self, dt):
        # Логика обновления игры
        pass

    def draw(self):
        # Отрисовка игры
        pass