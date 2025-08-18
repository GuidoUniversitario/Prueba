import pygame
from nave import Nave
from fondo import Fondo

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")
nave = Nave()

fondo = Fondo(screen)

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fondo.mover()

    screen.fill((0, 0, 0))
    nave.mover(screen, dt)
    pygame.display.flip()

pygame.quit()
