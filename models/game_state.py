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
        if level == 1:
            bonus_count = 0  # Убираем бонусы с первого уровня
        elif level == 5:
            bonus_types = [FREEZE, TELEPORT, BOMB]
        else:
            bonus_types = [FREEZE, TELEPORT, PATH_HINT]
        
        # Собираем все свободные клетки, не занятые игроком, выходом и уже выбранными бонусами, и до которых есть путь от игрока
        available_cells = []
        bomb_cells = []  # Отдельный список для бомб
        for row in range(1, height - 1):
            for col in range(1, width - 1):
                pos = (row, col)
                if pos == (1, 1) or pos == self.exit:
                    continue
                if self.maze.grid[row][col] != 0:
                    continue
                # Проверяем, что до клетки можно дойти от игрока
                path = self.maze.find_path((1, 1), pos)
                if not path:
                    continue
                # Для бомбы: не ближе 3 клеток к выходу
                if level == 5 and abs(pos[0] - self.exit[0]) + abs(pos[1] - self.exit[1]) >= 3:
                    bomb_cells.append(pos)
                available_cells.append(pos)
        
        random.shuffle(available_cells)
        random.shuffle(bomb_cells)
        
        if level == 5:
            # На 5 уровне: сначала создаем бомбы, затем остальные бонусы
            bomb_count = min(3, len(bomb_cells))  # 3 бомбы максимум
            for i in range(bomb_count):
                if bomb_cells:
                    pos = bomb_cells.pop()
                    self.bonuses.append(Bonus(pos, BOMB))
                    available_cells.remove(pos)  # Убираем из доступных
            
            # Остальные бонусы
            remaining_bonuses = bonus_count - bomb_count
            other_types = [FREEZE, TELEPORT]
            for i in range(remaining_bonuses):
                if not available_cells:
                    break
                pos = available_cells.pop()
                bonus_type = other_types[i % len(other_types)]
                self.bonuses.append(Bonus(pos, bonus_type))
        else:
            # Обычные уровни
            for i in range(bonus_count):
                if not available_cells:
                    break
                pos = available_cells.pop()
                bonus_type = bonus_types[i % len(bonus_types)]
                self.bonuses.append(Bonus(pos, bonus_type))
        
        # Монстры (пока пустой список)
        self.monsters = []
        
        # Подсказка пути
        self.show_path_hint = False
        self.path_hint = []
        self.path_hint_timer = 0.0
        
        # Заморозка лабиринта
        self.maze_freeze_timer = 0
        
        # Анимация взрыва
        self.explosion_animations = []  # Список активных анимаций взрыва
        
        # Ссылка на game_view для воспроизведения звуков
        self.game_view = None  # type: ignore
        
        # Причина смерти (для отображения сообщения)
        self.death_reason = None
    
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
            bonus_positions = [bonus.position for bonus in self.bonuses if bonus.active]
            self.maze.update_changing_walls(current_time, bonus_positions)
            # Если активна подсказка пути, обновить путь после смены лабиринта
            if self.show_path_hint:
                self.path_hint = self.maze.find_path(self.player.position, self.exit)
        # Подсказка пути: только таймер и отключение
        if self.show_path_hint:
            self.path_hint_timer -= dt
            if self.path_hint_timer <= 0:
                self.show_path_hint = False
                self.path_hint = []
        
        # Обновление анимаций взрыва
        for animation in self.explosion_animations[:]:
            animation['timer'] -= dt
            if animation['timer'] <= 0:
                self.explosion_animations.remove(animation)
        
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
            if bonus.active:
                if bonus.type == BOMB:
                    # Для бомбы: проверяем радиус 3 клетки
                    px, py = bonus.position
                    player_pos = self.player.position
                    if abs(player_pos[0] - px) + abs(player_pos[1] - py) <= 3:
                        if bonus.apply_effect(self.player, self):
                            bonus.active = False
                else:
                    # Для остальных бонусов: точное совпадение позиций
                    if bonus.position == self.player.position:
                        if bonus.apply_effect(self.player, self):
                            bonus.active = False
        
        # Коллизия с выходом
        if self.player.position == self.exit:
            self.state = VICTORY
            self.end_time = time.time()  # Сохраняем время завершения
            # Воспроизводим звук победы
            if self.game_view:
                self.game_view.play_win_sound()
    
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
    
    def create_explosion_animation(self, bomb_position):
        """Создание анимации взрыва"""
        explosion = {
            'position': bomb_position,
            'timer': 1.0,  # 1 секунда
            'size': 3  # 3x3 клетки
        }
        self.explosion_animations.append(explosion) 