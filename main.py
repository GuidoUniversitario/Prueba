import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi primer juego")

spaceship_img = pygame.image.load("spaceship_0001.png")
spaceship_img = pygame.transform.scale(spaceship_img,(50,50))
spaceship_x = 50
spaceship_y = 200

lasers = []

laser_speed = 2

def shoot_laser(x, y):
    laser_rect = pygame.Rect(x + 50, y + 24, 10, 2)
    lasers.append(laser_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_laser(spaceship_x, spaceship_y)

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

    for laser in lasers:
        laser.x += laser_speed

    lasers = [laser for laser in lasers if laser.x < 640]

    screen.fill((0, 0, 0))
    screen.blit(spaceship_img, (spaceship_x, spaceship_y))

    for laser in lasers:
        pygame.draw.rect(screen, (255, 0, 0), laser)

    pygame.display.flip()

pygame.quit()
