import pygame
from config import *

class MenuView:
    # Глобальное состояние музыки
    global_music_enabled = True
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        # Загрузка фонового изображения меню
        self.menu_bg = pygame.image.load("assets/images/menu.png").convert()
        # Загрузка звука клика
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        # Загрузка фоновой музыки
        self.soundtrack = pygame.mixer.Sound("assets/sounds/soundtrack.wav")
        
        # Настройки
        self.music_enabled = MenuView.global_music_enabled
    
    def draw_main_menu(self, selected_option: int):
        """Отрисовка главного меню"""
        # Рисуем фоновое изображение
        self.screen.blit(pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        
        # Заголовок
        title_text = self.big_font.render("Silent Shift", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Отрисовка опций меню
        options = [
            "Играть",
            "Выбор уровня",
            "Музыка: ВКЛ" if self.music_enabled else "Музыка: ВЫКЛ",
            "Выход"
        ]
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else WHITE
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 60))
            self.screen.blit(text_surface, text_rect)
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
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(start_text, start_rect)
    
    def play_click_sound(self):
        """Воспроизведение звука клика"""
        try:
            self.click_sound.play()
        except:
            pass
    
    def play_soundtrack(self):
        """Воспроизведение фоновой музыки с зацикливанием"""
        if self.music_enabled:
            try:
                self.soundtrack.set_volume(0.3)  # Устанавливаем громкость 30%
                self.soundtrack.play(-1)  # -1 означает бесконечное зацикливание
            except:
                pass
    
    def stop_soundtrack(self):
        """Остановка фоновой музыки"""
        try:
            self.soundtrack.stop()
        except:
            pass
    
    def toggle_music(self):
        """Переключение музыки вкл/выкл"""
        self.music_enabled = not self.music_enabled
        MenuView.global_music_enabled = self.music_enabled  # Обновляем глобальное состояние
        if self.music_enabled:
            self.play_soundtrack()
        else:
            self.stop_soundtrack() 