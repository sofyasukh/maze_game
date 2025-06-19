import pygame
import sys
from controllers.menu_controller import MenuController
from controllers.game_controller import GameController
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Лабиринт")
        
        self.menu_controller = MenuController(self.screen)
        self.game_controller = GameController(self.screen)
        
        self.current_level = 1
        self.running = True
    
    def run(self):
        """Запуск игры"""
        while self.running:
            # Запуск меню
            result = self.menu_controller.run()
            if result == "quit":
                self.running = False
                break
            if result and result.startswith("play_level_"):
                level = int(result.split("_")[-1])
                self.play_level(level)
            elif result and result.startswith("next_level_"):
                level = int(result.split("_")[-1])
                self.current_level = level
                self.menu_controller.set_current_level(level)
    
    def play_level(self, level: int):
        """Игра в уровне"""
        result = self.game_controller.start_game(level)
        if result == "menu":
            return
        elif result and result.startswith("next_level_"):
            next_level = int(result.split("_")[-1])
            self.current_level = max(self.current_level, next_level)
            self.menu_controller.set_current_level(self.current_level)
            self.play_level(next_level)
    
    def quit(self):
        """Завершение игры"""
        pygame.quit()
        sys.exit()

def main():
    """Точка входа"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nИгра прервана пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        pygame.quit()
        sys.exit() 