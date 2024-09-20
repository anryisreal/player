import sys
import threading
import numpy
import pygame.display

from maps import *
from player import *
from interface import *

class Game:

    def __init__(self, FULL_HEIGHT: int, FULL_WIDTH: int, HEIGHT: int, WIDTH: int, ABS_X: int, ABS_Y: int, FPS: int, player: Player):
        self.FULL_HEIGHT = FULL_HEIGHT
        self.FULL_WIDTH = FULL_WIDTH
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.ABS_X = ABS_X
        self.ABS_Y = ABS_Y
        self.FPS = FPS
        self.size = (FULL_WIDTH, FULL_HEIGHT)

        self.game_map = None
        self.interface_map = None
        self.player = player
        self.screen = pygame.display.set_mode([self.FULL_WIDTH, self.FULL_HEIGHT], pygame.RESIZABLE)

        # Игрок и его составляющие
        self.OBJECTS = [player]

        # Враги
        self.ENEMYS = []

        # Стенки
        self.MAP = []

        # Меню
        self.INTERFACE = Interface(FULL_HEIGHT, FULL_WIDTH, HEIGHT, WIDTH, ABS_X, ABS_Y)

        # Уникальные обьекты
        self.UNIQUE_OBJECTS = dict()

    # Загрузка обьектов игрового дисплея
    def display_obj(self) -> None:
        self.screen.fill((0, 0, 0))
        if self.INTERFACE.type != 0:
            for enemy in self.ENEMYS:
                enemy.movement()
                self.screen.blit(enemy.image, (enemy.x, enemy.y))
            for map_object in self.MAP:
                map_object.fill_blit(self.screen)
            for object in self.OBJECTS:
                self.screen.blit(object.image, (object.x + self.ABS_X, object.y + self.ABS_Y))
        for inter_object in self.INTERFACE.Windows:
            if inter_object.Property.is_on == True:
                inter_object.fill_blit(self.screen)
        pygame.display.update()


    # Перезагрузка игрового дисплея
    def display_reboot(self) -> None:
        if self.INTERFACE.type != 0:
            self.INTERFACE.Windows = []
            self.MAP = []
            self.game_map = numpy.empty((self.WIDTH + 1, self.HEIGHT + 1), dtype="object")
            self.game_map[...] = "N"
            self.interface_map = numpy.empty((data["FULL_WIDTH"] + 1, data["FULL_HEIGHT"] + 1), dtype="object")
            self.interface_map[...] = "N"
            init_map(map_level0, self.MAP, self.UNIQUE_OBJECTS)
            fill_map(self.game_map, self.MAP, self.player)
            self.display_obj()
        self.INTERFACE.fill_interface()

    def resize(self, event):
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

    # Загрузка игрового дисплея

    def CheckEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.resize(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def display(self) -> None:
        self.display_reboot()
        while True:
            clock.tick(self.FPS)
            self.CheckEvent()

            keys = pygame.key.get_pressed()

            threading.Thread(target=self.display_obj()).start()
            threading.Thread(target=player.movement(keys, self.game_map, data)).start()
            if player.obj != None:
                print(self.UNIQUE_OBJECTS)

    def BuilderMode(self):
        pass


    def authentication(self):
        self.display_reboot()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.resize(event)
                for textbox in self.INTERFACE.Active:
                    textbox.interaction(event, self.player)
                    if player.login != None:
                        self.INTERFACE.type = 1
                        return


            threading.Thread(target=self.display_obj()).start()

    def selectMode(self):
        self.display_reboot()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.resize(event)
                for selectB in self.INTERFACE.Active:
                    if (selectB.interaction(event) != None):
                        print(123123)
                        return


            threading.Thread(target=self.display_obj()).start()





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



if __name__ == "__main__":

    pygame.init()
    clock = pygame.time.Clock()
    MouseUp = False

    f = open("settings.json", "r")
    data = json.load(f)
    f.close()

    with open("../maps/map_level0.txt", "r") as map:
        map_level0 = map.read()
    player = Player(data)
    game = Game(data["FULL_HEIGHT"], data["FULL_WIDTH"], data["HEIGHT"], data["WIDTH"], data["ABS_X"], data["ABS_Y"], data["FPS"], player)
    game.authentication()
    game.selectMode()
    game.display()

