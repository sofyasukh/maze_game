import pygame
from config import *

class MenuView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        # Загрузка фонового изображения меню
        self.menu_bg = pygame.image.load("assets/images/menu.png").convert()
    
    def draw_main_menu(self, selected_option: int):
        """Отрисовка главного меню"""
        # Рисуем фоновое изображение
        self.screen.blit(pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        
        # Заголовок
        title_text = self.title_font.render("Silent Shift", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Опции меню
        options = ["Играть", "Выбор уровня", "Выход"]
        for i, option in enumerate(options):
            color = WHITE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 60))
            self.screen.blit(text, text_rect)
            if i == selected_option:
                pygame.draw.rect(self.screen, BLUE, 
                               (text_rect.left - 10, text_rect.top - 5, 
                                text_rect.width + 20, text_rect.height + 10), 2)
    
    def draw_level_select(self, selected_level: int, current_level: int):
        """Отрисовка выбора уровня"""
        # Рисуем фоновое изображение
        self.screen.blit(pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        title_text = self.font.render("ВЫБОР УРОВНЯ", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        max_level = len(LEVELS)
        # Центрируем уровни по ширине окна
        total_width = (max_level - 1) * 160
        start_x = (WINDOW_WIDTH - total_width) // 2
        for i, level in enumerate(range(1, max_level + 1)):
            x = start_x + i * 160
            y = 250
            if level <= current_level:
                bg_color = GREEN
                text_color = WHITE
            else:
                bg_color = GRAY
                text_color = BLACK
            pygame.draw.rect(self.screen, bg_color, (x - 30, y - 30, 120, 120))
            pygame.draw.rect(self.screen, BLACK, (x - 30, y - 30, 120, 120), 3)
            level_text = self.font.render(str(level), True, text_color)
            level_rect = level_text.get_rect(center=(x + 30, y + 30))
            self.screen.blit(level_text, level_rect)
            if level == selected_level:
                pygame.draw.rect(self.screen, BLUE, (x - 35, y - 35, 130, 130), 5)
        back_text = self.font.render("Назад (ESC)", True, WHITE)
        back_rect = back_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(back_text, back_rect)
        if selected_level <= current_level:
            start_text = self.font.render("Начать (ENTER)", True, BLUE)
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            self.screen.blit(start_text, start_rect) 