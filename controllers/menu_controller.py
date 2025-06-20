import pygame
from config import *
from views.menu_view import MenuView

class MenuController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.menu_view = MenuView(screen)
        self.clock = pygame.time.Clock()
        
        # Состояние меню
        self.current_menu = "main"
        self.selected_option = 0
        self.selected_level = 1
        self.current_level = 1
    
    def run(self):
        """Запуск меню"""
        # Запускаем фоновую музыку только если она включена глобально
        if self.menu_view.music_enabled:
            self.menu_view.play_soundtrack()
        
        running = True
        
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                elif event.type == pygame.KEYDOWN:
                    result = self.handle_keydown(event.key)
                    if result:
                        return result
            
            # Отрисовка
            self.render()
            pygame.display.flip()
    
    def handle_keydown(self, key):
        """Обработка нажатий клавиш"""
        if self.current_menu == "main":
            return self.handle_main_menu(key)
        elif self.current_menu == "level_select":
            return self.handle_level_select(key)
    
    def handle_main_menu(self, key):
        """Обработка главного меню"""
        if key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % 4
            self.menu_view.play_click_sound()
        elif key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % 4
            self.menu_view.play_click_sound()
        elif key == pygame.K_RETURN:
            if self.selected_option == 0:  # Играть
                self.menu_view.play_click_sound()
                self.menu_view.stop_soundtrack()  # Останавливаем музыку
                return f"play_level_{self.current_level}"
            elif self.selected_option == 1:  # Выбор уровня
                self.menu_view.play_click_sound()
                self.current_menu = "level_select"
                self.selected_level = self.current_level
            elif self.selected_option == 2:  # Музыка
                self.menu_view.play_click_sound()
                self.menu_view.toggle_music()
            elif self.selected_option == 3:  # Выход
                self.menu_view.play_click_sound()
                self.menu_view.stop_soundtrack()  # Останавливаем музыку
                return "quit"
    
    def handle_level_select(self, key):
        """Обработка выбора уровня"""
        max_level = len(LEVELS)
        if key == pygame.K_LEFT:
            self.selected_level = max(1, self.selected_level - 1)
        elif key == pygame.K_RIGHT:
            self.selected_level = min(max_level, self.selected_level + 1)
        elif key == pygame.K_RETURN:
            if self.selected_level <= self.current_level:
                self.menu_view.play_click_sound()
                self.menu_view.stop_soundtrack()  # Останавливаем музыку
                return f"play_level_{self.selected_level}"
        elif key == pygame.K_ESCAPE:
            self.current_menu = "main"
            self.menu_view.play_click_sound()
            # Возобновляем музыку при возврате в главное меню только если она включена
            if self.menu_view.music_enabled:
                self.menu_view.play_soundtrack()
    
    def render(self):
        """Отрисовка меню"""
        if self.current_menu == "main":
            self.menu_view.draw_main_menu(self.selected_option)
        elif self.current_menu == "level_select":
            self.menu_view.draw_level_select(self.selected_level, self.current_level)
    
    def set_current_level(self, level: int):
        """Установка текущего уровня и выбранного уровня"""
        self.current_level = max(self.current_level, level)
        self.selected_level = self.current_level 