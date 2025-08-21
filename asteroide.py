import pygame
import random

ASTEROIDE_IMG = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(ASTEROIDE_IMG, (150, 150, 150), (25, 25), 25) #temporal

class Asteroide:
    def __init__(self):
        self.image = ASTEROIDE_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 640
        self.rect.y = random.randint(0, 480 - self.rect.height)
        self.velocidad = random.randint(3, 6)

    def mover(self):
        self.rect.x -= self.velocidad

    def fuera_de_pantalla(self):
        return self.rect.right < 0

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
