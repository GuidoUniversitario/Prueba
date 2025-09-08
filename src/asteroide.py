import pygame
import random

class Asteroide:
    def __init__(self):
        self.asteroide_img = pygame.transform.scale(pygame.image.load("img/little_meteor.png").convert_alpha(), (25, 25))
        self.x = 640
        self.y = random.randint(0, 472)
        self.velocidad = random.randint(3, 6)

    def mover(self, screen):
        self.x -= self.velocidad
        screen.blit(self.asteroide_img, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.x < 0
