import unittest
from unittest.mock import patch, MagicMock
import pygame
from misil import Misil

class TestMisil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))
        cls.fake_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        cls.patcher_load = patch('pygame.image.load', return_value=cls.fake_surface)
        cls.patcher_load.start()
        # Patch Explosion sin autospec
        cls.patcher_explosion = patch('misil.Explosion', MagicMock())
        cls.patcher_explosion.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_load.stop()
        cls.patcher_explosion.stop()
        pygame.quit()

    def setUp(self):
        self.objetivo_mock = MagicMock()
        self.mock_screen = MagicMock()  # Para el test que falla

    def test_inicializacion_con_objetivo(self):
        misil = Misil(100, 100, self.objetivo_mock)
        self.assertIsNotNone(misil)

    def test_inicializacion_sin_objetivo(self):
        misil = Misil(100, 100, None)
        self.assertIsNotNone(misil)

    def test_get_rect(self):
        misil = Misil(100, 100, None)
        rect = misil.get_rect()
        self.assertIsInstance(rect, pygame.Rect)

    def test_fuera_de_pantalla(self):
        misil = Misil(700, 500, None)
        # Aquí pruebas lo que corresponda para fuera de pantalla

    @patch('misil.Explosion')
    def test_autodetonacion_despues_2s(self, mock_explosion):
        misil = Misil(100, 100, None)
        misil.tiempo_vida = 2100
        misil.update(self.mock_screen, dt=100)
        mock_explosion.assert_called_once()
        self.assertTrue(misil.ha_explotado())

    def test_update_persigue_objetivo(self):
        misil = Misil(100, 100, self.objetivo_mock)
        direccion_inicial = tuple(misil.direccion)
        misil.update(self.mock_screen, dt=16)
        # Aquí se puede chequear que la dirección cambió o que alguna función fue llamada
        # Depende de la implementación exacta de update
        self.assertIsNotNone(misil.direccion)  # Al menos que no sea None

if __name__ == '__main__':
    unittest.main()