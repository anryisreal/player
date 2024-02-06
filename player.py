import pygame

class Player:

    def __init__(self, data):
        self.width = 51
        self.height = 70
        self.image = pygame.image.load("models/Player/Player_W.png")
        self.x = int(data["WIDTH"] / 2)
        self.y = int(data["HEIGHT"] / 2)
        self.speed = 6
        self.space_x = 0
        self.space_y = 0
        self.stop_x = 0
        self.stop_y = 0
        self.MouseUp = False
        self.obj = None

    def movement(self, keys, game_map, data):
        if keys[pygame.K_w]:
            self.image = pygame.image.load("models/Player/Player_W.png")
            for i in range(self.speed):
                if self.y == 0:
                    return
                else:
                    for i in range(self.x, self.x + self.width):
                        if game_map[i][self.y - 1] == "W":
                            return
                    for i in range(self.x, self.x + self.width):
                        if game_map[i][self.y - 1] == "N":
                            game_map[i][self.y - 1] = "P"
                            game_map[i][self.y + self.height] = "N"
                        else:
                            self.obj = game_map[i][self.y - 1]
                    self.y -= 1

        if keys[pygame.K_s]:
            self.image = pygame.image.load("models/Player/Player_S.png")
            for i in range(self.speed):
                if self.y + self.height == data["HEIGHT"]:
                    return
                else:
                    for i in range(self.x, self.x + self.width):
                        if game_map[i][self.y + self.height + 1] == "W":
                            return
                    for i in range(self.x, self.x + self.width):
                        game_map[i][self.y + self.height + 1] = "P"
                        game_map[i][self.y] = "N"
                    self.y += 1

        if keys[pygame.K_a]:
            self.image = pygame.image.load("models/Player/Player_A.png")
            for i in range(self.speed):
                if self.x == 0:
                    return
                else:
                    for i in range(self.y, self.y + self.height):
                        if game_map[self.x - 1][i] == "W":
                            return
                    for i in range(self.y, self.y + self.height):
                        game_map[self.x - 1][i] = "P"
                        game_map[self.x + self.width][i] = "N"
                    self.x -= 1

        if keys[pygame.K_d]:
            self.image = pygame.image.load("models/Player/Player_D.png")
            for i in range(self.speed):
                if self.x + self.width == data["WIDTH"]:
                    return
                else:
                    for i in range(self.y, self.y + self.height):
                        if game_map[self.x + self.width + 1][i] == "W":
                            return
                    for i in range(self.y, self.y + self.height):
                        game_map[self.x + self.width + 1][i] = "P"
                        game_map[self.x][i] = "N"
                    self.x += 1