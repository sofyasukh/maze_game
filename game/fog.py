import pygame
from constants import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

class Fog:
    def __init__(self, visibility_radius):
        self.radius = visibility_radius
        self.fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    def update(self, player_pos):
        self.fog_surface.fill((0, 0, 0, 180))  # Полупрозрачный чёрный
        pygame.draw.circle(
            self.fog_surface, (0, 0, 0, 0),
            (player_pos[0], player_pos[1]),
            self.radius
        )
    
    def draw(self, surface):
        surface.blit(self.fog_surface, (0, 0))