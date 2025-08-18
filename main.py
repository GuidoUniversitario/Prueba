import pygame
from nave import Nave
from disparo import Disparo
from fondo import Fondo

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")
nave = Nave()

fondo = Fondo(screen)
disparo = Disparo(screen)

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                disparo.shoot(spaceship_x, spaceship_y)

    fondo.mover()

    screen.fill((0, 0, 0))

    disparo.update()
    nave.mover(screen, dt)
    pygame.display.flip()

pygame.quit()
