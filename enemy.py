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