import pygame
import json


class Object:
    def __init__(self, x, y, wall, image):
        self.x = int(x)
        self.y = int(y)
        self.wall = wall
        self.transmission = False
        self.image = image

    def fill_blit(self, screen):
        settings = open("settings.json", "r")
        data = json.load(settings)
        settings.close()
        screen.blit(self.image, (self.x + data["ABS_X"], self.y + data["ABS_Y"]))

class Teleport(Object):
    def __init__(self, x, y, wall, image, next_map):
        super().__init__(x, y, wall, image)

        self.next_map = next_map


def init_map(str_map: str, MAP: list) -> None:
    settings = open("settings.json", "r")
    data = json.load(settings)
    settings.close()
    height = str_map.count("\n")
    str_max = 0
    start_index = 0
    for i in range(height):
        if str_map.find("\n", start_index) - start_index > str_max:
            str_max = str_map.find("\n", start_index) - start_index
        start_index = str_map.find("\n", start_index) + 1
    x = data["WIDTH"]
    y = data["HEIGHT"]
    size_x = x / str_max
    size_y = y / height
    start_index = 0
    start_indey = 0
    for i in range(len(str_map)):
        if str_map[i] == "\n":
            start_index = 0
            start_indey += 1
            continue
        if str_map[i] == "W":
            barrier = pygame.Surface((size_x, size_y))
            wall = Object(size_x * start_index, size_y * start_indey, barrier, pygame.transform.scale(pygame.image.load("models/objects/brick.png"), (barrier.get_width(), barrier.get_height())))
            MAP.append(wall)
        if str_map[i] == "T":
            barrier = pygame.Surface((size_x, size_y))
            teleport = Teleport(size_x * start_index, size_y * start_indey, barrier, pygame.transform.scale(pygame.image.load("models/objects/teleport.png"), (barrier.get_width(), barrier.get_height())), "maps/map_level1.txt")
            teleport.transmission = True
            MAP.append(teleport)
        start_index += 1

def fill_map(game_map, map_object, player) -> None:
    for object in map_object:
        if object.transmission == False:
            for i in range(int(object.y), int(object.y + object.wall.get_height())):
                for j in range(int(object.x), int(object.x + object.wall.get_width())):
                    game_map[j][i] = "W"
        else:
            for i in range(int(object.y), int(object.y + object.wall.get_height())):
                for j in range(int(object.x), int(object.x + object.wall.get_width())):
                    game_map[j][i] = "T"
    for i in range(int(player.y), int(player.y + player.height)):
        for j in range(int(player.x), int(player.x + player.width)):
            game_map[j][i] = "P"