import pygame
from settings import *

class Player:

    def __init__(self):
        self.width = 51
        self.height = 70
        self.image = pygame.image.load("models/Player/Player_W.png")
        self.x = int(WIDTH / 2)
        self.y = int(HEIGHT / 2)
        self.speed = 6
        self.space_x = 0
        self.space_y = 0
        self.stop_x = 0
        self.stop_y = 0
        self.MouseUp = False

    def movement(self, keys, game_map):
        if keys[pygame.K_w]:
            self.image = pygame.image.load("models/Player/Player_W.png")
            for i in range(self.speed):
                if self.y == 0:
                    return
                else:
                    for i in range(self.x, self.x + self.width):
                        if game_map[self.y - 1][i] == "W":
                            return
                    for i in range(self.x, self.x + self.width):
                        game_map[self.y - 1][i] = "P"
                        game_map[self.y + self.height][i] = "N"
                    self.y -= 1

        if keys[pygame.K_s]:
            self.image = pygame.image.load("models/Player/Player_S.png")
            for i in range(self.speed):
                if self.y + self.height == HEIGHT:
                    return
                else:
                    for i in range(self.x, self.x + self.width):
                        if game_map[self.y + self.height + 1][i] == "W":
                            return
                    for i in range(self.x, self.x + self.width):
                        game_map[self.y + self.height + 1][i] = "P"
                        game_map[self.y][i] = "N"
                    self.y += 1

        if keys[pygame.K_a]:
            self.image = pygame.image.load("models/Player/Player_A.png")
            for i in range(self.speed):
                if self.x == 0:
                    return
                else:
                    for i in range(self.y, self.y + self.height):
                        if game_map[i][self.x - 1] == "W":
                            return
                    for i in range(self.y, self.y + self.height):
                        game_map[i][self.x - 1] = "P"
                        game_map[i][self.x + self.width] = "N"
                    self.x -= 1

        if keys[pygame.K_d]:
            self.image = pygame.image.load("models/Player/Player_D.png")
            for i in range(self.speed):
                if self.x + self.width == WIDTH:
                    return
                else:
                    for i in range(self.y, self.y + self.height):
                        if game_map[i][self.x + self.width + 1] == "W":
                            return
                    for i in range(self.y, self.y + self.height):
                        game_map[i][self.x + self.width + 1] = "P"
                        game_map[i][self.x] = "N"
                    self.x += 1

    '''def attack(self, mouses):
        if mouses[0]:
            if not self.MouseUp:
                print("123")
                self.MouseUp = True
        if not mouses[0]:
            self.MouseUp = False'''