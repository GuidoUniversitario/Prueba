import pygame

class Puntaje:
    def __init__(self, screen):
        self.screen = screen
        # Cargar imágenes de los números
        self.numero_imgs = [
            pygame.image.load(f"img/future_numbers_000{i}.png") for i in range(10)
        ]
        self.numero_imgs = [pygame.transform.scale(img, (15, 20)) for img in self.numero_imgs]
        self.puntos = 0

    def sumar(self, cantidad):
        self.puntos += cantidad

    def reset(self):
        self.puntos = 0

    def mostrar(self):
        # Convertir el puntaje a string para mostrar cada dígito
        puntos_str = str(self.puntos)
        x = 10
        y = 40  # un poco más abajo que las vidas
        for digito in puntos_str:
            img = self.numero_imgs[int(digito)]
            self.screen.blit(img, (x, y))
            x += 20  # espacio entre dígitos