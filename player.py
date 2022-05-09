import sys
import pygame
import threading

pygame.init()
WIDTH, HEIGHT = 980, 980
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
objects = []
enemys = []
firstshot = False


class Player:

    def __init__(self):
        self.width = 70
        self.height = 70
        self.color = [209, 41, 41, 0]
        self.image = pygame.image.load("models/player.png")
        self.x = 0
        self.y = 0
        self.speed = 10
        self.is_player = True

    def movement(self, signal):
        if signal == 0:
            if self.y - self.speed < 0:
                pass
            else:
                self.y -= self.speed
        if signal == 1:
            if self.y + self.speed > HEIGHT - self.height:
                pass
            else:
                self.y += self.speed
        if signal == 2:
            if self.x - self.speed < 0:
                pass
            else:
                self.x -= self.speed
        if signal == 3:
            if self.x + self.speed > WIDTH - self.width:
                pass
            else:
                self.x += self.speed


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


def display_obj():
    screen.fill((0, 0, 0))
    for object in objects:
        screen.blit(object.image, (object.x, object.y))
    for enemy in enemys:
        screen.blit(enemy.image, (enemy.x, enemy.y))


def display():
    global firstshot
    screen.fill((0, 0, 0))
    screen.blit(player.image, (player.x, player.y))
    objects.append(player)
    while True:
        screen.blit(player.image, (player.x, player.y))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
enemy = Player()
enemy.is_player = False
enemy.x = 50
enemy.y = 60
enemy.image = pygame.image.load("models/enemy.png")
enemys.append(enemy)
display()
