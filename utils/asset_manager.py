import pygame

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, key, path):
        """Загружает изображение и сохраняет его."""
        try:
            self.images[key] = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Не удалось загрузить изображение: {path}")
            print(e)
            # Можно установить "заглушку"
            self.images[key] = pygame.Surface((32, 32))
            self.images[key].fill((255, 0, 255))

    def load_sound(self, key, path):
        """Загружает звук и сохраняет его."""
        try:
            self.sounds[key] = pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Не удалось загрузить звук: {path}")
            print(e)
            self.sounds[key] = None # Или заглушка

    def get_image(self, key):
        """Возвращает загруженное изображение по ключу."""
        return self.images.get(key)

    def get_sound(self, key):
        """Возвращает загруженный звук по ключу."""
        return self.sounds.get(key) 