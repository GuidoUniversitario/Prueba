import pygame
import random

class Asteroide_Grande:
    def __init__(self):
        self.asteroide_img = pygame.transform.scale(pygame.image.load("img/medium_meteor.png").convert_alpha(), (50, 50))
        self.x = 640
        self.y = random.randint(0, 472)
        self.velocidad = random.randint(3, 6)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def mover(self, screen):
        self.x -= self.velocidad
        self.rect.x = self.x
        screen.blit(self.asteroide_img, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.x < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)