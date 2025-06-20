from typing import Tuple
from config import *

class Player:
    def __init__(self, position: Tuple[int, int]):
        self.position = position  # Логическая позиция (клетка)
        self.pixel_pos = list(position)
        self.target_pixel_pos = list(position)
        self.move_timer = 0
        self.speed = PLAYER_SPEED  # Использование константы
        self.frozen = False
        self.freeze_timer = 0
        self.target_cell = position
        self.moving = False

    def move(self, direction: Tuple[int, int], maze) -> bool:
        if self.frozen or self.moving:
            return False
        new_row = self.position[0] + direction[0]
        new_col = self.position[1] + direction[1]
        if (0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == 0):
            self.target_cell = (new_row, new_col)
            self.moving = True
            return True
        return False

    def update(self, dt: float):
        if self.frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self.frozen = False
        # Плавное движение
        if self.moving:
            tx, ty = self.target_cell[1], self.target_cell[0]
            px, py = self.pixel_pos
            dx = tx - px
            dy = ty - py
            dist = (dx ** 2 + dy ** 2) ** 0.5
            step = self.speed * dt
            if dist <= step:
                self.pixel_pos = [tx, ty]
                self.position = self.target_cell
                self.moving = False
            else:
                self.pixel_pos[0] += dx / dist * step
                self.pixel_pos[1] += dy / dist * step

    def freeze(self, duration: float = 3.0):
        self.frozen = True
        self.freeze_timer = duration

    def teleport(self, new_position: Tuple[int, int], maze) -> bool:
        if (0 <= new_position[0] < len(maze) and 0 <= new_position[1] < len(maze[0]) and maze[new_position[0]][new_position[1]] == 0):
            self.position = new_position
            self.pixel_pos = [new_position[1], new_position[0]]
            self.target_cell = new_position
            self.moving = False
            return True
        return False 