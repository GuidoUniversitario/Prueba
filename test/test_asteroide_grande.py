import unittest
from unittest.mock import patch, Mock
import pygame
from asteroide_grande import Asteroide_Grande

class TestAsteroideGrande(unittest.TestCase):

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_asteroide_mueve_hacia_la_izquierda(self, mock_scale, mock_load):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        asteroide_grande = Asteroide_Grande()
        x_inicial = asteroide_grande.x
        asteroide_grande.mover(Mock())  # screen mock
        self.assertLess(asteroide_grande.x, x_inicial)

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_fuera_de_pantalla(self, mock_scale, mock_load):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        asteroide_grande = Asteroide_Grande()
        asteroide_grande.x = -10
        self.assertTrue(asteroide_grande.fuera_de_pantalla())

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_dentro_de_pantalla(self, mock_scale, mock_load):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        asteroide_grande = Asteroide_Grande()
        asteroide_grande.x = 100
        self.assertFalse(asteroide_grande.fuera_de_pantalla())

if __name__ == "__main__":
    unittest.main()