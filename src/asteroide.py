import pygame
import random

class Asteroide:
    def __init__(self):
        self.asteroide_img = pygame.transform.scale(pygame.image.load("img/little_meteor.png").convert_alpha(), (25, 25))
        self.x = 640
        self.y = random.randint(0, 472)
        self.velocidad = random.randint(3, 6)
        self.velocidad_y = 0  # ← Movimiento vertical por defecto (horizontal puro)
        self.rect = pygame.Rect(self.x, self.y, 25, 25)

    def mover(self, screen):
        self.x -= self.velocidad
        self.y += self.velocidad_y  # ← Agregamos el movimiento vertical
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.asteroide_img, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.x < 0 or self.y < 0 or self.y > 480  # si se sale por arriba o abajo también

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 25, 25)