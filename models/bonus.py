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
            duration = 10.0
            game_state.maze_freeze_timer = duration
            return True
        
        elif self.type == TELEPORT:
            # Телепорт в случайную позицию
            attempts = 0
            while attempts < 50:
                new_pos = game_state.get_random_position()
                if new_pos != player.position:
                    success = player.teleport(new_pos, game_state.maze.grid)
                    if success:
                        return success
                attempts += 1
            return False
        
        elif self.type == PATH_HINT:
            # Показать путь к выходу на ограниченное время
            game_state.show_path_hint = True
            game_state.path_hint_timer = 7.0  # 7 секунд
            game_state.path_hint = game_state.maze.find_path(player.position, game_state.exit)
            return True
        
        elif self.type == BOMB:
            # Детонация в радиусе
            px, py = self.position
            # Игрок уже в радиусе (проверка сделана в check_collisions)
            game_state.state = 'GAME_OVER'
            game_state.death_reason = 'bomb'
            game_state.create_explosion_animation(self.position)
            # Деактивируем все бонусы в радиусе (кроме самой бомбы)
            for bonus in game_state.bonuses:
                if bonus is not self and bonus.active:
                    bx, by = bonus.position
                    if abs(bx - px) + abs(by - py) <= BOMB_EXPLOSION_RADIUS:
                        bonus.active = False
            return True
        
        return False 