import pygame
import math
from explosion import Explosion  # Importar la clase Explosion

class Misil:
    def __init__(self, x, y, objetivo):
        self.image = pygame.image.load("img/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 5

        self.objetivo = objetivo
        self.direccion = pygame.math.Vector2(1, 0)
        self.persiguiendo = True

        # Timer para autodestrucción
        self.tiempo_vida = 0          # En milisegundos
        self.tiempo_maximo = 2000     # 2 segundos

        self.explosion = None         # Se llenará al detonar

        if self.objetivo and hasattr(self.objetivo, "get_rect"):
            objetivo_pos = pygame.math.Vector2(self.objetivo.get_rect().center)
            misil_pos = pygame.math.Vector2(self.rect.center)
            diferencia = objetivo_pos - misil_pos
            if diferencia.length_squared() > 0:
                self.direccion = diferencia.normalize()

    def update(self, screen, dt):
        # Si ya explotó, actualizar su animación y salir
        if self.explosion:
            self.explosion.update(screen, dt)
            return

        # Actualizar temporizador de vida
        self.tiempo_vida += dt
        if self.tiempo_vida >= self.tiempo_maximo:
            # Autodetonar
            self.detonar()
            return

        # Perseguir al objetivo (si aún existe)
        if self.persiguiendo and self.objetivo:
            try:
                objetivo_pos = pygame.math.Vector2(self.objetivo.get_rect().center)
                misil_pos = pygame.math.Vector2(self.rect.center)
                diferencia = objetivo_pos - misil_pos

                if diferencia.length_squared() > 0:
                    self.direccion = diferencia.normalize()
                else:
                    self.persiguiendo = False
                    self.objetivo = None
            except Exception:
                self.persiguiendo = False
                self.objetivo = None

        # Mover el misil
        self.rect.x += int(self.direccion.x * self.velocidad)
        self.rect.y += int(self.direccion.y * self.velocidad)

        screen.blit(self.image, self.rect)

    def detonar(self):
        """Activa la explosión y marca el misil como destruido."""
        self.explosion = Explosion(self.rect.centerx - 25, self.rect.centery - 25)

    def fuera_de_pantalla(self):
        return (self.rect.right < 0 or self.rect.left > 640 or
                self.rect.bottom < 0 or self.rect.top > 480)

    def get_rect(self):
        return self.rect

    def ha_explotado(self):
        """Devuelve True si la explosión terminó y el misil puede eliminarse."""
        return self.explosion is not None and self.explosion.finished