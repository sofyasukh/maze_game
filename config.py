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

# Игровые параметры
PLAYER_SPEED = 5
BOMB_EXPLOSION_RADIUS = 3
FOG_OF_WAR_RADIUS = {
    4: 5,  # Для 4 уровня
    5: 3   # Для 5 уровня
}

# Константы для лабиринта
WALL = 1
PATH = 0

# Уровни
LEVELS = {
    1: {"size": (17, 17), "bonuses": 3, "wall_change_interval": 3000},
    2: {"size": (23, 23), "bonuses": 4, "wall_change_interval": 2500},
    3: {"size": (29, 17), "bonuses": 5, "allow_bomb": True, "wall_change_interval": 2000},
    4: {"size": (35, 35), "bonuses": 6, "allow_bomb": True, "wall_change_interval": 1500},
    5: {"size": (41, 41), "bonuses": 7, "allow_bomb": True, "wall_change_interval": 1000},
} 