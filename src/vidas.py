import pygame

class Vidas:
    def __init__(self, cantidad, screen):
        self.vidas = cantidad
        self.screen = screen
        self.numero_imgs = [
            pygame.image.load(f"img/future_numbers_000{i}.png") for i in range(10)
        ]
        self.numero_imgs = [pygame.transform.scale(img, (15, 20)) for img in self.numero_imgs]

    def restar(self):
        if self.vidas > 0:
            self.vidas -= 1

    def reset(self, cantidad):
        self.vidas = cantidad

    def mostrar(self):
        # Mostrar número en la esquina superior izquierda
        if self.vidas >= 0 and self.vidas < 10:
            img = self.numero_imgs[self.vidas]
            self.screen.blit(img, (10, 10))

    def esta_sin_vidas(self):
        return self.vidas <= 0