import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, EASY, MEDIUM, HARD
from game.game import Game
from ui.menu import Menu
from utils.file_utils import load_records, save_record

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen, self.start_game)
        self.game_instance = None

    def start_game(self, difficulty):
        self.game_instance = Game(
            screen=self.screen,
            difficulty=difficulty,
            completion_callback=self.on_game_complete
        )
        self.run_game()

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

            self.game_instance.update(1/60)
            self.game_instance.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self.menu.run()

if __name__ == "__main__":
    game = MazeGame()
    game.run()