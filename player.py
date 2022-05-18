import sys
import pygame
import threading
from maps import *

pygame.init()
WIDTH, HEIGHT = 980, 980
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
objects = []
enemys = []
map = []
firstshot = False


class Player:

    def __init__(self):
        self.width = 70
        self.height = 70
        self.image = pygame.image.load("models/player.png")
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 6
        self.space_x = 0
        self.space_y = 0
        self.stop_x = 0
        self.stop_y = 0

    def movement(self, signal):
        self.space_x, self.space_y, self.stop_x, self.stop_y = 0, 0, 0, 0
        if signal == 0:
            for map_object in map:
                if map_object.y + map_object.wall.get_height() <= self.y:
                    if map_object.y + map_object.wall.get_height() > self.stop_y:
                        self.stop_y = map_object.y + map_object.wall.get_height()
                    if map_object.x <= self.x <= map_object.x + map_object.wall.get_width():
                        self.space_x += map_object.wall.get_width()
            if self.space_x >= self.width:
                if self.y > self.stop_y:
                    self.y -= self.speed
            else:
                if self.y - self.speed < 0:
                    pass
                else:
                    self.y -= self.speed



                '''for map_object in map:
                    if self.y - self.speed >= map_object.y + map_object.wall.get_height():
                        if self.y - self.speed < 0:
                            pass
                        else:
                            self.y -= self.speed
                    if self.y - self.speed < map_object.y + map_object.wall.get_height() and self.y > map_object.y + map_object.wall.get_height():
                        self.y = map_object.y + map_object.wall.get_height()'''



        if signal == 1:
            for map_object in map:
                if map_object.y >= self.y + self.height:
                    if map_object.y > self.stop_y:
                        self.stop_y = map_object.y - self.height
                    if map_object.x <= self.x <= map_object.x + map_object.wall.get_width():
                        self.space_x += map_object.wall.get_width()
            if self.space_x >= self.width:
                if self.y < self.stop_y:
                    if self.y + self.speed > self.stop_y:
                        self.y = self.stop_y
                    if self.y + self.speed <= self.stop_y:
                        self.y += self.speed
                        print(self.y, self.space_x, self.width, self.stop_y)
            else:
                if self.y + self.speed > HEIGHT - self.height:
                    pass
                else:
                    self.y += self.speed

                '''if self.y + self.speed <= map_object.y - self.height:
                    if self.y + self.speed > HEIGHT - self.height:
                        pass
                    else:
                        self.y += self.speed
                if self.y + self.speed > map_object.y - self.height and self.y < map_object.y - self.height:
                    self.y = map_object.y - self.heigh'''


        if signal == 2:
            for map_object in map:
                if self.x - self.speed >= map_object.x + map_object.wall.get_width():
                    if self.x - self.speed < 0:
                        pass
                    else:
                        self.x -= self.speed
                if self.x - self.speed < map_object.x + map_object.wall.get_width() and self.x > map_object.x + map_object.wall.get_width():
                    self.x = map_object.x + map_object.wall.get_width()
        if signal == 3:
            for map_object in map:
                if self.x + self.speed <= map_object.x - self.width:
                    if self.x + self.speed > WIDTH - self.width:
                        pass
                    else:
                        self.x += self.speed
                if self.x + self.speed > map_object.x - self.width and self.x < map_object.x - self.width:
                    self.x = map_object.x - self.width

    def check_wall(self):
        pass

'''    def check_w(x, y, space_x, space_y):
    for map_object in map:
        if map_object.y + map_object.wall.get_height() >= self.y:
            if map_object.x <= self.x <= map_object.x + map_object.wall.get_width():
                self.space_x += (map_object.wall.get_width() - map_object.x)
    if self.space_x >= self.width:
        return 0
    return -1
    def check_s(x, y, space_x, space_y):
    for map_object in map:
        if map_object.y <= self.y + self.height:
            if map_object.x <= self.x <= map_object.x + map_object.wall.get_width():
                self.space_x += (map_object.wall.get_width() - map_object.x)
    if self.space_x >= self.width:
        return 0
    return -1
    def check_a(x, y, space_x, space_y):
    for map_object in map:
        if map_object.x + map_object.wall.width() <= self.x:
            if map_object.y <= self.y <= map_object.y + map_object.wall.get_height():
                self.space_y += (map_object.wall.height() - map_object.y)
    if self.space_y >= self.height:
        return 0
    return -1
    def check_d(x, y, space_x, space_y, height, width):
    for map_object in map:
        if map_object.x >= x + width:
            if map_object.y <= y <= map_object.y + map_object.wall.get_height():
                .space_y += (map_object.wall.height() - map_object.y)
    if space_y >= height:
        return 0
    return -1'''

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


class Shot:
    def __init__(self, x, y):
        self.image = pygame.image.load("models/shot.png")
        self.x = x + 30
        self.y = y - 10

    def shot(self):
        if self.y > 0:
            while self.y != 0:
                for enemy in enemys:
                    if enemy.x <= self.x <= (enemy.x + enemy.width):
                        if enemy.y <= self.y <= (enemy.y + enemy.height):
                            del enemys[0]
                            del objects[1]
                            return
                clock.tick(30)
                self.y -= 10
        if self.y <= 0:
            del objects[1]


class Wall:
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.color = [185, 173, 173]
        self.wall = wall

    def fill_blit(self):
        self.wall.fill([185, 173, 173])
        screen.blit(self.wall, (self.x, self.y))



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
    for object in objects:
        screen.blit(object.image, (object.x, object.y))
    for enemy in enemys:
        enemy.movement()
        screen.blit(enemy.image, (enemy.x, enemy.y))
    for map_object in map:
        map_object.fill_blit()


def display():
    global firstshot
    screen.fill((0, 0, 0))
    screen.blit(player.image, (player.x, player.y))
    objects.append(player)
    init_map(map_level0)
    while True:
        screen.blit(player.image, (player.x, player.y))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and firstshot == False:
                if event.key == pygame.K_SPACE:
                    shot = Shot(player.x, player.y)
                    objects.append(shot)
                    threading.Thread(target=shot.shot).start()
                    firstshot = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    firstshot = False
                    continue

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
        pygame.display.update()


player = Player()
enemy = Enemy(50, 60, 600, 400)
enemys.append(enemy)
display()
