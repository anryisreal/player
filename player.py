import sys
import numpy
import pygame
import threading
from maps import *

pygame.init()
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
game_map = numpy.empty((screen.get_width() + 1, screen.get_height() + 1), dtype="object")
game_map[...] = "N"
clock = pygame.time.Clock()
objects = []
enemys = []
map = []


class Player:

    def __init__(self):
        self.width = 51
        self.height = 70
        self.image = pygame.image.load("models/player.png")
        self.x = int(WIDTH / 2)
        self.y = int(HEIGHT / 2)
        self.speed = 6
        self.space_x = 0
        self.space_y = 0
        self.stop_x = 0
        self.stop_y = 0
        self.firstshot = False

    def movement(self, signal):
        if signal == 0:
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

        if signal == 1:
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


        if signal == 2:
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

        if signal == 3:
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

class Enemy:

    def __init__(self, x, y, x_end, y_end):
        self.width = 70
        self.height = 70
        self.image = pygame.image.load("models/enemy.png")
        self.x = x
        self.y = y
        self.speed = 3
        self.x_end = x_end
        self.y_end = y_end
        self.glx = x
        self.gly = y
        self.revers = False

    def movement(self):
        if not self.revers:
            if self.x < self.x_end:
                self.x += self.speed * ((self.x_end - self.glx) / (self.y_end - self.gly))
            if self.x > self.x_end:
                self.x -= self.speed * ((self.x_end - self.glx) / (self.y_end - self.gly))
            if self.y < self.y_end:
                self.y += self.speed
            if self.y > self.y_end:
                self.y -= self.speed
            if self.x + self.speed * ((self.x_end - self.glx) / (self.y_end - self.gly)) > self.x_end:
                if self.y + self.speed > self.y_end:
                    self.x = self.x_end
                    self.y = self.y_end
                    self.revers = True
            if self.x == self.x_end and self.y == self.y_end:
                self.revers = True
        if self.revers:
            if self.x < self.glx:
                self.x += self.speed * ((self.x_end - self.glx) / (self.y_end - self.gly))
            if self.x > self.glx:
                self.x -= self.speed * ((self.x_end - self.glx) / (self.y_end - self.gly))
            if self.y < self.gly:
                self.y += self.speed
            if self.y > self.gly:
                self.y -= self.speed
            if self.x - self.speed * ((self.x_end - self.glx) / (self.y_end - self.gly)) < self.glx:
                if self.y - self.speed < self.gly:
                    self.x = self.glx
                    self.y = self.gly
                    self.revers = False
            if self.x == self.glx and self.y == self.gly:
                self.revers = False


'''class Shot:
    def __init__(self, x, y):
        self.image = pygame.image.load("models/shot.png")
        self.x = x + 30
        self.y = y - 10

    def shot(self):
        if self.y > 0:
            while self.y != 0:
                for enemy in enemys:
                    if enemy.x <= self.x <= (enemy.x + enemy.width):
                        if enemy.y <= self.y <= (enemy.y + enemy.height):               #Модельки пуль
                            del enemys[0]
                            del objects[1]
                            return
                clock.tick(30)
                self.y -= 10
        if self.y <= 0:
            del objects[1]'''


class Wall:
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.color = [185, 173, 173]
        self.image = pygame.transform.scale(pygame.image.load("models/brick.png"), (wall.get_width(), wall.get_height()))
        self.wall = wall

    def fill_blit(self):
        screen.blit(self.image, (self.x, self.y))



def init_map(str_map):
    height = str_map.count("\n")
    str_max = 0
    start_index = 0
    for i in range(height):
        if str_map.find("\n", start_index) - start_index > str_max:
            str_max = str_map.find("\n", start_index) - start_index
        start_index = str_map.find("\n", start_index) + 1
    x = screen.get_width()
    y = screen.get_height()
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
            map.append(wall)
        start_index += 1


def display_obj():
    screen.fill((0, 0, 0))
    for enemy in enemys:
        enemy.movement()
        screen.blit(enemy.image, (enemy.x, enemy.y))
    for map_object in map:
        map_object.fill_blit()
    for object in objects:
        screen.blit(object.image, (object.x, object.y))
    pygame.display.update()


def display():
    init_map(map_level0)
    fill_map(game_map, map, screen, player)
    while True:
        clock.tick(30)
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
        if keys[pygame.K_w]:
            threading.Thread(target=player.movement, args=(0,)).start()
        if keys[pygame.K_s]:
            threading.Thread(target=player.movement, args=(1,)).start()
        if keys[pygame.K_a]:
            threading.Thread(target=player.movement, args=(2,)).start()
        if keys[pygame.K_d]:
            threading.Thread(target=player.movement, args=(3,)).start()
        threading.Thread(target=display_obj).start()


player = Player()
objects.append(player)
'''enemy = Enemy(50, 60, 600, 400)  #Создание врага
enemys.append(enemy)'''

display()