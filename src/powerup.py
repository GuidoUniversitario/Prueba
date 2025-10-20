import pygame
import random

class PowerUp:
    def __init__(self, x, y):
        self.images = [
            pygame.image.load("img/powerup1.png").convert_alpha(),
            pygame.image.load("img/powerup2.png").convert_alpha(),
            pygame.image.load("img/powerup3.png").convert_alpha()
        ]
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = -1  # Flota lentamente hacia la izquierda

    def mover(self):
        self.rect.x += self.velocidad_x

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def fuera_de_pantalla(self):
        return self.rect.right < 0

    def get_rect(self):
        return self.rect