import sys
import threading
import numpy
import pygame.display

from PyQt5.QtWidgets import QDesktopWidget, QApplication
app = QApplication(sys.argv)
q = QDesktopWidget().availableGeometry()

from maps import *
from player import *

f = open("settings.json", "r")
data = json.load(f)
f.close()
HEIGHT = data["HEIGHT"]
WIDTH = data["WIDTH"]
FULL_HEIGHT = data["FULL_HEIGHT"]
FULL_WIDTH = data["FULL_WIDTH"]
ABS_X = data["ABS_X"]
ABS_Y = data["ABS_Y"]
FPS = data["FPS"]



map_level0 = 'WWWW  WWWW\n' \
             'W        W\n' \
             '         W\n' \
             'W        W\n' \
             'WWWW  WWWW\n'

pygame.init()
clock = pygame.time.Clock()
interface_map = numpy.empty((FULL_WIDTH + 1, FULL_HEIGHT + 1), dtype="object")
interface_map[...] = "N"
MouseUp = False

# Основное игровое меню
class Game:

    def __init__(self, FULL_HEIGHT, FULL_WIDTH, HEIGHT, WIDTH, ABS_X, ABS_Y, FPS, interface_map, player):
        self.FULL_HEIGHT = FULL_HEIGHT
        self.FULL_WIDTH = FULL_WIDTH
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.ABS_X = ABS_X
        self.ABS_Y = ABS_Y
        self.FPS = FPS
        self.size = (FULL_WIDTH, FULL_HEIGHT)

        self.game_map = None
        self.interface_map = interface_map
        self.player = player
        self.screen = pygame.display.set_mode([self.FULL_WIDTH, self.FULL_HEIGHT], pygame.RESIZABLE)

        # Игрок и его составляющие
        self.OBJECTS = [player]

        # Враги
        self.ENEMYS = []

        # Стенки
        self.MAP = []

        # Меню
        self.INTERFACE = []

    def display_obj(self):
        self.screen.fill((0, 0, 0))
        for enemy in self.ENEMYS:
            enemy.movement()
            self.screen.blit(enemy.image, (enemy.x, enemy.y))
        for map_object in self.MAP:
            map_object.fill_blit(self.screen)
        for object in self.OBJECTS:
            self.screen.blit(object.image, (object.x + self.ABS_X, object.y + self.ABS_Y))
        for inter_object in self.INTERFACE:
            if inter_object.is_on == True:
                inter_object.fill_blit(self.screen)
        pygame.display.update()

    def display_reboot(self):
        self.INTERFACE = []
        self.MAP = []
        self.game_map = numpy.empty((self.WIDTH + 1, self.HEIGHT + 1), dtype="object")
        self.game_map[...] = "N"
        init_map(map_level0, self.MAP)
        fill_map(self.game_map, self.MAP, self.player)
        self.display_obj()
        self.fill_interface()
    def display(self):
        self.display_reboot()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    self.FULL_WIDTH = event.size[0]
                    self.FULL_HEIGHT = event.size[1]
                    self.WIDTH = self.FULL_WIDTH - 80
                    self.HEIGHT = self.FULL_HEIGHT - 80
                    data["FULL_WIDTH"] = event.size[0]
                    data["FULL_HEIGHT"] = event.size[1]
                    data["WIDTH"] = self.FULL_WIDTH - 80
                    data["HEIGHT"] = self.FULL_HEIGHT - 80
                    player.x = int(data["WIDTH"] / 2)
                    player.y = int(data["HEIGHT"] / 2)
                    with open("settings.json", "w") as setting:
                        setting.write(json.dumps(data))
                    self.display_reboot()
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
            # threading.Thread(target=player.attack(mouses)).start()

            threading.Thread(target=self.display_obj()).start()
            threading.Thread(target=player.movement(keys, self.game_map, data)).start()
            #threading.Thread(target=init_menu(mouses)).start()

    def fill_interface(self):
        Border_Left = Menu("models/menu/menu.png", 0, 0, self.ABS_X, self.FULL_HEIGHT, True)
        Border_Top = Menu("models/menu/menu.png", 0, 0, self.FULL_WIDTH, self.ABS_Y, True)
        Border_Right = Menu("models/menu/menu.png", self.FULL_WIDTH - self.ABS_X, 0, self.ABS_X, self.FULL_HEIGHT - self.ABS_Y, True)
        Inventory = Menu("models/menu/inventory.png", self.FULL_WIDTH - 200, self.FULL_HEIGHT - self.ABS_Y, 200,
                         self.FULL_HEIGHT - self.HEIGHT - self.ABS_Y, True)
        Fill_Menu = Menu("models/menu/menu.png", 0, self.FULL_HEIGHT - self.ABS_Y, self.FULL_WIDTH - 200, self.FULL_HEIGHT - self.HEIGHT - self.ABS_Y,
                         True)
        self.INTERFACE.append(Fill_Menu)
        self.INTERFACE.append(Inventory)
        interface_menu = Menu("models/menu/menu_rgb.png", 400, 400, 300, 300, False)
        self.INTERFACE.append(interface_menu)
        self.INTERFACE.append(Border_Left)
        self.INTERFACE.append(Border_Top)
        self.INTERFACE.append(Border_Right)


# Создание дисплея

class Menu:
    def __init__(self, image, x, y, x_line, y_line, is_on):
        self.x = x
        self.y = y
        self.x_line = x_line
        self.y_line = y_line
        self.image = pygame.transform.scale(pygame.image.load(image),(x_line, y_line))
        self.is_on = is_on

    def fill_blit(self, screen):
        screen.blit(self.image, (self.x, self.y))



'''def init_menu(mouses):
    global MouseUp
    if mouses[0]:
        if not MouseUp:
            if interface_menu.is_on == False:
                interface_menu.is_on = True
            elif interface_menu.is_on == True:
                interface_menu.is_on = False
            MouseUp = True
    if not mouses[0]:
        MouseUp = False'''




player = Player(data)
game = Game(FULL_HEIGHT, FULL_WIDTH, HEIGHT, WIDTH, ABS_X, ABS_Y, FPS, interface_map, player)

'''enemy = Enemy(50, 60, 600, 400)  #Создание врага
enemys.append(enemy)'''

game.display()
