import pygame
import math

class Misil:
    def __init__(self, x, y, objetivo):
        self.image = pygame.image.load("img/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 5

        self.objetivo = objetivo
        self.direccion = pygame.math.Vector2(1, 0)  # Dirección por defecto: derecha
        self.persiguiendo = True  # Mientras sea True, el misil recalcula dirección

        # Si el objetivo es válido al inicio, calcula dirección hacia él
        if self.objetivo and hasattr(self.objetivo, "get_rect"):
            objetivo_pos = pygame.math.Vector2(self.objetivo.get_rect().center)
            misil_pos = pygame.math.Vector2(self.rect.center)
            diferencia = objetivo_pos - misil_pos
            if diferencia.length_squared() > 0:
                self.direccion = diferencia.normalize()

    def update(self, screen):
        if self.persiguiendo and self.objetivo:
            try:
                objetivo_pos = pygame.math.Vector2(self.objetivo.get_rect().center)
                misil_pos = pygame.math.Vector2(self.rect.center)
                diferencia = objetivo_pos - misil_pos

                if diferencia.length_squared() > 0:
                    self.direccion = diferencia.normalize()
                else:
                    # Si está muy cerca del objetivo, se desactiva el seguimiento
                    self.persiguiendo = False
                    self.objetivo = None
            except Exception:
                # Si ocurre un error (objetivo eliminado), detener seguimiento
                self.persiguiendo = False
                self.objetivo = None

        # Mover el misil en su dirección actual
        self.rect.x += int(self.direccion.x * self.velocidad)
        self.rect.y += int(self.direccion.y * self.velocidad)

        screen.blit(self.image, self.rect)

    def fuera_de_pantalla(self):
        return (self.rect.right < 0 or self.rect.left > 640 or
                self.rect.bottom < 0 or self.rect.top > 480)

    def get_rect(self):
        return self.rect