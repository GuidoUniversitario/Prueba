import pygame

class Fondo:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 64
        self.bg_tile = pygame.image.load("stars_big.png").convert()
        self.offset_x = 0
        self.scroll_speed = 1

    def mover(self):
        self.screen.fill((0, 0, 0))
        self.offset_x -= self.scroll_speed
        if self.offset_x <= -self.tile_size:
            self.offset_x = 0

        for y in range(0, 480, self.tile_size):
            for x in range(0, 640 + self.tile_size, self.tile_size):
                self.screen.blit(self.bg_tile, (x + self.offset_x, y))
