import pygame
import sys
from controllers.menu_controller import MenuController
from controllers.game_controller import GameController
from config import *
from utils.asset_manager import AssetManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Лабиринт")
        
        self.asset_manager = AssetManager()
        self.load_assets()
        
        self.menu_controller = MenuController(self.screen, self.asset_manager)
        # GameController будет создаваться динамически с ссылкой на MenuView
        
        self.current_level = 1
        self.running = True
    
    def load_assets(self):
        """Загрузка всех игровых ресурсов."""
        # Изображения
        self.asset_manager.load_image('wall', "assets/images/wall.png")
        self.asset_manager.load_image('floor', "assets/images/floor.png")
        self.asset_manager.load_image('flag', "assets/images/flag.png")
        self.asset_manager.load_image('menu_bg', "assets/images/menu.png")
        self.asset_manager.load_image('explosion', "assets/images/explosion.png")
        # Бонусы
        self.asset_manager.load_image(FREEZE, "assets/images/freeze.png")
        self.asset_manager.load_image(TELEPORT, "assets/images/teleport.png")
        self.asset_manager.load_image(PATH_HINT, "assets/images/path_hint.png")
        self.asset_manager.load_image(BOMB, "assets/images/bomb.png")
        
        # Звуки
        self.asset_manager.load_sound('click', "assets/sounds/click.wav")
        self.asset_manager.load_sound('freezing', "assets/sounds/freezing.wav")
        self.asset_manager.load_sound('teleporting', "assets/sounds/teleporting.wav")
        self.asset_manager.load_sound('hint', "assets/sounds/hint.wav")
        self.asset_manager.load_sound('win', "assets/sounds/win.wav")
        self.asset_manager.load_sound('boom', "assets/sounds/boom.wav")
        self.asset_manager.load_sound('soundtrack', "assets/sounds/soundtrack.wav")

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
        # Создаем GameController с ссылкой на MenuView и AssetManager
        game_controller = GameController(self.screen, self.menu_controller.menu_view, self.asset_manager)
        result = game_controller.start_game(level)
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