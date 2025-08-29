import pygame

class Disparo:
    def __init__(self, screen):
        self.screen = screen
        self.laser_img = pygame.image.load("img/laser.png")
        self.laser_img = pygame.transform.scale(self.laser_img, (25, 25))
        self.lasers = []
        self.laser_speed = 1

    def shoot(self, x, y):
        laser_x = x + 45
        laser_y = y + 15
        self.lasers.append({"x": laser_x, "y": laser_y})

    def update(self):
        for laser in self.lasers:
            laser["x"] += self.laser_speed

        self.lasers = [laser for laser in self.lasers if laser["x"] < 640]

        for laser in self.lasers:
            self.screen.blit(self.laser_img, (laser["x"], laser["y"]))