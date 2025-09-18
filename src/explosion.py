import pygame

class Explosion:
    def __init__(self, x, y):
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"img/explosion_1_000{i}.png"), (50, 50)
            ) for i in range(1, 4)
        ]
        self.x = x
        self.y = y
        self.current_frame = 0
        self.timer = 0
        self.frame_duration = 150  # ms por cuadro
        self.finished = False

    def update(self, screen, dt):
        if self.finished:
            return

        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True
                return

        if not self.finished:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))