import random
from typing import Tuple, List

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = []
        self.changing_walls = []
        self.last_change = 0
        self.generate()
    
    def generate(self):
        """Генерация классического лабиринта с гарантированной проходимостью"""
        # 1. Сетка стен
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # 2. Классический DFS (backtracking) по всей сетке
        self.dfs_maze_classic(1, 1, set())

        # 3. Вход и выход
        self.grid[0][1] = 0
        self.grid[1][1] = 0
        self.grid[self.height - 1][self.width - 2] = 0
        self.grid[self.height - 2][self.width - 2] = 0

        # 4. Проверяем путь от старта к выходу
        from_pos = (1, 1)
        to_pos = (self.height - 2, self.width - 2)
        path = self.find_path(from_pos, to_pos)
        if not path:
            # Если пути нет, соединяем прямым коридором
            self.create_direct_path(from_pos, to_pos)

        # 5. Немного дополнительных проходов
        self.add_extra_passages(minimal=True)
        self.create_changing_walls()

    def create_snake_path(self, start, end):
        """Генерирует гарантированный путь через случайные точки"""
        points = [start]
        num_waypoints = random.randint(3, 6)
        for i in range(num_waypoints):
            row = random.randint(1, self.height - 2)
            col = random.randint(1, self.width - 2)
            points.append((row, col))
        points.append(end)
        # Соединяем точки прямыми отрезками
        path = []
        for i in range(len(points) - 1):
            path += self.straight_line(points[i], points[i+1])
        return path

    def straight_line(self, a, b):
        """Возвращает клетки прямой линии между двумя точками (манхэттен)"""
        path = []
        r, c = a
        r2, c2 = b
        while (r, c) != (r2, c2):
            path.append((r, c))
            if r != r2:
                r += 1 if r2 > r else -1
            elif c != c2:
                c += 1 if c2 > c else -1
        path.append((r2, c2))
        return path

    def dfs_maze_classic(self, row, col, reserved):
        """DFS-генерация лабиринта с тропинками шириной 1 клетка, не затирая reserved (гарантированный путь)"""
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = row + dr * 2, col + dc * 2
            if 1 <= nr < self.height - 1 and 1 <= nc < self.width - 1:
                if self.grid[nr][nc] == 1 and (nr, nc) not in reserved:
                    self.grid[nr][nc] = 0
                    self.grid[row + dr][col + dc] = 0
                    self.dfs_maze_classic(nr, nc, reserved)

    def create_vertical_wall(self, x: int, y1: int, y2: int):
        """Создание вертикальной стены с проходами"""
        # Создаем стену
        for y in range(y1, y2 + 1):
            self.grid[y][x] = 1
        
        # Создаем несколько проходов в стене (1-3 прохода)
        num_passages = random.randint(1, 3)
        for _ in range(num_passages):
            passage_y = random.randint(y1, y2)
            self.grid[passage_y][x] = 0
    
    def create_horizontal_wall(self, y: int, x1: int, x2: int):
        """Создание горизонтальной стены с проходами"""
        # Создаем стену
        for x in range(x1, x2 + 1):
            self.grid[y][x] = 1
        
        # Создаем несколько проходов в стене (1-3 прохода)
        num_passages = random.randint(1, 3)
        for _ in range(num_passages):
            passage_x = random.randint(x1, x2)
            self.grid[y][passage_x] = 0
    
    def create_entrance_exit(self):
        """Создание входа и выхода"""
        # Вход (верхняя часть)
        self.grid[0][1] = 0
        self.grid[1][1] = 0
        
        # Выход (нижняя часть)
        self.grid[self.height - 1][self.width - 2] = 0
        self.grid[self.height - 2][self.width - 2] = 0
        
        # Создаем путь от входа к основной части лабиринта
        self.connect_entrance()
        
        # Создаем путь от выхода к основной части лабиринта
        self.connect_exit()
    
    def connect_entrance(self):
        """Подключение входа к лабиринту"""
        # Ищем ближайшую пустую клетку от входа
        for y in range(2, min(5, self.height - 1)):
            for x in range(1, min(4, self.width - 1)):
                if self.grid[y][x] == 0:
                    # Создаем путь от входа к этой клетке
                    self.create_path((1, 1), (y, x))
                    return
    
    def connect_exit(self):
        """Подключение выхода к лабиринту"""
        # Ищем ближайшую пустую клетку от выхода
        for y in range(self.height - 3, max(self.height - 6, 1), -1):
            for x in range(self.width - 3, max(self.width - 6, 1), -1):
                if self.grid[y][x] == 0:
                    # Создаем путь от выхода к этой клетке
                    self.create_path((self.height - 2, self.width - 2), (y, x))
                    return
    
    def create_path(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Создание пути между двумя точками"""
        current = start
        
        while current != end:
            # Определяем направление к цели
            dr = end[0] - current[0]
            dc = end[1] - current[1]
            
            # Выбираем направление
            if abs(dr) > abs(dc):
                step = 1 if dr > 0 else -1
                new_pos = (current[0] + step, current[1])
            else:
                step = 1 if dc > 0 else -1
                new_pos = (current[0], current[1] + step)
            
            # Проверяем границы и создаем путь
            if (0 <= new_pos[0] < self.height and 
                0 <= new_pos[1] < self.width):
                self.grid[new_pos[0]][new_pos[1]] = 0
                current = new_pos
            else:
                break
    
    def add_extra_passages(self, minimal=False):
        """Добавление дополнительных проходов для связности"""
        # Меньше проходов, если minimal=True
        extra_count = (self.width * self.height) // (40 if minimal else 15)
        for _ in range(extra_count):
            row = random.randint(1, self.height - 2)
            col = random.randint(1, self.width - 2)
            if random.random() < (0.2 if minimal else 0.5):
                self.grid[row][col] = 0
        self.create_connecting_passages()
    
    def create_connecting_passages(self):
        """Создание проходов для соединения изолированных областей"""
        # Проходим по всей сетке и создаем проходы в стенах
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.grid[row][col] == 1:  # Если это стена
                    # Проверяем соседние клетки
                    neighbors = [
                        (row-1, col), (row+1, col),  # Вертикальные соседи
                        (row, col-1), (row, col+1)   # Горизонтальные соседи
                    ]
                    
                    # Если рядом есть пустые клетки, создаем проход
                    empty_neighbors = 0
                    for nr, nc in neighbors:
                        if (0 <= nr < self.height and 0 <= nc < self.width and 
                            self.grid[nr][nc] == 0):
                            empty_neighbors += 1
                    
                    # Если рядом есть пустые клетки, создаем проход с некоторой вероятностью
                    if empty_neighbors > 0 and random.random() < 0.3:
                        self.grid[row][col] = 0
    
    def create_changing_walls(self):
        """Создание меняющихся стен"""
        self.changing_walls = []
        change_count = (self.width * self.height) // 30
        
        for _ in range(change_count):
            row = random.randint(1, self.height - 2)
            col = random.randint(1, self.width - 2)
            
            # Добавляем стену как меняющуюся
            if self.grid[row][col] == 0:
                self.changing_walls.append((row, col))
    
    def update_changing_walls(self, current_time):
        """Обновление меняющихся стен"""
        if current_time - self.last_change > 3000:  # 3 секунды
            self.last_change = current_time
            
            for wall_pos in self.changing_walls:
                row, col = wall_pos
                # Инвертируем стену
                self.grid[row][col] = 1 - self.grid[row][col]
    
    def get_random_position(self) -> Tuple[int, int]:
        """Получение случайной пустой позиции"""
        attempts = 0
        while attempts < 100:
            row = random.randint(1, self.height - 2)
            col = random.randint(1, self.width - 2)
            if self.grid[row][col] == 0:
                return (row, col)
            attempts += 1
        return (1, 1)  # Fallback
    
    def is_wall(self, position: Tuple[int, int]) -> bool:
        """Проверка, является ли позиция стеной"""
        row, col = position
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col] == 1
        return True
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Поиск кратчайшего пути (A*)"""
        if start == goal:
            return [start]
        
        open_set = [start]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            
            if current == goal:
                return self.reconstruct_path(came_from, current)
            
            open_set.remove(current)
            
            # Проверяем соседей
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + dr, current[1] + dc)
                
                if (0 <= neighbor[0] < self.height and 
                    0 <= neighbor[1] < self.width and 
                    self.grid[neighbor[0]][neighbor[1]] == 0):
                    
                    tentative_g = g_score.get(current, float('inf')) + 1
                    
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                        
                        if neighbor not in open_set:
                            open_set.append(neighbor)
        
        return []  # Путь не найден
    
    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Манхэттенское расстояние"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Восстановление пути"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
    
    def ensure_path_to_exit(self):
        """Гарантированное создание пути от входа к выходу"""
        # Находим путь от входа к выходу
        path = self.find_path((1, 1), (self.height - 2, self.width - 2))
        
        if not path:
            # Если путь не найден, создаем его принудительно
            self.create_forced_path()
    
    def create_forced_path(self):
        """Создание принудительного пути от входа к выходу"""
        # Создаем путь через центр лабиринта
        center_row = self.height // 2
        center_col = self.width // 2
        
        # Путь от входа к центру
        self.create_direct_path((1, 1), (center_row, center_col))
        
        # Путь от центра к выходу
        self.create_direct_path((center_row, center_col), (self.height - 2, self.width - 2))
    
    def create_direct_path(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Создание прямого пути между двумя точками"""
        current = start
        
        while current != end:
            # Определяем направление к цели
            dr = end[0] - current[0]
            dc = end[1] - current[1]
            
            # Выбираем направление
            if abs(dr) > abs(dc):
                step = 1 if dr > 0 else -1
                new_pos = (current[0] + step, current[1])
            else:
                step = 1 if dc > 0 else -1
                new_pos = (current[0], current[1] + step)
            
            # Проверяем границы и создаем путь
            if (0 <= new_pos[0] < self.height and 
                0 <= new_pos[1] < self.width):
                self.grid[new_pos[0]][new_pos[1]] = 0
                current = new_pos
            else:
                break 