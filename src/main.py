import pygame
from src.nave import Nave
from src.disparo import Disparo
from src.fondo import Fondo
from src.asteroide import Asteroide
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")
nave = Nave()

fondo = Fondo(screen)
disparo = Disparo(screen)
asteroide = Asteroide()

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

    disparo.update()
    nave.mover(screen, dt)
    asteroide.mover(screen)
    pygame.display.flip()

pygame.quit()
