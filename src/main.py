import pygame
from nave import Nave
from disparo import Disparo
from fondo import Fondo
from asteroide import Asteroide
from nave_enemiga import Nave_Enemiga
from disparo_enemigo import Disparo_Enemigo
from nave_veloz import Nave_Veloz

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")
nave = Nave()

fondo = Fondo(screen)
disparo = Disparo(screen)
asteroide = Asteroide()
nave_enemiga = Nave_Enemiga(screen)
nave_veloz = Nave_Veloz(nave)
disparos_enemigos = []

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                disparo.shoot(nave.spaceship_x, nave.spaceship_y)

    fondo.mover()

    if asteroide.fuera_de_pantalla():
        asteroide = Asteroide()

    if nave_enemiga.fuera_de_pantalla():
        nave_enemiga = Nave_Enemiga(screen)

    for disparo_enemigo in disparos_enemigos[:]:
        disparo_enemigo.update()
        disparo_enemigo.draw()
        if disparo_enemigo.fuera_de_pantalla():
            disparos_enemigos.remove(disparo_enemigo)

    disparo.update()
    nave.mover(screen, dt)
    asteroide.mover(screen)
    disparo_enemigo_nuevo = nave_enemiga.mover(screen, dt)
    if disparo_enemigo_nuevo:
        disparos_enemigos.append(disparo_enemigo_nuevo)
    nave_veloz.update()
    screen.blit(nave_veloz.image, nave_veloz.rect)
    pygame.display.flip()

pygame.quit()
