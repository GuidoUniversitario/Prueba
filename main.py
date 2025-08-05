import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")

spaceship_img = pygame.image.load("spaceship_0001.png")
spaceship_img = pygame.transform.scale(spaceship_img,(50,50))
spaceship_x = 50
spaceship_y = 200

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(spaceship_img, (spaceship_x, spaceship_y))
    pygame.display.flip()

pygame.quit()
