import pygame
from disparo import Disparo
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")

spaceship_img = pygame.image.load("spaceship_0001.png")
spaceship_img = pygame.transform.scale(spaceship_img,(50,50))

disparo = Disparo(screen)

spaceship_x = 50
spaceship_y = 200

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                disparo.shoot(spaceship_x, spaceship_y)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_x -= 0.1
    if keys[pygame.K_RIGHT]:
        spaceship_x += 0.1
    if keys[pygame.K_UP]:
        spaceship_y -= 0.1
    if keys[pygame.K_DOWN]:
        spaceship_y += 0.1

    spaceship_x = max(0, min(spaceship_x, 640 - 50))
    spaceship_y = max(0, min(spaceship_y, 480 - 50))

    screen.fill((0, 0, 0))
    screen.blit(spaceship_img, (spaceship_x, spaceship_y))

    disparo.update()
    pygame.display.flip()

pygame.quit()
