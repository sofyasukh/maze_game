import pygame
from views.menu_view import MenuView

class SoundController:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        # Получение звуков из AssetManager
        self.click_sound = self.asset_manager.get_sound('click')
        self.freezing_sound = self.asset_manager.get_sound('freezing')
        self.teleporting_sound = self.asset_manager.get_sound('teleporting')
        self.hint_sound = self.asset_manager.get_sound('hint')
        self.win_sound = self.asset_manager.get_sound('win')
        self.boom_sound = self.asset_manager.get_sound('boom')
        self.soundtrack = self.asset_manager.get_sound('soundtrack')
        
        # Глобальное состояние музыки
        self.music_enabled = True
    
    def play_click_sound(self):
        """Воспроизведение звука клика"""
        if self.click_sound:
            self.click_sound.play()
    
    def play_freezing_sound(self):
        """Воспроизведение звука заморозки"""
        if self.freezing_sound:
            self.freezing_sound.play()
    
    def play_teleporting_sound(self):
        """Воспроизведение звука телепортации"""
        if self.teleporting_sound:
            self.teleporting_sound.play()
    
    def play_hint_sound(self):
        """Воспроизведение звука подсказки"""
        if self.hint_sound:
            self.hint_sound.play()
    
    def play_win_sound(self):
        """Воспроизведение звука победы"""
        if self.win_sound:
            self.win_sound.play()
    
    def play_explosion_sound(self):
        """Воспроизведение звука взрыва с остановкой музыки"""
        self.stop_soundtrack()
        if self.boom_sound:
            self.boom_sound.play()
    
    def play_soundtrack(self):
        """Воспроизведение фоновой музыки с зацикливанием"""
        if self.music_enabled and self.soundtrack:
            self.soundtrack.set_volume(0.3)
            self.soundtrack.play(-1)
    
    def stop_soundtrack(self):
        """Остановка фоновой музыки"""
        if self.soundtrack:
            self.soundtrack.stop()
    
    def pause_soundtrack(self):
        """Пауза фоновой музыки"""
        if self.soundtrack:
            self.soundtrack.stop()
    
    def toggle_music(self):
        """Переключение музыки вкл/выкл"""
        self.music_enabled = not self.music_enabled
        # Синхронизируем с глобальным состоянием
        MenuView.global_music_enabled = self.music_enabled
        if self.music_enabled:
            self.play_soundtrack()
        else:
            self.stop_soundtrack() 