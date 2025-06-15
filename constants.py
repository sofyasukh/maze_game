# Цвета (добавляем недостающие)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # Добавляем пурпурный
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Размеры
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CELL_SIZE = 30
PLAYER_SIZE = 20

# Уровни сложности
EASY = {"fog": False, "wall_change_time": 10, "visibility": 100}
MEDIUM = {"fog": True, "wall_change_time": 7, "visibility": 70}
HARD = {"fog": True, "wall_change_time": 5, "visibility": 40}

#СКОРОСТЬ ИГРОКА
PLAYER_SPEED = 3

# Длительности эффектов в миллисекундах
FREEZE_DURATION = 5000  # 5 секунд
PATH_HINT_DURATION = 3000  # 3 секунды