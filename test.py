import pygame
import sys

# Config
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ALIVE_COLOR = (0, 200, 0)
GRID_COLOR = (40, 40, 40)

# Init Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de la Vie - Conway")
clock = pygame.time.Clock()

# Fonctions
def empty_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def count_neighbors(grid, x, y):
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH:
            count += grid[nx][ny]
    return count

def update(grid):
    new_grid = empty_grid()
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            neighbors = count_neighbors(grid, i, j)
            if grid[i][j] == 1 and neighbors in [2, 3]:
                new_grid[i][j] = 1
            elif grid[i][j] == 0 and neighbors == 3:
                new_grid[i][j] = 1
    return new_grid

def draw_grid(grid):
    screen.fill(BLACK)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            if grid[i][j] == 1:
                pygame.draw.rect(screen, ALIVE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)
    pygame.display.flip()

# Grille de base
grid = empty_grid()
running = True
paused = True

# Boucle principale
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Touche clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_c:
                grid = empty_grid()
            elif event.key == pygame.K_r:
                import random
                grid = [[random.randint(0, 1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Clic souris
        if pygame.mouse.get_pressed()[0]:  # Clic gauche
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x, mouse_y)
            j = mouse_x // CELL_SIZE
            i = mouse_y // CELL_SIZE
            if 0 <= i < GRID_HEIGHT and 0 <= j < GRID_WIDTH:
                grid[i][j] = 1
        elif pygame.mouse.get_pressed()[2]:  # Clic droit
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x, mouse_y)
            j = mouse_x // CELL_SIZE
            i = mouse_y // CELL_SIZE
            if 0 <= i < GRID_HEIGHT and 0 <= j < GRID_WIDTH:
                grid[i][j] = 0

    if not paused:
        grid = update(grid)

    draw_grid(grid)

pygame.quit()
sys.exit()
