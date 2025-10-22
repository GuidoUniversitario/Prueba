import pygame
from misil import Misil  # Asegúrate de tener esta clase lista

class Disparo:
    def __init__(self, screen):
        self.screen = screen
        self.laser_img = pygame.image.load("img/laser.png")
        self.laser_img = pygame.transform.scale(self.laser_img, (16, 16))
        self.lasers = []
        self.laser_speed = 20
        self.misiles = []
        self.auto_timer = 0  # Tiempo del último disparo automático
        self.auto_cooldown = 100  # En milisegundos (0.1 segundos)

    def shoot(self, x, y):
        laser_x = x + 45
        laser_y = y + 15
        rect = pygame.Rect(laser_x, laser_y, 25, 25)
        self.lasers.append({
            "x": laser_x,
            "y": laser_y,
            "dx": self.laser_speed,
            "dy": 0,
            "rect": rect,
            "image": self.laser_img
        })

    def shoot_triple(self, x, y):
        origin_x = x + 45
        origin_y = y + 15
        for dx, dy in [(self.laser_speed, -5), (self.laser_speed, 0), (self.laser_speed, 5)]:
            rect = pygame.Rect(origin_x, origin_y, 25, 25)
            self.lasers.append({
                "x": origin_x,
                "y": origin_y,
                "dx": dx,
                "dy": dy,
                "rect": rect,
                "image": self.laser_img
            })

    def shoot_misil(self, x, y, enemigos):
        if enemigos:
            objetivo = min(enemigos, key=lambda e: ((e.get_rect().centerx - x) ** 2 + (e.get_rect().centery - y) ** 2))
            self.misiles.append(Misil(x, y, objetivo))

    def update(self):
        for laser in self.lasers[:]:
            laser["x"] += laser["dx"]
            laser["y"] += laser["dy"]
            laser["rect"].x = int(laser["x"])
            laser["rect"].y = int(laser["y"])

            # Dibujar el láser
            self.screen.blit(laser["image"], (laser["x"], laser["y"]))

            # Eliminar si se sale de la pantalla
            if laser["x"] > 640 or laser["y"] < 0 or laser["y"] > 480:
                self.lasers.remove(laser)

        for misil in self.misiles[:]:
            misil.update(self.screen)
            if misil.fuera_de_pantalla():
                self.misiles.remove(misil)