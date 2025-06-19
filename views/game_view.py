import pygame
from config import *

class GameView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        # Размер видимой области (в клетках)
        self.VIEW_SIZE = 30
    
    def draw(self, game_state):
        """Отрисовка игры"""
        self.game_state = game_state  # Для draw_bonuses
        # Очистка экрана
        self.screen.fill(WHITE)
        player_row, player_col = game_state.player.position
        maze = game_state.maze
        # Выбор размера видимой области
        if game_state.level <= 3:
            view_size = max(maze.width, maze.height)
        elif game_state.level == 4:
            view_size = 20
        else:
            view_size = 10
        half = view_size // 2
        # Проверяем, помещается ли лабиринт на экране
        fits_x = maze.width * CELL_SIZE <= WINDOW_WIDTH
        fits_y = maze.height * CELL_SIZE <= WINDOW_HEIGHT
        if game_state.level <= 3 and fits_x and fits_y:
            # Центрируем весь лабиринт в окне
            min_row = 0
            min_col = 0
            offset_x = (WINDOW_WIDTH - maze.width * CELL_SIZE) // 2
            offset_y = (WINDOW_HEIGHT - maze.height * CELL_SIZE) // 2
        elif game_state.level in (4, 5):
            # Центрируем видимую область (view_size x view_size) в окне
            min_row = max(0, min(player_row - half, max(0, maze.height - view_size)))
            min_col = max(0, min(player_col - half, max(0, maze.width - view_size)))
            offset_x = (WINDOW_WIDTH - view_size * CELL_SIZE) // 2
            offset_y = (WINDOW_HEIGHT - view_size * CELL_SIZE) // 2
        else:
            # Камера вокруг игрока
            min_row = max(0, min(player_row - half, max(0, maze.height - view_size)))
            min_col = max(0, min(player_col - half, max(0, maze.width - view_size)))
            offset_x = 0
            offset_y = 0
        self.draw_maze(maze, min_row, min_col, view_size, offset_x, offset_y)
        
        # Отрисовка подсказки пути
        if game_state.show_path_hint and game_state.path_hint:
            self.draw_path_hint(game_state.path_hint, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка игрока
        self.draw_player(game_state.player, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка бонусов
        self.draw_bonuses(game_state.bonuses, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка выхода
        self.draw_exit(game_state.exit, min_row, min_col, offset_x, offset_y)
        
        # ТУМАН ВОЙНЫ для уровней 4 и 5
        if game_state.level in (4, 5):
            fog = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            fog.fill((0, 0, 0, 220))  # Более тёмный туман
            player_x = (player_col - min_col) * CELL_SIZE + offset_x + CELL_SIZE // 2
            player_y = (player_row - min_row) * CELL_SIZE + offset_y + CELL_SIZE // 2
            if game_state.level == 4:
                radius = CELL_SIZE * 5
            else:
                radius = CELL_SIZE * 3
            pygame.draw.circle(fog, (0, 0, 0, 0), (player_x, player_y), radius)
            self.screen.blit(fog, (0, 0))
        
        # Отрисовка UI
        self.draw_ui(game_state)
        
        # Отрисовка экранов состояния
        if game_state.state == VICTORY:
            self.draw_victory_screen(game_state)
        elif game_state.state == 'GAME_OVER':
            self.draw_game_over_screen(game_state)
    
    def draw_maze(self, maze, min_row=0, min_col=0, view_size=15, offset_x=0, offset_y=0):
        """Отрисовка лабиринта"""
        for row in range(min_row, min(min_row + view_size, maze.height)):
            for col in range(min_col, min(min_col + view_size, maze.width)):
                x = (col - min_col) * CELL_SIZE + offset_x
                y = (row - min_row) * CELL_SIZE + offset_y
                
                if maze.grid[row][col] == 1:  # Стена
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                else:  # Проход
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    def draw_player(self, player, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка игрока"""
        x = (player.position[1] - min_col) * CELL_SIZE + offset_x
        y = (player.position[0] - min_row) * CELL_SIZE + offset_y
        
        color = CYAN if player.frozen else GREEN
        pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
    def draw_bonuses(self, bonuses, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка бонусов"""
        for bonus in bonuses:
            if bonus.active:
                x = (bonus.position[1] - min_col) * CELL_SIZE + offset_x
                y = (bonus.position[0] - min_row) * CELL_SIZE + offset_y
                # На уровнях 3-5 все бонусы серые (игрок не знает тип)
                if hasattr(self, 'game_state') and 3 <= self.game_state.level <= 5:
                    color = (120, 120, 120)
                else:
                    color_map = {FREEZE: BLUE, TELEPORT: MAGENTA, PATH_HINT: YELLOW, BOMB: (120, 120, 120)}
                    color = color_map.get(bonus.type, WHITE)
                pygame.draw.circle(self.screen, color, 
                                 (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 
                                 CELL_SIZE // 3)
    
    def draw_exit(self, exit_pos, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка выхода"""
        x = (exit_pos[1] - min_col) * CELL_SIZE + offset_x
        y = (exit_pos[0] - min_row) * CELL_SIZE + offset_y
        
        pygame.draw.rect(self.screen, RED, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
    def draw_path_hint(self, path_hint, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка подсказки пути"""
        for i in range(len(path_hint) - 1):
            current = path_hint[i]
            next_pos = path_hint[i + 1]
            
            x1 = (current[1] - min_col) * CELL_SIZE + CELL_SIZE // 2 + offset_x
            y1 = (current[0] - min_row) * CELL_SIZE + CELL_SIZE // 2 + offset_y
            x2 = (next_pos[1] - min_col) * CELL_SIZE + CELL_SIZE // 2 + offset_x
            y2 = (next_pos[0] - min_row) * CELL_SIZE + CELL_SIZE // 2 + offset_y
            
            pygame.draw.line(self.screen, YELLOW, (x1, y1), (x2, y2), 2)
    
    def draw_ui(self, game_state):
        """Отрисовка UI"""
        # Уровень
        level_text = self.font.render(f"Уровень: {game_state.level}", True, BLACK)
        self.screen.blit(level_text, (10, 10))
        
        # Время
        time_text = self.font.render(f"Время: {game_state.get_game_time():.1f}с", True, BLACK)
        self.screen.blit(time_text, (10, 50))
        
        # Бонусы
        active_bonuses = sum(1 for b in game_state.bonuses if b.active)
        bonus_text = self.font.render(f"Бонусы: {active_bonuses}", True, BLACK)
        self.screen.blit(bonus_text, (10, 90))
        
        # Заморозка лабиринта
        if game_state.maze_freeze_timer > 0:
            freeze_text = self.font.render(f"Заморозка: {game_state.maze_freeze_timer:.1f}с", True, BLUE)
            self.screen.blit(freeze_text, (10, 130))
        
        # Подсказка пути
        if game_state.show_path_hint:
            hint_text = self.font.render("Путь показан", True, YELLOW)
            self.screen.blit(hint_text, (10, 170))
    
    def draw_victory_screen(self, game_state):
        """Отрисовка экрана победы"""
        # Полупрозрачный фон
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        # Текст победы
        victory_text = self.font.render("ПОБЕДА!", True, GREEN)
        text_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(victory_text, text_rect)
        
        # Время
        time_text = self.font.render(f"Время: {game_state.get_game_time():.1f}с", True, BLACK)
        time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(time_text, time_rect)
        
        # Инструкции
        if game_state.level + 1 in LEVELS:
            next_text = self.font.render("Следующий уровень (N)", True, BLUE)
            next_rect = next_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(next_text, next_rect)
        
        menu_text = self.font.render("Меню (M)", True, BLACK)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)

    def draw_game_over_screen(self, game_state):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        text1 = self.font.render("GAME OVER! Вы нашли бомбу...", True, (255, 0, 0))
        text2 = self.font.render("Заново (R)", True, (255, 255, 0))
        text3 = self.font.render("Меню (M)", True, (255, 255, 255))
        self.screen.blit(text1, (WINDOW_WIDTH//2 - text1.get_width()//2, WINDOW_HEIGHT//2 - 60))
        self.screen.blit(text2, (WINDOW_WIDTH//2 - text2.get_width()//2, WINDOW_HEIGHT//2))
        self.screen.blit(text3, (WINDOW_WIDTH//2 - text3.get_width()//2, WINDOW_HEIGHT//2 + 40)) 