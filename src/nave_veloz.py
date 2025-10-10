import pygame
import random

class Nave_Veloz(pygame.sprite.Sprite):
    def __init__(self, jugador, pantalla_ancho=640, pantalla_alto=480):
        super().__init__()

        self.nave_enemiga_frames = [
            pygame.transform.scale(pygame.image.load(f"img/speed_enemy_000{i}.png"), (50, 50))
            for i in range(1, 4)
        ]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 100  # milisegundos por frame

        self.image = self.nave_enemiga_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = pantalla_ancho + 10
        self.rect.y = random.randint(0, pantalla_alto - self.rect.height)

        self.vel_x = -2.0
        self.max_vel_x = -10.0
        self.aceleracion_x = -0.5

        self.vel_y = 0
        self.max_vel_y = 2.0

        self.jugador = jugador

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.nave_enemiga_frames)
            self.image = self.nave_enemiga_frames[self.frame_index]

        # Aceleración hacia la izquierda
        if self.vel_x > self.max_vel_x:
            self.vel_x += self.aceleracion_x

        self.rect.x += int(self.vel_x)

        # Seguimiento vertical
        jugador_rect = self.jugador.get_rect()

        if jugador_rect.centery < self.rect.centery:
            self.vel_y = max(self.vel_y - 0.1, -self.max_vel_y)
        elif jugador_rect.centery > self.rect.centery:
            self.vel_y = min(self.vel_y + 0.1, self.max_vel_y)
        else:
            self.vel_y *= 0.9

        self.rect.y += int(self.vel_y)

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        elif self.rect.bottom > 480:
            self.rect.bottom = 480
            self.vel_y = 0

    def get_rect(self):
        return self.rect

    def fuera_de_pantalla(self):
        return self.rect.right < 0