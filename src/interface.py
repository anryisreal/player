import pygame
import authentification as auth

class DataForWindow:

    def __init__(self, image: str, x: int, y: int, x_line: int, y_line: int, is_on: bool):
        self.x = x
        self.y = y
        self.x_line = x_line
        self.y_line = y_line
        self.image = pygame.transform.scale(pygame.image.load(image), (x_line, y_line))
        self.is_on = is_on


class Window:

    def __init__(self, image: str, x: int, y: int, x_line: int, y_line: int, is_on: bool):
        self.Property = DataForWindow(image, x, y, x_line, y_line, is_on)

    def fill_blit(self, screen):
        screen.blit(self.Property.image, (self.Property.x, self.Property.y))
class DataForButton:

    def __init__(self, x, y, width, height, color, is_on, fill, text, text_x, text_y):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_on = is_on
        self.fill = fill # 0 - all surface; any INT - surface border
        self.text = text
        self.text_x = text_x
        self.text_y = text_y
        self.TextSize = 36
        self.TextColor = pygame.Color('black')
        self.TextSurface = pygame.font.Font(None, self.TextSize).render(self.text, True, self.TextColor)
        self.active = False

class Button:

    def __init__(self, x, y, width, height, color=pygame.Color('White'), is_on=True, fill=0, text="", text_x=0, text_y=0):
        super().__init__()
        self.Property = DataForButton(x, y, width, height, color, is_on, fill, text, text_x, text_y)

    def fill_blit(self, screen):
        pygame.draw.rect(screen, self.Property.color, self.Property.rect, self.Property.fill)
        TextRect = self.Property.TextSurface.get_rect()
        TextRect.center = (self.Property.rect.x + self.Property.rect.width / 2, self.Property.rect.y + self.Property.rect.height / 2)
        screen.blit(self.Property.TextSurface, TextRect)



class LoginButton(Button):

    def __init__(self, x, y, width, height, LoginBox, PasswordBox, color=pygame.Color('lightskyblue3'), is_on=True, fill=0, text_x=0, text_y=0):
        super().__init__(x, y, width, height, color, is_on, fill, "Login", text_x, text_y)

        #Data:
        self.LoginBox = LoginBox
        self.PasswordBox = PasswordBox

    def interaction(self, event, player):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Property.rect.collidepoint(event.pos):
                    self.Property.active = True
                    self.Property.color = pygame.Color(0, 255, 14)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.Property.rect.collidepoint(event.pos):
                    conn = auth.connection()
                    if conn != -1 and self.DataCheck():
                        login = auth.login(conn, self.LoginBox.Property.text, self.PasswordBox.Property.text)
                        if login:
                            player.login = login
                self.Property.active = False
                self.Property.color = pygame.Color('lightskyblue3')
            else:
                self.Property.color = pygame.Color('lightskyblue3')

    def DataCheck(self):
        if len(self.LoginBox.Property.text) < 1:
            print("No Login")
            return 0
        if len(self.PasswordBox.Property.text) < 1:
            print("No Password")
            return 0

        return 1

# ChangeInterfaceButton
class CIButton(Button):

    def __init__(self, x, y, width, height, text, INTERFACE, Itype, color=pygame.Color('lightskyblue3'), is_on=True, fill=0):
        super().__init__(x, y, width, height, color, is_on, fill, text)
        self.I = INTERFACE
        self.Itype = Itype

    def interaction(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Property.rect.collidepoint(event.pos):
                    self.Property.active = True
                    self.Property.color = pygame.Color(0, 255, 14)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.Property.rect.collidepoint(event.pos):
                    self.I.type = self.Itype
                    return self.Itype
                self.Property.active = False
                self.Property.color = pygame.Color('lightskyblue3')
            else:
                self.Property.color = pygame.Color('lightskyblue3')

class DataForIB:

    def __init__(self, x, y, width, height, text='', is_on=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 28).render(text, True, self.color)
        self.active = False
        self.is_on = is_on
class InputBox:

    def __init__(self, x, y, width, height, text='', is_on=True):
        self.Property = DataForIB(x, y, width, height, text, is_on)

    def interaction(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.Property.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.Property.active = not self.Property.active
            else:
                self.Property.active = False
            # Change the current color of the input box.
            self.Property.color = pygame.Color('dodgerblue2') if self.Property.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.Property.active:
                if event.key == pygame.K_BACKSPACE:
                    self.Property.text = self.Property.text[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_SPACE:
                    if len(self.Property.text) < 24:
                        self.Property.text += event.unicode
                # Re-render the text.
                self.Property.txt_surface = (pygame.font.Font(None, 28)).render(self.Property.text, True, self.Property.color)


    def fill_blit(self, screen):
        # Blit the text.
        screen.blit(self.Property.txt_surface, (self.Property.rect.x+5, self.Property.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.Property.color, self.Property.rect, 2)

class Interface:

    def __init__(self, FULL_HEIGHT: int, FULL_WIDTH: int, HEIGHT: int, WIDTH: int, ABS_X: int, ABS_Y: int):
        self.Windows = []
        self.Active = []
        self.type = 0
        self.FULL_HEIGHT = FULL_HEIGHT
        self.FULL_WIDTH = FULL_WIDTH
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.ABS_X = ABS_X
        self.ABS_Y = ABS_Y

    def fill_interface(self) -> None:

        # Отрисовка меню авторизации
        if self.type == 0:
            LoginBox = InputBox(self.WIDTH * 0.19, self.HEIGHT * 0.26, self.WIDTH * 0.17, self.HEIGHT * 0.033)
            PasswordBox = InputBox(self.WIDTH * 0.19, self.HEIGHT * 0.39, self.WIDTH * 0.17, self.HEIGHT * 0.033)
            LButton = LoginButton(self.WIDTH * 0.24, self.HEIGHT * 0.465, self.WIDTH * 0.07, self.HEIGHT * 0.05, LoginBox, PasswordBox, text_x=self.WIDTH * 0.07 / 2)
            ActiveAuthMenu = [
                LoginBox,
                PasswordBox,
                LButton
            ]
            AuthenticationMenu = [
                Window("../models/Authentification/MenuFrame.png", 0, 0, self.FULL_WIDTH, self.FULL_HEIGHT, True),
                ActiveAuthMenu[0],
                ActiveAuthMenu[1],
                ActiveAuthMenu[2]
            ]
            self.Windows = AuthenticationMenu
            self.Active = ActiveAuthMenu
        if self.type == 1:
            PlayButton = CIButton(self.WIDTH * 0.155, self.HEIGHT * 0.27, self.WIDTH * 0.16, self.HEIGHT * 0.045, "Play", self, 3)
            BuilderButton = CIButton(self.WIDTH * 0.155, self.HEIGHT * 0.44, self.WIDTH * 0.16, self.HEIGHT * 0.045, "Build Mode", self, 2)
            ActiveSelectInterface = [
                PlayButton,
                BuilderButton
            ]
            SelectInterface = [
                Window("../models/SelectMode/MenuFrame.png", 0, 0, self.FULL_WIDTH, self.FULL_HEIGHT, True),
                ActiveSelectInterface[0],
                ActiveSelectInterface[1]
            ]
            self.Windows = SelectInterface
            self.Active = ActiveSelectInterface
        if self.type == 2:
            pass
        if self.type == 3:
            GeneralInterface = [
            Window("../models/menu/menu.png", 0, 0, self.ABS_X, self.FULL_HEIGHT, True), #Border_Left
            Window("../models/menu/menu.png", 0, 0, self.FULL_WIDTH, self.ABS_Y, True), #Border_Top
            Window("../models/menu/menu.png", self.FULL_WIDTH - self.ABS_X, 0, self.ABS_X, self.FULL_HEIGHT - self.ABS_Y, True), #Border_Right
            Window("../models/menu/inventory.png", self.FULL_WIDTH - 200, self.FULL_HEIGHT - self.ABS_Y, 200, self.FULL_HEIGHT - self.HEIGHT - self.ABS_Y, True), #Inventory
            Window("../models/menu/menu.png", 0, self.FULL_HEIGHT - self.ABS_Y, self.FULL_WIDTH - 200, self.FULL_HEIGHT - self.HEIGHT - self.ABS_Y, True), #Fill_Menu
            Window("../models/menu/menu_rgb.png", 400, 400, 300, 300, False), #interface_menu
            Window("../models/menu/tp_menu.png", int(self.FULL_WIDTH * 0.42), int(self.HEIGHT * 0.8), int(self.WIDTH * 0.19), int(self.HEIGHT * 0.08), True) #tp_menu
            ]
            self.Windows = GeneralInterface
            self.Active = []




