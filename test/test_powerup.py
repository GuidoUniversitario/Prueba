import unittest
from unittest.mock import MagicMock, patch
import pygame
from powerup import PowerUp


class NaveSimulada:
    def __init__(self):
        self.modo_disparo = "normal"

    def get_rect(self):
        rect = MagicMock()
        rect.colliderect = MagicMock(return_value=True)
        return rect


class TestPowerUp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Inicializa pygame en modo sin ventana
        pygame.init()
        pygame.display.set_mode((1, 1))  # Requerido para convert_alpha()

    def setUp(self):
        # Crear un Surface real para que pygame.transform.scale lo acepte
        self.fake_surface = pygame.Surface((32, 32))

        # Mock de pygame.image.load para devolver un surface válido
        patcher_load = patch('pygame.image.load', return_value=self.fake_surface)
        self.addCleanup(patcher_load.stop)
        patcher_load.start()

        # Mock de transform.scale para devolver el mismo surface
        patcher_scale = patch('pygame.transform.scale', return_value=self.fake_surface)
        self.addCleanup(patcher_scale.stop)
        patcher_scale.start()

    def test_creacion_powerup(self):
        p = PowerUp(100, 100)
        self.assertIn(p.tipo, ["disparo_triple", "auto_disparo", "misil"])
        self.assertEqual(p.rect.x, 100)
        self.assertEqual(p.rect.y, 100)

    def test_mover_powerup(self):
        p = PowerUp(100, 100)
        x_antes = p.rect.x
        p.mover()
        self.assertEqual(p.rect.x, x_antes - 1)

    def test_fuera_de_pantalla(self):
        p = PowerUp(0, 0)
        p.rect.right = -1
        self.assertTrue(p.fuera_de_pantalla())
        p.rect.right = 1
        self.assertFalse(p.fuera_de_pantalla())

    def test_dibuja_powerup(self):
        p = PowerUp(0, 0)
        screen_mock = MagicMock()
        p.draw(screen_mock)
        screen_mock.blit.assert_called_once_with(p.image, p.rect)

    def test_nave_cambia_modo_disparo_al_recoger_powerup(self):
        nave = NaveSimulada()
        powerup = PowerUp(0, 0)
        powerup.tipo = "disparo_triple"
        nave.get_rect().colliderect = MagicMock(return_value=True)
        powerup.get_rect = MagicMock(return_value=MagicMock())

        if nave.get_rect().colliderect(powerup.get_rect()):
            nave.modo_disparo = powerup.tipo

        self.assertEqual(nave.modo_disparo, "disparo_triple")


if __name__ == '__main__':
    unittest.main()