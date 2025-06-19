# Конфигурация игры
import pygame

# Размеры окна
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CELL_SIZE = 30

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

# Состояния игры
MENU = "menu"
PLAYING = "playing"
VICTORY = "victory"
GAME_OVER = "game_over"

# Типы бонусов
FREEZE = "freeze"
TELEPORT = "teleport"
PATH_HINT = "path_hint"
BOMB = "bomb"

# Уровни
LEVELS = {
    1: {"size": (17, 17), "bonuses": 3},
    2: {"size": (23, 23), "bonuses": 4},
    3: {"size": (29, 17), "bonuses": 5, "allow_bomb": True},
    4: {"size": (35, 35), "bonuses": 6, "allow_bomb": True},
    5: {"size": (41, 41), "bonuses": 7, "allow_bomb": True},
} 