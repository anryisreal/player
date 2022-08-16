import sys
import pygame
import threading
import numpy
from maps import *
from player import *
from settings import *

pygame.init()
screen = pygame.display.set_mode([FULL_WIDTH, FULL_HEIGHT])
clock = pygame.time.Clock()
game_map = numpy.empty((WIDTH + 1, HEIGHT + 1), dtype="object")
game_map[...] = "N"
interface_map = numpy.empty((FULL_WIDTH + 1, FULL_HEIGHT + 1), dtype="object")
interface_map[...] = "N"
MouseUp = False


# Создание дисплея

class Menu:
    def __init__(self, image, x, y, x_line, y_line, is_on):
        self.x = x
        self.y = y
        self.x_line = x_line
        self.y_line = y_line
        self.image = pygame.transform.scale(pygame.image.load(image),(x_line, y_line))
        self.is_on = is_on

    def fill_blit(self):
        screen.blit(self.image, (self.x, self.y))

Border_Left = Menu("models/menu/menu.png", 0, 0, ABS_X, FULL_HEIGHT, True)
Border_Top = Menu("models/menu/menu.png", 0, 0, FULL_WIDTH, ABS_Y, True)
Border_Right = Menu("models/menu/menu.png", FULL_WIDTH - ABS_X, 0, ABS_X, FULL_HEIGHT - ABS_Y, True)
Inventory = Menu("models/menu/inventory.png", FULL_WIDTH - 200, FULL_HEIGHT - ABS_Y, 200, FULL_HEIGHT - HEIGHT - ABS_Y, True)
Fill_Menu = Menu("models/menu/menu.png", 0, FULL_HEIGHT - ABS_Y, FULL_WIDTH - 200, FULL_HEIGHT - HEIGHT - ABS_Y, True)
INTERFACE.append(Fill_Menu)
INTERFACE.append(Inventory)
interface_menu = Menu("models/menu/menu_rgb.png", 400, 400, 300, 300, False)
INTERFACE.append(interface_menu)
INTERFACE.append(Border_Left)
INTERFACE.append(Border_Top)
INTERFACE.append(Border_Right)


def init_menu(mouses):
    global MouseUp
    if mouses[0]:
        if not MouseUp:
            if interface_menu.is_on == False:
                interface_menu.is_on = True
            elif interface_menu.is_on == True:
                interface_menu.is_on = False
            MouseUp = True
    if not mouses[0]:
        MouseUp = False


def display_obj():
    screen.fill((0, 0, 0))
    for enemy in ENEMYS:
        enemy.movement()
        screen.blit(enemy.image, (enemy.x, enemy.y))
    for map_object in MAP:
        map_object.fill_blit(screen)
    for object in OBJECTS:
        screen.blit(object.image, (object.x + ABS_X, object.y + ABS_Y))
    for inter_object in INTERFACE:
        if inter_object.is_on == True:
            inter_object.fill_blit()
    pygame.display.update()


def display():
    init_map(map_level0)
    fill_map(game_map, MAP, player)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            '''if event.type == pygame.KEYDOWN and player.firstshot == False:
                if event.key == pygame.K_SPACE:
                    shot = Shot(player.x, player.y)
                    objects.append(shot)
                    threading.Thread(target=shot.shot).start()                      #Отслеживание стрельбы
                    player.firstshot = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.firstshot = False
                    continue'''

        keys = pygame.key.get_pressed()
        mouses = pygame.mouse.get_pressed()
        #threading.Thread(target=player.attack(mouses)).start()
        threading.Thread(target=player.movement(keys, game_map)).start()
        threading.Thread(target=init_menu(mouses)).start()
        threading.Thread(target=display_obj).start()


player = Player()
OBJECTS.append(player)

'''enemy = Enemy(50, 60, 600, 400)  #Создание врага
enemys.append(enemy)'''

display()
