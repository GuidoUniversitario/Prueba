import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
