import pygame, random

def add_entity(x, y):
    print(x, y)
    the_game[y][x] = 1
def reload_map():
    screen.fill((0, 0, 0))
    for y in range(len(the_game) // 10):
        for x in range(len(the_game[y]) // 10):
            if the_game[y * 10][x * 10] == 1:
                pygame.draw.rect(screen, (255, 0, 0), (y * 10, x * 10, 10, 10))
def select_tool(key):
    global tool
    match key:
        case "1":
            print("Put selected")
    tool = key
def do_tool(pos):
    x, y = pos
    match tool:
        case "1":
            add_entity(x // 10, y // 10)
            reload_map()
        case _:
            print("No tool selected")

pygame.init()
screen = pygame.display.set_mode((500, 500))
the_game = [[0 for i in range(50)] for j in range (50)]
clock = pygame.time.Clock()
is_running = True
tool = "1"
add_entity(random.randint(0, 50), random.randint(0, 50))

reload_map()
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Clic détecté à la position : {event.pos}")
            do_tool(event.pos)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                select_tool(pygame.key.name(event.key))

    #pygame.draw.rect(screen, (255, 0, 0), (100, 100, 50, 50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
