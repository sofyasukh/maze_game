
def apply_fog(surface, visibility_radius):
    fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fog.fill(BLACK)
    center = (player_x, player_y)
    pygame.draw.circle(fog, (0, 0, 0, 0), center, visibility_radius)
    surface.blit(fog, (0, 0))