import pygame
import json
import os
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
        
        # Загрузка рекордов
        self.records = self.load_records()
    
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
        # Фон - растягиваем на весь экран
        self.screen.blit(pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        
        # Заголовок
        title_text = self.big_font.render("Выбор уровня", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Отображение уровней
        level_width = 200
        level_height = 150
        levels_per_row = 3
        start_x = (WINDOW_WIDTH - level_width * levels_per_row) // 2
        start_y = 200
        
        for i, level in enumerate(LEVELS.keys()):
            row = i // levels_per_row
            col = i % levels_per_row
            x = start_x + col * level_width
            y = start_y + row * (level_height + 50)
            
            # Фон для уровня
            if level <= current_level:
                bg_color = (50, 150, 50) if level == selected_level else (30, 100, 30)
            else:
                bg_color = (100, 100, 100)
            
            pygame.draw.rect(self.screen, bg_color, (x, y, level_width - 20, level_height))
            pygame.draw.rect(self.screen, WHITE, (x, y, level_width - 20, level_height), 2)
            
            # Номер уровня
            level_text = self.font.render(f"Уровень {level}", True, WHITE)
            level_rect = level_text.get_rect(center=(x + (level_width - 20) // 2, y + 30))
            self.screen.blit(level_text, level_rect)
            
            # Рекорд времени
            record_text = self.font.render(f"Рекорд: {self.get_record(level)}", True, WHITE)
            record_rect = record_text.get_rect(center=(x + (level_width - 20) // 2, y + 70))
            self.screen.blit(record_text, record_rect)
            
            # Размер лабиринта
            size = LEVELS[level]["size"]
            size_text = self.font.render(f"{size[1]}x{size[0]}", True, WHITE)
            size_rect = size_text.get_rect(center=(x + (level_width - 20) // 2, y + 110))
            self.screen.blit(size_text, size_rect)
            
            # Если уровень заблокирован
            if level > current_level:
                lock_font = pygame.font.Font(None, 24)  # Меньший размер шрифта
                lock_text = lock_font.render("ЗАБЛОКИРОВАН", True, RED)
                lock_rect = lock_text.get_rect(center=(x + (level_width - 20) // 2, y + 140))
                self.screen.blit(lock_text, lock_rect)
        
        # Инструкции
        instructions = [
            "Влево/Вправо - Выбор уровня",
            "Enter - Играть",
            "Esc - Назад"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100 + i * 30))
            self.screen.blit(text, rect)
    
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

    def load_records(self):
        """Загрузка рекордов"""
        if os.path.exists("records.json"):
            with open("records.json", "r") as f:
                return json.load(f)
        else:
            return {}
    
    def save_records(self):
        """Сохранение рекордов"""
        with open("records.json", "w") as f:
            json.dump(self.records, f)
    
    def update_record(self, level: int, time: float):
        """Обновление рекорда для уровня"""
        level_str = str(level)
        if level_str not in self.records or time < self.records[level_str]:
            self.records[level_str] = time
            self.save_records()
    
    def get_record(self, level: int) -> str:
        """Получение рекорда для уровня в формате MM:SS"""
        level_str = str(level)
        if level_str in self.records:
            time = self.records[level_str]
            minutes = int(time // 60)
            seconds = int(time % 60)
            return f"{minutes:02d}:{seconds:02d}"
        else:
            return "--:--" 