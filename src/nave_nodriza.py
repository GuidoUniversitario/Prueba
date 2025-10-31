import pygame
import math
from disparo_enemigo import Disparo_Enemigo
from explosion import Explosion

class Nave_Nodriza(pygame.sprite.Sprite):
    def __init__(self, screen, disparos_enemigos, disparos_jugador):
        self.screen = screen
        self.imagen = pygame.transform.scale(pygame.image.load(f"img/mothership.png"), (150, 150))
        self.rect = self.imagen.get_rect(midright=(700, 240))  # Entrando desde la derecha
        self.velocidad_movimiento = 2
        self.direccion_movimiento = 1  # 1 para abajo, -1 para arriba
        self.limite_superior = 50
        self.limite_inferior = 430
        self.estado = "entrando"  # o "activo"
        self.vida = 20
        self.esta_destruida = False
        self.disparos_enemigos = disparos_enemigos
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.tiempo_entre_disparos = 1000  # milisegundos, por ejemplo 1 segundo entre disparos
        self.disparos_jugador = disparos_jugador

    def update(self):
        if self.estado == "entrando":
            self.rect.x -= 1
            if self.rect.x <= 500:
                self.estado = "activo"
        elif self.estado == "activo":
            self.mover_vertical()
            self.disparar()

    def draw(self):
        self.screen.blit(self.imagen, self.rect)

    def entrada(self):
        if self.invulnerable:
            if self.rect.x > self.posicion_objetivo_x:
                self.rect.x -= self.velocidad_entrada
            else:
                self.invulnerable = False  # Ya puede recibir daño

    def mover_vertical(self):
        self.rect.y += self.direccion_movimiento * self.velocidad_movimiento
        if self.rect.top <= self.limite_superior or self.rect.bottom >= self.limite_inferior:
            self.direccion_movimiento *= -1

    def disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_disparo > self.tiempo_entre_disparos:
            self.disparo_abanico()
            self.tiempo_ultimo_disparo = ahora

    def disparo_abanico(self):
        origen_x = self.rect.left
        origen_y = self.rect.centery
        angulos = [-30, -15, 0, 15, 30]
        velocidad = 6
        for angulo in angulos:
            radianes = math.radians(angulo)
            vx = -velocidad * math.cos(radianes)  # Hacia la izquierda
            vy = velocidad * math.sin(radianes)
            disparo = Disparo_Enemigo(self.screen, origen_x, origen_y, vx, vy)
            self.disparos_enemigos.append(disparo)

    def detectar_colisiones(self):
        impactos = pygame.sprite.spritecollide(self, self.disparos_jugador, True)
        if impactos:
            self.vida -= len(impactos)
            if self.vida <= 0:
                self.kill()
                # Aquí puedes agregar explosión, sonido, puntuación, etc.

    def recibir_dano(self):
        if self.estado == "activo":
            self.vida -= 1
            if self.vida <= 0:
                self.esta_destruida = True

    def get_rect(self):
        return self.rect