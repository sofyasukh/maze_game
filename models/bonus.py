import random
from typing import Tuple
from config import *

class Bonus:
    def __init__(self, position: Tuple[int, int], bonus_type: str):
        self.position = position
        self.type = bonus_type
        self.active = True
    
    def apply_effect(self, player, game_state) -> bool:
        """Применение эффекта бонуса"""
        if self.type == FREEZE:
            # Заморозка изменения лабиринта
            freeze_duration = {
                1: 30.0,  # 30 секунд на первом уровне
                2: 20.0,  # 20 секунд на втором
                3: 15.0,  # 15 секунд на третьем
                4: 10.0,  # 10 секунд на четвертом
                5: 5.0    # 5 секунд на пятом
            }
            duration = freeze_duration.get(game_state.level, 10.0)
            game_state.maze_freeze_timer = duration
            return True
        
        elif self.type == TELEPORT:
            # Телепорт в случайную позицию
            attempts = 0
            while attempts < 50:
                new_pos = game_state.get_random_position()
                if new_pos != player.position:
                    return player.teleport(new_pos, game_state.maze.grid)
                attempts += 1
            return False
        
        elif self.type == PATH_HINT:
            # Показать путь к выходу
            game_state.show_path_hint = True
            game_state.path_hint = game_state.maze.find_path(player.position, game_state.exit)
            return True
        
        elif self.type == BOMB:
            # Бомба — мгновенный GAME OVER
            game_state.state = 'GAME_OVER'
            return True
        
        return False 