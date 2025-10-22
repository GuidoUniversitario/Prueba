import pygame

class Disparo_Enemigo:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.laser_img = pygame.image.load("img/laser.png")
        self.laser_img = pygame.transform.scale(self.laser_img, (16, 16))
        self.x = x + 45
        self.y = y + 15
        self.rect = pygame.Rect(self.x, self.y, 25, 25)
        self.laser_speed = 5

    def update(self):
        self.x -= self.laser_speed
        self.rect.x = self.x  # <-- ¡Muy importante!
        self.rect.y = self.y  # Por si acaso (aunque Y no cambia, lo mantiene alineado)

    def draw(self):
        self.screen.blit(self.laser_img, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.x < 0

    def get_rect(self):
        return self.rect