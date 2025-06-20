import pygame
from config import *
from views.menu_view import MenuView

class GameView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 90)  # Крупный, но не слишком
        # Загрузка иконок бонусов
        self.bonus_images = {
            FREEZE: pygame.image.load("assets/images/freeze.png").convert_alpha(),
            TELEPORT: pygame.image.load("assets/images/teleport.png").convert_alpha(),
            PATH_HINT: pygame.image.load("assets/images/path_hint.png").convert_alpha(),
            BOMB: pygame.image.load("assets/images/bomb.png").convert_alpha(),
        }
        # Загрузка изображения флага
        self.flag_img = pygame.image.load("assets/images/flag.png").convert_alpha()
        # Загрузка звука взрыва
        self.boom_sound = pygame.mixer.Sound("assets/sounds/boom.wav")
        # Загрузка всех звуков
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        self.freezing_sound = pygame.mixer.Sound("assets/sounds/freezing.wav")
        self.teleporting_sound = pygame.mixer.Sound("assets/sounds/teleporting.wav")
        self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.wav")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
        # Загрузка фоновой музыки
        self.soundtrack = pygame.mixer.Sound("assets/sounds/soundtrack.wav")
        # Загрузка изображения взрыва
        self.explosion_img = pygame.image.load("assets/images/explosion.png").convert_alpha()
        # Загрузка текстур пола, стен и фона
        self.floor_img = pygame.image.load("assets/images/floor.png").convert()
        self.wall_img = pygame.image.load("assets/images/wall.png").convert()
        self.background = pygame.image.load("assets/images/background.png").convert()
        # Размер видимой области (в клетках)
        self.VIEW_SIZE = 30
    
    def play_boom_sound(self):
        """Воспроизведение звука взрыва"""
        try:
            self.boom_sound.play()
        except:
            pass  # Игнорируем ошибки воспроизведения
    
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
    
    def play_soundtrack(self):
        """Воспроизведение фоновой музыки с зацикливанием"""
        if MenuView.global_music_enabled:  # Проверяем глобальное состояние
            try:
                self.soundtrack.set_volume(0.3)  # Устанавливаем громкость 30%
                self.soundtrack.play(-1)  # -1 означает бесконечное зацикливание
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
    
    def play_explosion_sound(self):
        """Воспроизведение звука взрыва"""
        try:
            # Останавливаем фоновую музыку при взрыве
            self.stop_soundtrack()
            self.boom_sound.play()
        except:
            pass
    
    def draw(self, game_state):
        """Отрисовка игры"""
        self.game_state = game_state  # Для draw_bonuses
        # Фон
        self.screen.blit(pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        # Очистка экрана
        # self.screen.fill(WHITE)  # Больше не нужен
        player_row, player_col = game_state.player.position
        maze = game_state.maze
        # Выбор размера видимой области
        if game_state.level <= 3:
            view_size = max(maze.width, maze.height)
        elif game_state.level == 4:
            view_size = 20
        else:
            view_size = 10
        half = view_size // 2
        # Проверяем, помещается ли лабиринт на экране
        fits_x = maze.width * CELL_SIZE <= WINDOW_WIDTH
        fits_y = maze.height * CELL_SIZE <= WINDOW_HEIGHT
        if game_state.level <= 3 and fits_x and fits_y:
            # Центрируем весь лабиринт в окне
            min_row = 0
            min_col = 0
            offset_x = (WINDOW_WIDTH - maze.width * CELL_SIZE) // 2
            offset_y = (WINDOW_HEIGHT - maze.height * CELL_SIZE) // 2
        elif game_state.level in (4, 5):
            # Центрируем видимую область (view_size x view_size) в окне
            min_row = max(0, min(player_row - half, max(0, maze.height - view_size)))
            min_col = max(0, min(player_col - half, max(0, maze.width - view_size)))
            offset_x = (WINDOW_WIDTH - view_size * CELL_SIZE) // 2
            offset_y = (WINDOW_HEIGHT - view_size * CELL_SIZE) // 2
        else:
            # Камера вокруг игрока
            min_row = max(0, min(player_row - half, max(0, maze.height - view_size)))
            min_col = max(0, min(player_col - half, max(0, maze.width - view_size)))
            offset_x = 0
            offset_y = 0
        self.draw_maze(maze, min_row, min_col, view_size, offset_x, offset_y)
        
        # Отрисовка подсказки пути
        if game_state.show_path_hint and game_state.path_hint:
            self.draw_path_hint(game_state.path_hint, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка игрока
        self.draw_player(game_state.player, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка бонусов
        self.draw_bonuses(game_state.bonuses, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка выхода
        self.draw_exit(game_state.exit, min_row, min_col, offset_x, offset_y)
        
        # Отрисовка анимаций взрыва
        self.draw_explosions(game_state.explosion_animations, min_row, min_col, offset_x, offset_y)
        
        # ТУМАН ВОЙНЫ для уровней 4 и 5
        if game_state.level in (4, 5):
            fog = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA) 
            fog.fill((0, 0, 0, 255))
            player_x = (player_col - min_col) * CELL_SIZE + offset_x + CELL_SIZE // 2
            player_y = (player_row - min_row) * CELL_SIZE + offset_y + CELL_SIZE // 2
            if game_state.level == 4:
                radius = CELL_SIZE * 5
            else:
                radius = CELL_SIZE * 3
            steps = 16
            for i in range(steps, 0, -1):
                alpha = int(255 * (i / steps))
                pygame.draw.circle(fog, (0, 0, 0, alpha), (player_x, player_y), radius + i * 5)
            pygame.draw.circle(fog, (0, 0, 0, 0), (player_x, player_y), radius)
            self.screen.blit(fog, (0, 0))
        
        # Отрисовка UI
        self.draw_ui(game_state)
        
        # Отрисовка экранов состояния
        if game_state.state == VICTORY:
            self.draw_victory_screen(game_state)
        elif game_state.state == 'GAME_OVER':
            self.draw_game_over_screen(game_state)
    
    def draw_maze(self, maze, min_row=0, min_col=0, view_size=15, offset_x=0, offset_y=0):
        """Отрисовка лабиринта"""
        for row in range(min_row, min(min_row + view_size, maze.height)):
            for col in range(min_col, min(min_col + view_size, maze.width)):
                x = (col - min_col) * CELL_SIZE + offset_x
                y = (row - min_row) * CELL_SIZE + offset_y
                if maze.grid[row][col] == 1:  # Стена
                    img = pygame.transform.scale(self.wall_img, (CELL_SIZE, CELL_SIZE))
                    self.screen.blit(img, (x, y))
                else:  # Проход
                    img = pygame.transform.scale(self.floor_img, (CELL_SIZE, CELL_SIZE))
                    self.screen.blit(img, (x, y))
                    pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    def draw_player(self, player, min_row=0, min_col=0, offset_x=0, offset_y=0):
        px, py = player.pixel_pos
        x = (px - min_col) * CELL_SIZE + offset_x
        y = (py - min_row) * CELL_SIZE + offset_y
        
        # Менее насыщенные цвета
        if player.frozen:
            color = (100, 200, 200)  # Светло-голубой вместо CYAN
        else:
            color = (100, 200, 100)  # Светло-зелёный вместо GREEN
        
        pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
        
        # Добавляем глаза
        eye_size = CELL_SIZE // 6
        eye_offset = CELL_SIZE // 4
        
        # Левый глаз
        left_eye_x = x + eye_offset
        left_eye_y = y + eye_offset
        pygame.draw.circle(self.screen, BLACK, (left_eye_x, left_eye_y), eye_size)
        
        # Правый глаз
        right_eye_x = x + CELL_SIZE - eye_offset
        right_eye_y = y + eye_offset
        pygame.draw.circle(self.screen, BLACK, (right_eye_x, right_eye_y), eye_size)
    
    def draw_bonuses(self, bonuses, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка бонусов"""
        for bonus in bonuses:
            if bonus.active:
                x = (bonus.position[1] - min_col) * CELL_SIZE + offset_x
                y = (bonus.position[0] - min_row) * CELL_SIZE + offset_y
                image = self.bonus_images.get(bonus.type)
                if image:
                    image = pygame.transform.smoothscale(image, (CELL_SIZE, CELL_SIZE))
                    self.screen.blit(image, (x, y))
    
    def draw_exit(self, exit_pos, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка выхода"""
        x = (exit_pos[1] - min_col) * CELL_SIZE + offset_x
        y = (exit_pos[0] - min_row) * CELL_SIZE + offset_y
        
        # Отображаем флаг вместо красного квадрата
        try:
            flag_img = pygame.transform.smoothscale(self.flag_img, (CELL_SIZE, CELL_SIZE))
            self.screen.blit(flag_img, (x, y))
        except:
            # Fallback: если флаг не загрузился, рисуем цветной прямоугольник с текстом
            pygame.draw.rect(self.screen, (255, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))  # Жёлтый
            pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
            # Добавляем текст "FLAG"
            flag_text = pygame.font.Font(None, 20).render("FLAG", True, BLACK)
            text_rect = flag_text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
            self.screen.blit(flag_text, text_rect)
    
    def draw_path_hint(self, path_hint, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка подсказки пути"""
        # Исключаем текущую позицию игрока из отображения пути
        # Рисуем путь начиная со второго элемента (индекс 1)
        for i in range(1, len(path_hint) - 1):
            current = path_hint[i]
            next_pos = path_hint[i + 1]
            
            x1 = (current[1] - min_col) * CELL_SIZE + CELL_SIZE // 2 + offset_x
            y1 = (current[0] - min_row) * CELL_SIZE + CELL_SIZE // 2 + offset_y
            x2 = (next_pos[1] - min_col) * CELL_SIZE + CELL_SIZE // 2 + offset_x
            y2 = (next_pos[0] - min_row) * CELL_SIZE + CELL_SIZE // 2 + offset_y
            
            pygame.draw.line(self.screen, YELLOW, (x1, y1), (x2, y2), 2)
    
    def draw_ui(self, game_state):
        """Отрисовка UI"""
        # Светло-зелёная заливка для легенды слева
        legend_width = 200
        legend_height = 200
        legend_surface = pygame.Surface((legend_width, legend_height))
        legend_surface.fill((200, 255, 200))  # Светло-зелёный
        legend_surface.set_alpha(200)  # Полупрозрачность
        self.screen.blit(legend_surface, (5, 5))
        
        # Уровень
        level_text = self.font.render(f"Уровень: {game_state.level}", True, BLACK)
        self.screen.blit(level_text, (10, 10))
        
        # Время
        time_text = self.font.render(f"Время: {game_state.get_game_time():.1f}с", True, BLACK)
        self.screen.blit(time_text, (10, 50))
        
        # Заморозка лабиринта
        if game_state.maze_freeze_timer > 0:
            freeze_text = self.font.render(f"Заморозка: {game_state.maze_freeze_timer:.1f}с", True, BLUE)
            self.screen.blit(freeze_text, (10, 90))
        
        # Подсказка пути
        if game_state.show_path_hint:
            hint_text = self.font.render(f"Путь: {game_state.path_hint_timer:.1f}с", True, YELLOW)
            self.screen.blit(hint_text, (10, 130))
    
    def draw_victory_screen(self, game_state):
        """Отрисовка экрана победы"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        # Тёмно-зелёный цвет
        dark_green = (0, 80, 0)
        victory_text = self.big_font.render("ПОБЕДА!", True, dark_green)
        text_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(victory_text, text_rect)
        
        # Время
        time_text = self.font.render(f"Время: {game_state.get_game_time():.1f}с", True, BLACK)
        time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(time_text, time_rect)
        
        # Инструкции
        if game_state.level + 1 in LEVELS:
            next_text = self.font.render("Следующий уровень (N)", True, BLUE)
            next_rect = next_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(next_text, next_rect)
        
        menu_text = self.font.render("Меню (M)", True, BLACK)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)

    def draw_game_over_screen(self, game_state):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        # Тёмно-красный цвет
        dark_red = (120, 0, 0)
        text1 = self.big_font.render("ИГРА ОКОНЧЕНА!", True, dark_red)
        self.screen.blit(text1, (WINDOW_WIDTH//2 - text1.get_width()//2, WINDOW_HEIGHT//2 - 60))
        
        # Определяем причину смерти
        if hasattr(game_state, 'death_reason') and game_state.death_reason == 'bomb':
            text2 = self.font.render("Не подходи близко к бомбе", True, WHITE)
        else:
            text2 = self.font.render("Монстр вас поймал!", True, WHITE)
        
        text3 = self.font.render("R - Перезапустить уровень", True, WHITE)
        text4 = self.font.render("M - Главное меню", True, WHITE)
        self.screen.blit(text2, (WINDOW_WIDTH//2 - text2.get_width()//2, WINDOW_HEIGHT//2))
        self.screen.blit(text3, (WINDOW_WIDTH//2 - text3.get_width()//2, WINDOW_HEIGHT//2 + 40))
        self.screen.blit(text4, (WINDOW_WIDTH//2 - text4.get_width()//2, WINDOW_HEIGHT//2 + 80))
    
    def draw_explosions(self, explosions, min_row=0, min_col=0, offset_x=0, offset_y=0):
        """Отрисовка анимаций взрыва"""
        for explosion in explosions:
            center_row, center_col = explosion['position']
            size = explosion['size']
            
            # Вычисляем координаты для одной большой картинки взрыва
            x = (center_col - min_col) * CELL_SIZE + offset_x - CELL_SIZE
            y = (center_row - min_row) * CELL_SIZE + offset_y - CELL_SIZE
            
            # Масштабируем изображение взрыва под размер 3x3 клетки
            explosion_size = CELL_SIZE * 3
            explosion_big = pygame.transform.scale(self.explosion_img, (explosion_size, explosion_size))
            self.screen.blit(explosion_big, (x, y)) 