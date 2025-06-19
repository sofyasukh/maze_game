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
    1: {"size": (21, 21), "bonuses": 3},
    2: {"size": (31, 31), "bonuses": 5, "allow_bomb": True},
    3: {"size": (35, 35), "bonuses": 6},
    4: {"size": (39, 39), "bonuses": 7},
    5: {"size": (45, 45), "bonuses": 8},
} 