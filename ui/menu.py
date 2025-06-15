import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, YELLOW, RED
from utils.file_utils import load_records

class Button:
    """Класс для создания интерактивных кнопок."""
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        """Отрисовывает кнопку с эффектом наведения."""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        """Проверяет, находится ли курсор над кнопкой."""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        """Проверяет клик по кнопке."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Menu:
    """Главное меню игры с выбором уровня сложности."""
    def __init__(self, screen, start_game_callback):
        self.screen = screen
        self.start_game = start_game_callback
        self.records = load_records()
        self.buttons = self._create_buttons()
        self.title_font = pygame.font.Font(None, 72)
        self.record_font = pygame.font.Font(None, 28)

    def _create_buttons(self):
        """Создаёт кнопки для меню."""
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        return [
            Button(center_x, 200, button_width, button_height, "Лёгкий", GREEN, (100, 255, 100)),
            Button(center_x, 280, button_width, button_height, "Средний", YELLOW, (255, 255, 100)),
            Button(center_x, 360, button_width, button_height, "Сложный", RED, (255, 100, 100)),
            Button(center_x, 450, button_width, button_height, "Выход", (200, 200, 200), (150, 150, 150))
        ]

    def draw(self):
        """Отрисовывает все элементы меню."""
        self.screen.fill(WHITE)
        
        # Заголовок
        title = self.title_font.render("Динамический Лабиринт", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen)
        
        # Рекорды
        self._draw_records()
        
        pygame.display.flip()

    def _draw_records(self):
        """Отображает таблицу рекордов."""
        y_offset = 520
        records_title = self.record_font.render("Лучшее время:", True, BLACK)
        self.screen.blit(records_title, (50, y_offset))
        
        records = [
            f"Лёгкий: {self.records.get('Лёгкий', '--:--')} сек",
            f"Средний: {self.records.get('Средний', '--:--')} сек",
            f"Сложный: {self.records.get('Сложный', '--:--')} сек"
        ]
        
        for i, record in enumerate(records):
            record_text = self.record_font.render(record, True, BLACK)
            self.screen.blit(record_text, (50, y_offset + 30 + i * 25))

    def handle_events(self):
        """Обрабатывает события меню."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Проверка кликов по кнопкам
            if self.buttons[0].is_clicked(mouse_pos, event):
                self.start_game("easy")
            elif self.buttons[1].is_clicked(mouse_pos, event):
                self.start_game("medium")
            elif self.buttons[2].is_clicked(mouse_pos, event):
                self.start_game("hard")
            elif self.buttons[3].is_clicked(mouse_pos, event):
                return False
        
        return True

    def update_records(self, new_records):
        """Обновляет отображаемые рекорды."""
        self.records = new_records

    def run(self):
        """Запускает цикл меню."""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.time.Clock().tick(60)