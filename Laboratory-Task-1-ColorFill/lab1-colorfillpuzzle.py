import pygame
import sys

pygame.init()

# Константи
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
GRID_SIZE = 5
BOARD_SIZE = 400  # Димензија на таблата
MARGIN = (SCREEN_HEIGHT - BOARD_SIZE) // 2
SQUARE_SIZE = BOARD_SIZE // GRID_SIZE
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Црвена, Зелена, Сина, Жолта
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Фонт
FONT = pygame.font.Font(None, 24)

# Иницијализација на екран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

# Табла
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    """Цртање на таблата со маргини"""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col] if grid[row][col] else WHITE
            x = MARGIN + col * SQUARE_SIZE
            y = MARGIN + row * SQUARE_SIZE
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)

def draw_message(message, color, position="top"):
    """Прикажување порака над таблата"""
    text = FONT.render(message, True, color)
    if position == "top":
        text_rect = text.get_rect(center=(BOARD_SIZE // 2 + MARGIN, MARGIN // 2))
    elif position == "bottom":
        text_rect = text.get_rect(center=(BOARD_SIZE // 2 + MARGIN, SCREEN_HEIGHT - MARGIN // 2))
    screen.blit(text, text_rect)

def draw_rules():
    """Прикажување на правилата десно од таблата"""
    rules = [
        "Правила на играта:",
        "1. Обојте ги сите квадрати во таблата.",
        "2. Два соседни квадрати не смеат да имаат иста боја.",
        "3. Користете копчиња 1-4 за избор на боја.",
        "   -->1-црвена",
        "   -->2-зелена",
        "   -->3-сина",
        "   -->4-жолта",
        "4. Кликнете на квадрат за да го обоите.",
        "5. Притиснете 'R' за ресетирање на таблата."
    ]
    x_offset = MARGIN + BOARD_SIZE + 20  # Почеток на текстот десно од таблата
    y_offset = MARGIN
    for rule in rules:
        text = FONT.render(rule, True, BLACK)
        screen.blit(text, (x_offset, y_offset))
        y_offset += 30  # Простор меѓу редовите

def get_neighbors(row, col):
    """Добивање на соседни квадрати"""
    neighbors = []
    if row > 0: neighbors.append(grid[row - 1][col])  # Горен
    if row < GRID_SIZE - 1: neighbors.append(grid[row + 1][col])  # Долен
    if col > 0: neighbors.append(grid[row][col - 1])  # Лев
    if col < GRID_SIZE - 1: neighbors.append(grid[row][col + 1])  # Десен
    return neighbors

def is_valid_color(row, col, color):
    """Проверка дали бојата е валидна"""
    neighbors = get_neighbors(row, col)
    return color not in neighbors

def is_board_filled():
    """Проверка дали целата табла е обоена"""
    for row in grid:
        if None in row:
            return False
    return True

def main():
    running = True
    selected_color = None
    message = ""
    success_message = ""

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_rules()

        # Прикажи пораки
        if message:
            draw_message(message, (255, 0, 0))  # Црвена боја за грешка
        if success_message:
            draw_message(success_message, (0, 255, 0), position="bottom")  # Зелена порака под таблата

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - MARGIN) // SQUARE_SIZE
                row = (y - MARGIN) // SQUARE_SIZE

                # Проверка дали кликот е во таблата
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    if selected_color and is_valid_color(row, col, selected_color):
                        grid[row][col] = selected_color
                        message = ""

                        # Проверка дали таблата е целосно обоена
                        if is_board_filled():
                            success_message = "Честитки! Успешно ја обоивте целата табла!"
                    elif selected_color:
                        message = "Невалиден потег!"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Ресет
                    for row in range(GRID_SIZE):
                        for col in range(GRID_SIZE):
                            grid[row][col] = None
                    message = ""  # Исчисти ја пораката
                    success_message = ""  # Исчисти ја пораката за успех

                # Избор на боја (1-4 за различни бои)
                if event.key == pygame.K_1: selected_color = COLORS[0]
                if event.key == pygame.K_2: selected_color = COLORS[1]
                if event.key == pygame.K_3: selected_color = COLORS[2]
                if event.key == pygame.K_4: selected_color = COLORS[3]

        pygame.display.flip()

if __name__ == "__main__":
    main()
