# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Размеры объектов
CELL_SIZE = 30
PLAYER_SIZE = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Добавлен желтый цвет

# Уровни сложности
EASY = {"fog": False, "wall_change_time": 10, "visibility": 100}
MEDIUM = {"fog": True, "wall_change_time": 7, "visibility": 70}
HARD = {"fog": True, "wall_change_time": 5, "visibility": 40}