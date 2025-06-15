import pygame
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, PLAYER_SIZE,
    FREEZE_DURATION, PATH_HINT_DURATION
)
from .maze import Maze
from .player import Player
from .bonuses import Bonus
from .fog import Fog

class Game:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.difficulty = difficulty
        self.maze = Maze(screen.get_width(), screen.get_height())
        self.player = Player(CELL_SIZE, CELL_SIZE, self.maze.exit_pos)
        self.bonuses = [Bonus(self.maze.grid) for _ in range(3)]
        self.fog = Fog(difficulty['visibility']) if difficulty['fog'] else None
        self.clock = pygame.time.Clock()
        self.running = False
        self.walls_frozen = False
        self.show_path = False
        self.freeze_end_time = 0
        self.path_end_time = 0
        self.wall_change_timer = 0
        self.wall_change_interval = difficulty['wall_change_time'] * 1000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        # Обработка движения
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1

        if self.player.move(dx, dy, self.maze.grid):
            # Проверка сбора бонусов
            for bonus in self.bonuses[:]:
                if self.player.grid_pos == bonus.pos:
                    self._apply_bonus(bonus)
                    self.bonuses.remove(bonus)

        # Проверка таймеров бонусов
        current_time = pygame.time.get_ticks()
        if self.walls_frozen and current_time > self.freeze_end_time:
            self.walls_frozen = False
        if self.show_path and current_time > self.path_end_time:
            self.show_path = False

        self._update_dynamic_walls()

    def _apply_bonus(self, bonus):
        """Применяет эффект бонуса"""
        current_time = pygame.time.get_ticks()
        
        if bonus.type == 'teleport':
            # Исправленный генератор списка:
            empty_cells = [
                (x, y) 
                for y in range(len(self.maze.grid)) 
                for x in range(len(self.maze.grid[0])) 
                if self.maze.grid[y][x] == 0
            ]  # Скобка закрывается здесь
            
            if empty_cells:
                target = random.choice(empty_cells)
                self.player.teleport(*target)

        elif bonus.type == 'freeze':
            self.walls_frozen = True
            self.freeze_end_time = current_time + FREEZE_DURATION

        elif bonus.type == 'path_hint':
            self.show_path = True
            self.path_end_time = current_time + PATH_HINT_DURATION
    
    def _update_dynamic_walls(self):
        """Обновляет динамические стены"""
        current_time = pygame.time.get_ticks()
        if current_time - self.wall_change_timer > self.wall_change_interval:
            self.wall_change_timer = current_time
            self._change_walls()

    def _change_walls(self):
        """Изменяет случайные стены"""
        if self.walls_frozen:  # Не меняем стены, если они заморожены
            return
            
        for _ in range(5):  # Меняем 5 случайных стен
            x = random.randint(1, len(self.maze.grid[0]) - 2)
            y = random.randint(1, len(self.maze.grid)) - 2
            self.maze.grid[y][x] = 1 - self.maze.grid[y][x]  # Инвертируем стену    
    def draw(self):
        self.screen.fill((0, 0, 0))  # Черный фон
        
        # Отрисовка лабиринта
        for y in range(len(self.maze.grid)):
            for x in range(len(self.maze.grid[0])):
                if self.maze.grid[y][x] == 1:  # Стена
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),
                        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        
        # Отрисовка бонусов
        for bonus in self.bonuses:
            pygame.draw.circle(
                self.screen, bonus.color,
                (bonus.pos[0] * CELL_SIZE + CELL_SIZE//2,
                 bonus.pos[1] * CELL_SIZE + CELL_SIZE//2),
                CELL_SIZE//3
            )
        
        # Отрисовка игрока
        pygame.draw.rect(
            self.screen, (0, 255, 0),
            (self.player.rect.x, self.player.rect.y, PLAYER_SIZE, PLAYER_SIZE)
        )
        
        # Отрисовка тумана войны
        if self.fog:
            self.fog.update((self.player.rect.x, self.player.rect.y))
            self.fog.draw(self.screen)
        
        pygame.display.flip()

        font = pygame.font.Font(None, 24)
        debug_text = [
            f"Сложность: {self.difficulty}",
            f"Бонусов: {len(self.bonuses)}",
            f"Стены меняются через: {max(0, (self.wall_change_timer + self.wall_change_interval - pygame.time.get_ticks()) // 1000)} сек",
            f"Состояние: {'Заморожено' if self.walls_frozen else 'Активно'}"
        ]
    
        for i, text in enumerate(debug_text):
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10 + i * 25))

    def run(self):
        self.running = True
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)