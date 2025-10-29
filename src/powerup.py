import pygame
import random

class PowerUp:
    def __init__(self, x, y):
        self.tipos = {
            "img/powerup1.png": "disparo_triple",
            "img/powerup2.png": "auto_disparo",
            "img/powerup3.png": "misil"
        }

        self.image_path = random.choice(list(self.tipos.keys()))
        self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (32, 32))
        self.tipo = self.tipos[self.image_path]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = -1

    def mover(self):
        self.rect.x += self.velocidad_x

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def fuera_de_pantalla(self):
        return self.rect.right < 0

    def get_rect(self):
        return self.rect