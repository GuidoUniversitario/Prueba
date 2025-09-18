import unittest
from unittest.mock import patch, Mock
import pygame
from asteroide import Asteroide

class TestAsteroide(unittest.TestCase):

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_asteroide_mueve_hacia_la_izquierda(self, mock_scale, mock_load):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        asteroide = Asteroide()
        x_inicial = asteroide.x
        asteroide.mover(Mock())  # screen mock
        self.assertLess(asteroide.x, x_inicial)

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_fuera_de_pantalla(self, mock_scale, mock_load):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        asteroide = Asteroide()
        asteroide.x = -10
        self.assertTrue(asteroide.fuera_de_pantalla())

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_dentro_de_pantalla(self, mock_scale, mock_load):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        asteroide = Asteroide()
        asteroide.x = 100
        self.assertFalse(asteroide.fuera_de_pantalla())

if __name__ == "__main__":
    unittest.main()