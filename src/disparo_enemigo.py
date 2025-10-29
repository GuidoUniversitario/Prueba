import pygame

class Disparo_Enemigo:
    def __init__(self, screen, x, y, velocidad_x=-5, velocidad_y=0):
        self.screen = screen
        self.laser_img = pygame.image.load("img/laser.png")
        self.laser_img = pygame.transform.scale(self.laser_img, (16, 16))
        self.x = x + 45
        self.y = y + 15
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.rect = pygame.Rect(self.x, self.y, 25, 25)

    def update(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.laser_img, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.x < 0 or self.y < 0 or self.y > 600

    def get_rect(self):
        return self.rect