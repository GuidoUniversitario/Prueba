import pygame

class Nave:
    def __init__(self):
        self.spaceship_frames = [
            pygame.transform.scale(pygame.image.load(f"img/spaceship_000{i}.png"), (50, 50))
            for i in range(1, 4)
        ]
        self.spaceship_x = 50
        self.spaceship_y = 200

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 100

    # En el main loop
    def mover(self, screen, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.spaceship_x -= 0.2 * dt
        if keys[pygame.K_RIGHT]:
            self.spaceship_x += 0.2 * dt
        if keys[pygame.K_UP]:
            self.spaceship_y -= 0.2 * dt
        if keys[pygame.K_DOWN]:
            self.spaceship_y += 0.2 * dt

        self.spaceship_x = max(0, min(self.spaceship_x, 640 - 50))
        self.spaceship_y = max(0, min(self.spaceship_y, 480 - 50))

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.spaceship_frames)

        screen.blit(self.spaceship_frames[self.frame_index], (self.spaceship_x, self.spaceship_y))
