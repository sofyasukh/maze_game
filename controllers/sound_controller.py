import pygame
from views.menu_view import MenuView

class SoundController:
    def __init__(self):
        # Загрузка всех звуков
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        self.freezing_sound = pygame.mixer.Sound("assets/sounds/freezing.wav")
        self.teleporting_sound = pygame.mixer.Sound("assets/sounds/teleporting.wav")
        self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.wav")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
        self.boom_sound = pygame.mixer.Sound("assets/sounds/boom.wav")
        self.soundtrack = pygame.mixer.Sound("assets/sounds/soundtrack.wav")
        
        # Глобальное состояние музыки
        self.music_enabled = True
    
    def play_click_sound(self):
        """Воспроизведение звука клика"""
        try:
            self.click_sound.play()
        except:
            pass
    
    def play_freezing_sound(self):
        """Воспроизведение звука заморозки"""
        try:
            self.freezing_sound.play()
        except:
            pass
    
    def play_teleporting_sound(self):
        """Воспроизведение звука телепортации"""
        try:
            self.teleporting_sound.play()
        except:
            pass
    
    def play_hint_sound(self):
        """Воспроизведение звука подсказки"""
        try:
            self.hint_sound.play()
        except:
            pass
    
    def play_win_sound(self):
        """Воспроизведение звука победы"""
        try:
            self.win_sound.play()
        except:
            pass
    
    def play_explosion_sound(self):
        """Воспроизведение звука взрыва с остановкой музыки"""
        try:
            self.stop_soundtrack()
            self.boom_sound.play()
        except:
            pass
    
    def play_soundtrack(self):
        """Воспроизведение фоновой музыки с зацикливанием"""
        if self.music_enabled:
            try:
                self.soundtrack.set_volume(0.3)
                self.soundtrack.play(-1)
            except:
                pass
    
    def stop_soundtrack(self):
        """Остановка фоновой музыки"""
        try:
            self.soundtrack.stop()
        except:
            pass
    
    def pause_soundtrack(self):
        """Пауза фоновой музыки"""
        try:
            self.soundtrack.stop()
        except:
            pass
    
    def toggle_music(self):
        """Переключение музыки вкл/выкл"""
        self.music_enabled = not self.music_enabled
        # Синхронизируем с глобальным состоянием
        MenuView.global_music_enabled = self.music_enabled
        if self.music_enabled:
            self.play_soundtrack()
        else:
            self.stop_soundtrack() 