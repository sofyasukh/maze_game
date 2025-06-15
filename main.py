import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, EASY, MEDIUM, HARD
from game.game_core import Game
from ui.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Динамический Лабиринт")
    
    def start_game(difficulty_name):
        """Обработчик выбора уровня сложности"""
        difficulty = {
            "easy": EASY,
            "medium": MEDIUM,
            "hard": HARD
        }.get(difficulty_name, EASY)
        
        game = Game(screen, difficulty)
        game.run()

    menu = Menu(screen, start_game_callback=start_game)
    menu.run()

if __name__ == "__main__":
    main()