import pygame
import json

settings = open("settings.json", "r")
data = json.load(settings)
settings.close()
class Wall:
    def __init__(self, x, y, wall):
        self.x = int(x)
        self.y = int(y)
        self.image = pygame.transform.scale(pygame.image.load("models/brick.png"),
                                            (wall.get_width(), wall.get_height()))
        self.wall = wall

    def fill_blit(self, screen):
        screen.blit(self.image, (self.x + data["ABS_X"], self.y + data["ABS_Y"]))


def init_map(str_map, MAP):
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
            wall = Wall(size_x * start_index, size_y * start_indey, barrier)
            MAP.append(wall)
        start_index += 1

def fill_map(game_map, map_object, player):
    for object in map_object:
        for i in range(int(object.y), int(object.y + object.wall.get_height())):
            for j in range(int(object.x), int(object.x + object.wall.get_width())):
                game_map[j][i] = "W"
    for i in range(int(player.y), int(player.y + player.height)):
        for j in range(int(player.x), int(player.x + player.width)):
            game_map[j][i] = "P"