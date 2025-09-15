import pygame
import random
from disparo_enemigo import Disparo_Enemigo

class Nave_Enemiga:
    def __init__(self, screen):
        self.screen = screen
        self.nave_enemiga_frames  = [
            pygame.transform.scale(pygame.image.load(f"img/flank_attacker_000{i}.png"), (50, 50))
            for i in range (1,4)
        ]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 100
        self.direccion = random.randint(0, 1)
        self.x = 480
        if self.direccion == 1:
            self.y = 480
            self.velocidad = -3
        else:
            self.y = 0
            self.velocidad = 3

        self.ultimo_disparo = pygame.time.get_ticks()
        self.intervalo_disparo = 1000

    def mover(self, screen, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.nave_enemiga_frames)
        self.y += self.velocidad
        screen.blit(self.nave_enemiga_frames[self.frame_index], (self.x, self.y))

        # Intentar disparar
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
            self.ultimo_disparo = tiempo_actual
            return Disparo_Enemigo(self.screen, self.x-50, self.y)

        return None

    def fuera_de_pantalla(self):
        if self.direccion == 1:
            return self.y < 0
        else:
            return self.y > 480