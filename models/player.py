from typing import Tuple
from config import *

class Player:
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.frozen = False
        self.freeze_timer = 0
    
    def move(self, direction: Tuple[int, int], maze) -> bool:
        """Движение игрока"""
        if self.frozen:
            return False
        
        new_row = self.position[0] + direction[0]
        new_col = self.position[1] + direction[1]
        
        # Проверка границ и стен
        if (0 <= new_row < len(maze) and 
            0 <= new_col < len(maze[0]) and 
            maze[new_row][new_col] == 0):
            self.position = (new_row, new_col)
            return True
        return False
    
    def update(self, dt: float):
        """Обновление состояния"""
        if self.frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self.frozen = False
    
    def freeze(self, duration: float = 3.0):
        """Заморозка игрока"""
        self.frozen = True
        self.freeze_timer = duration
    
    def teleport(self, new_position: Tuple[int, int], maze) -> bool:
        """Телепортация"""
        if (0 <= new_position[0] < len(maze) and 
            0 <= new_position[1] < len(maze[0]) and 
            maze[new_position[0]][new_position[1]] == 0):
            self.position = new_position
            return True
        return False 