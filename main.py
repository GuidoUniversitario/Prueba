import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")

spaceship_frames = [
    pygame.transform.scale(pygame.image.load(f"spaceship_000{i}.png"), (50, 50))
    for i in range(1, 4)
]
laser_img = pygame.image.load("laser.png")
laser_img = pygame.transform.scale(laser_img, (25, 25))

spaceship_x = 50
spaceship_y = 200

lasers = []

laser_speed = 10

def shoot_laser(x, y):
    laser_rect = pygame.Rect(x + 25, y + 12, 10, 2)
    lasers.append(laser_rect)

frame_index = 0
animation_timer = 0
animation_speed = 100

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_laser(spaceship_x, spaceship_y)

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

    for laser in lasers:
        laser.x += laser_speed

    lasers = [laser for laser in lasers if laser.x < 640]

    animation_timer += dt
    if animation_timer >= animation_speed:
        animation_timer = 0
        frame_index = (frame_index + 1) % len(spaceship_frames)

    screen.fill((0, 0, 0))

    for laser in lasers:
        screen.blit(laser_img, (laser.x, laser.y))

    screen.blit(spaceship_frames[frame_index], (spaceship_x, spaceship_y))
    pygame.display.flip()

pygame.quit()
