import pygame
from config import *
from models.game_state import GameState
from views.game_view import GameView

class GameController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.game_state = None
        self.game_view = GameView(screen)
        self.clock = pygame.time.Clock()
    
    def start_game(self, level: int = 1):
        """Запуск игры"""
        self.game_state = GameState(level)
        return self.run()
    
    def run(self):
        """Игровой цикл"""
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
            
            # Обновление игры
            if self.game_state:
                self.game_state.update(dt)
            
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
                return f"next_level_{next_level}"
            elif key == pygame.K_m:
                # Возврат в меню
                return "menu"
        
        elif self.game_state.state == 'GAME_OVER':
            if key == pygame.K_r:
                # Перезапуск уровня
                return f"play_level_{self.game_state.level}"
            elif key == pygame.K_m:
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