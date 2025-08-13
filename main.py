import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")

spaceship_img = pygame.image.load("spaceship_0001.png")
spaceship_img = pygame.transform.scale(spaceship_img,(50,50))
spaceship_x = 50
spaceship_y = 200

tile_size = 64
bg_tile = pygame.image.load("stars_big.png").convert()
offset_x = 0
scroll_speed = 0.1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    offset_x -= scroll_speed
    if offset_x <= -tile_size:
        offset_x = 0

    screen.fill((0, 0, 0))
    for y in range(0, 480, tile_size):
        for x in range(0, 640 + tile_size, tile_size):
            screen.blit(bg_tile, (x + offset_x, y))
    screen.blit(spaceship_img, (spaceship_x, spaceship_y))
    pygame.display.flip()

pygame.quit()
