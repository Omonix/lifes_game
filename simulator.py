import pygame, copy, random, urllib.request
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import simpledialog

def add_entity(x, y):
    try:
        the_game[y][x] = 1
    except:
        pass
def remove_entity(x, y):
    try:
        the_game[y][x] = 0
    except:
        pass
def reload_map():
    screen.fill((0, 0, 0))
    for y in range(len(the_game)):
        for x in range(len(the_game[y])):
            if the_game[y][x] == 1:
                pygame.draw.rect(screen, colorChoiced, (x * element_size, y * element_size, element_size, element_size))
            if not played:
                pygame.draw.rect(screen, (40, 40, 40), (x * element_size, y * element_size, 10, 10), 1)
def live():
    global the_game
    new_game = copy.deepcopy(the_game)
    for y in range(len(the_game)):
        for x in range(len(the_game[0])):
            friends = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < len(the_game[0]) and 0 <= ny < len(the_game):
                        if (nx != x or ny != y) and the_game[ny][nx] == 1:
                            friends += 1
            if the_game[y][x] == 1:
                if friends != 2 and friends != 3:
                    new_game[y][x] = 0
            else:
                if friends == 3:
                    new_game[y][x] = 1
    the_game = new_game
def greyMode(img):
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            new_color = (r + g + b) // 3
            img.putpixel((x, y), (new_color, new_color, new_color))
def threshold(img, level):
    greyMode(img)
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r < level:
                img.putpixel((x, y), (0, 0, 0))
            else:
                img.putpixel((x, y), (255, 255, 255))
def image_to_map(level):
    global the_game
    try:
        with urllib.request.urlopen(simpledialog.askstring("Entrer l'URL", "Entre l'URL de l'image :")) as response:
            image_choiced = Image.open(BytesIO(response.read())).convert("RGB").resize((width // element_size, height // element_size))
    except:
        return
    threshold(image_choiced, level)
    w, h = image_choiced.size
    the_game = [[0 for i in range(w)] for j in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b = image_choiced.getpixel((x, y))
            if r == 255:
                the_game[y][x] = 1
            else:
                the_game[y][x] = 0
def handle_level():
    global image_level
    try:
        level = int(simpledialog.askstring("Niveau de gris", "Entre le niveau de gris (0-255) :", initialvalue=str(image_level)))
        if 0 <= level <= 255:
            image_level = level
    except:
        pass

pygame.init()
root = tk.Tk()
root.withdraw()

info = pygame.display.Info()
width, height = info.current_w, info.current_h
clock = pygame.time.Clock()
lived = pygame.USEREVENT + 1
pygame.time.set_timer(lived, 75)
element_size = 10
image_level = 80
is_running = True
played = True

screen = pygame.display.set_mode((width, height))
the_game = [[0 for i in range(width // element_size)] for j in range (height // element_size)]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]
colorChoiced = colors[random.randint(0, 6)]

reload_map()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in ["1", "2", "3", "4", "5", "6", "7"]:
                colorChoiced = colors[int(pygame.key.name(event.key)) - 1]
            elif pygame.key.name(event.key) == "space":
                played = not played
            elif pygame.key.name(event.key) == "c":
                the_game = [[0 for i in range(width // element_size)] for j in range (height // element_size)]
            elif pygame.key.name(event.key) == "r":
                the_game = [[random.randint(0, 1) for i in range(width // element_size)] for j in range (height // element_size)]
            elif pygame.key.name(event.key) == "t":
                colorChoiced = colors[random.randint(0, 6)]
            elif pygame.key.name(event.key) == "i":
                image_to_map(image_level)
            elif pygame.key.name(event.key) == "n":
                handle_level()
            elif pygame.key.name(event.key) == "escape":
                is_running = False
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            add_entity(x // element_size, y // element_size)
        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            remove_entity(x // element_size, y // element_size)
        if event.type == lived:
            if played:
                live()
        reload_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
