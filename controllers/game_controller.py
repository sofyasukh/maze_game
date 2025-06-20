import pygame
from config import *
from models.game_state import GameState
from views.game_view import GameView

class GameController:
    def __init__(self, screen: pygame.Surface, menu_view=None):
        self.screen = screen
        self.game_state = None
        self.game_view = GameView(screen)
        self.clock = pygame.time.Clock()
        self.menu_view = menu_view  # Ссылка на MenuView для обновления рекордов
    
    def start_game(self, level: int = 1):
        """Запуск игры"""
        self.game_state = GameState(level)
        self.game_state.game_view = self.game_view  # Устанавливаем ссылку для звуков
        # Запускаем фоновую музыку только если она включена глобально
        from views.menu_view import MenuView
        if MenuView.global_music_enabled:
            self.game_view.play_soundtrack()
        return self.run()
    
    def run(self):
        """Игровой цикл"""
        running = True
        
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Останавливаем музыку при выходе
                    self.game_view.stop_soundtrack()
                    return "quit"
                
                elif event.type == pygame.KEYDOWN:
                    result = self.handle_keydown(event.key)
                    if result:
                        return result
            
            # Удержание клавиши для движения
            if self.game_state and self.game_state.state == PLAYING:
                keys = pygame.key.get_pressed()
                direction = None
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    direction = (-1, 0)
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    direction = (1, 0)
                elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    direction = (0, -1)
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    direction = (0, 1)
                if direction:
                    self.game_state.move_player(direction)
            
            # Обновление игры
            if self.game_state:
                previous_state = self.game_state.state
                self.game_state.update(dt)
                # Проверяем, перешла ли игра в состояние GAME_OVER (бомба сработала)
                if previous_state == PLAYING and self.game_state.state == 'GAME_OVER':
                    self.game_view.play_explosion_sound()
                # Проверяем победу и обновляем рекорд
                elif previous_state == PLAYING and self.game_state.state == VICTORY:
                    # Обновляем рекорд для текущего уровня
                    if self.menu_view:
                        self.menu_view.update_record(self.game_state.level, self.game_state.get_game_time())
            
            # Отрисовка
            if self.game_state:
                self.game_view.draw(self.game_state)
                pygame.display.flip()
        
        return "menu"  # Возвращаем результат по умолчанию
    
    def handle_keydown(self, key):
        """Обработка нажатий клавиш"""
        if not self.game_state:
            return None
        
        if self.game_state.state == PLAYING:
            # Движение игрока
            direction = self.get_direction(key)
            if direction:
                self.game_state.move_player(direction)
        
        elif self.game_state.state == VICTORY:
            next_level = self.game_state.level + 1
            if key == pygame.K_n and next_level in LEVELS:
                # Следующий уровень
                self.game_view.play_click_sound()
                self.game_view.stop_soundtrack()  # Останавливаем музыку
                return f"next_level_{next_level}"
            elif key == pygame.K_m:
                # Возврат в меню
                self.game_view.play_click_sound()
                self.game_view.stop_soundtrack()  # Останавливаем музыку
                return "menu"
        
        elif self.game_state.state == 'GAME_OVER':
            if key == pygame.K_r:
                # Перезапуск уровня
                self.game_view.play_click_sound()
                self.game_view.stop_soundtrack()  # Останавливаем музыку
                return f"play_level_{self.game_state.level}"
            elif key == pygame.K_m:
                self.game_view.play_click_sound()
                self.game_view.stop_soundtrack()  # Останавливаем музыку
                return "menu"
        
        return None
    
    def get_direction(self, key):
        """Получение направления движения"""
        if key == pygame.K_w or key == pygame.K_UP:
            return (-1, 0)  # Вверх
        elif key == pygame.K_s or key == pygame.K_DOWN:
            return (1, 0)   # Вниз
        elif key == pygame.K_a or key == pygame.K_LEFT:
            return (0, -1)  # Влево
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            return (0, 1)   # Вправо
        return None 