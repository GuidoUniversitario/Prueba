import pygame
from asteroide import Asteroide
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")

spaceship_frames = [
    pygame.transform.scale(pygame.image.load(f"spaceship_000{i}.png"), (50, 50))
    for i in range(1, 4)
]
spaceship_x = 50
spaceship_y = 200

frame_index = 0
animation_timer = 0
animation_speed = 100

asteroide = Asteroide()

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_x -= 0.2 * dt
    if keys[pygame.K_RIGHT]:
        spaceship_x += 0.2 * dt
    if keys[pygame.K_UP]:
        spaceship_y -= 0.2 * dt
    if keys[pygame.K_DOWN]:
        spaceship_y += 0.2 * dt

    spaceship_x = max(0, min(spaceship_x, 640 - 50))
    spaceship_y = max(0, min(spaceship_y, 480 - 50))

    animation_timer += dt
    if animation_timer >= animation_speed:
        animation_timer = 0
        frame_index = (frame_index + 1) % len(spaceship_frames)

    asteroide.mover()
    if asteroide.fuera_de_pantalla():
        asteroide = Asteroide()

    screen.fill((0, 0, 0))
    asteroide.dibujar(screen)
    screen.blit(spaceship_frames[frame_index], (spaceship_x, spaceship_y))
    pygame.display.flip()

pygame.quit()
