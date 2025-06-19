import random
import time
from typing import Tuple, List
from config import *
from .player import Player
from .maze import Maze
from .bonus import Bonus

class GameState:
    def __init__(self, level: int = 1):
        self.level = level
        self.state = PLAYING
        self.start_time = time.time()
        self.end_time = None  # Время завершения уровня
        
        # Создание лабиринта
        level_config = LEVELS[level]
        width, height = level_config["size"]
        self.maze = Maze(width, height)
        
        # Создание игрока в гарантированно доступной позиции
        self.player = Player((1, 1))
        
        # Создание выхода
        self.exit = (height - 2, width - 2)
        
        # Создание бонусов
        self.bonuses = []
        bonus_count = level_config["bonuses"]
        if level >= 3 and level_config.get("allow_bomb"):
            # На 5 уровне без PATH_HINT

            if level == 5:
                bonus_types = [FREEZE, TELEPORT, BOMB]
            else:
                bonus_types = [FREEZE, TELEPORT, PATH_HINT, BOMB]
            for _ in range(bonus_count):
                pos = self.maze.get_random_position()
                bonus_type = random.choice(bonus_types)
                self.bonuses.append(Bonus(pos, bonus_type))

        else:
            bonus_types = [FREEZE, TELEPORT, PATH_HINT]
            for i in range(bonus_count):
                pos = self.maze.get_random_position()
                bonus_type = bonus_types[i % len(bonus_types)]
                self.bonuses.append(Bonus(pos, bonus_type))

        
        # Монстры (пока пустой список)
        self.monsters = []
        
        # Подсказка пути
        self.show_path_hint = False
        self.path_hint = []
        
        # Заморозка лабиринта
        self.maze_freeze_timer = 0
    
    def update(self, dt: float):
        """Обновление состояния игры"""
        if self.state != PLAYING:
            return
        
        # Обновление игрока
        self.player.update(dt)
        
        # Обновление заморозки лабиринта
        if self.maze_freeze_timer > 0:
            self.maze_freeze_timer -= dt
        else:
            # Обновление меняющихся стен
            current_time = time.time() * 1000
            self.maze.update_changing_walls(current_time)
        
        # Если подсказка пути активна, проверяем ее валидность
        if self.show_path_hint and self.path_hint:
            for cell in self.path_hint:
                if self.maze.is_wall(cell):
                    self.show_path_hint = False
                    self.path_hint = []
                    break
        
        # Проверка коллизий
        self.check_collisions()
    
    def move_player(self, direction: Tuple[int, int]) -> bool:
        """Движение игрока"""
        if self.state != PLAYING:
            return False
        
        success = self.player.move(direction, self.maze.grid)
        if success:
            self.check_collisions()
        return success
    
    def check_collisions(self):
        """Проверка коллизий"""
        # Коллизии с бонусами
        for bonus in self.bonuses[:]:
            if bonus.active and bonus.position == self.player.position:
                if bonus.apply_effect(self.player, self):
                    bonus.active = False
        
        # Коллизия с выходом
        if self.player.position == self.exit:
            self.state = VICTORY
            self.end_time = time.time()  # Сохраняем время завершения
    
    def get_random_position(self) -> Tuple[int, int]:
        """Получение случайной позиции"""
        return self.maze.get_random_position()
    
    def get_game_time(self) -> float:
        """Получение времени игры"""
        if self.end_time is not None:
            # Если уровень завершен, возвращаем финальное время
            return self.end_time - self.start_time
        else:
            # Если игра еще идет, возвращаем текущее время
            return time.time() - self.start_time 