import pygame
import random


class Nave_Veloz(pygame.sprite.Sprite):
    def __init__(self, jugador, pantalla_ancho=640, pantalla_alto=480):
        super().__init__()

        # Imagen de la nave enemiga (puedes cambiar esto por una imagen real)
        self.image = pygame.Surface((40, 20))
        self.image.fill((255, 0, 0))  # Color rojo para identificarla
        self.rect = self.image.get_rect()

        # Posición inicial (fuera de la pantalla por la derecha)
        self.rect.x = pantalla_ancho + 10
        self.rect.y = random.randint(0, pantalla_alto - self.rect.height)

        # Velocidades
        self.vel_x = -2.0  # inicial
        self.max_vel_x = -10.0  # máxima hacia la izquierda
        self.aceleracion_x = -0.5  # cada frame

        self.vel_y = 0
        self.max_vel_y = 2.0  # velocidad vertical máxima
        self.jugador = jugador  # referencia a la nave del jugador

    def update(self):
        # Aceleración hacia la izquierda
        if self.vel_x > self.max_vel_x:
            self.vel_x += self.aceleracion_x

        # Movimiento horizontal
        self.rect.x += int(self.vel_x)

        # Seguimiento vertical (lento)
        if self.jugador.rect.centery < self.rect.centery:
            self.vel_y = max(self.vel_y - 0.1, -self.max_vel_y)
        elif self.jugador.rect.centery > self.rect.centery:
            self.vel_y = min(self.vel_y + 0.1, self.max_vel_y)
        else:
            self.vel_y *= 0.9  # desaceleración si ya está alineado

        # Movimiento vertical
        self.rect.y += int(self.vel_y)

        # Limitar al área de la pantalla
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        elif self.rect.bottom > 480:
            self.rect.bottom = 480
            self.vel_y = 0

        # Destruir si sale completamente de la pantalla por la izquierda
        if self.rect.right < 0:
            self.kill()