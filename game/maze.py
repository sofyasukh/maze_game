import pygame
import random
from constants import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

class Maze:
    def __init__(self, width, height):
        self.width = width // CELL_SIZE
        self.height = height // CELL_SIZE
        self.grid = self._generate_maze()
        self.exit_pos = (self.width-2, self.height-2)  # Правый нижний угол
        self._ensure_path()

    def _generate_maze(self):
        """Генерация лабиринта алгоритмом Depth-First Search"""
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        stack = [(0, 0)]
        grid[0][0] = 0  # Стартовая точка

        while stack:
            x, y = stack[-1]
            neighbors = self._get_unvisited_neighbors(x, y, grid)
            if neighbors:
                nx, ny = random.choice(neighbors)
                grid[ny][nx] = 0
                grid[y + (ny-y)//2][x + (nx-x)//2] = 0  # Убираем стену между
                stack.append((nx, ny))
            else:
                stack.pop()
        return grid

    def _get_unvisited_neighbors(self, x, y, grid):
        """Возвращает непосещённых соседей для алгоритма DFS"""
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        neighbors = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and grid[ny][nx] == 1:
                neighbors.append((nx, ny))
        return neighbors

    def _ensure_path(self):
        """Гарантирует путь от старта до выхода (алгоритм BFS)"""
        from collections import deque
        start = (0, 0)
        queue = deque([start])
        visited = set([start])
        parent = {}

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit_pos:
                break
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] == 0 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
        else:
            # Если путь не найден, создаём проход
            self.grid[self.exit_pos[1]][self.exit_pos[0]] = 0
            self.grid[self.exit_pos[1]-1][self.exit_pos[0]] = 0

    def draw(self, surface, player_pos):
        """Отрисовка лабиринта с центрированием на игроке"""
        player_x, player_y = player_pos
        offset_x = SCREEN_WIDTH // 2 - player_x
        offset_y = SCREEN_HEIGHT // 2 - player_y

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:  # Стена
                    rect = pygame.Rect(
                        x * CELL_SIZE + offset_x,
                        y * CELL_SIZE + offset_y,
                        CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(surface, WHITE, rect)