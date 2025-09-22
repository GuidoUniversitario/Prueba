import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from disparo_enemigo import Disparo_Enemigo

class TestDisparoEnemigo(unittest.TestCase):

    @patch('pygame.transform.scale')
    @patch('pygame.image.load')
    def setUp(self, mock_load, mock_scale):
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        self.mock_screen = Mock()
        self.disparo = Disparo_Enemigo(self.mock_screen, 100, 100)

    def test_inicializacion_correcta(self):
        self.assertEqual(self.disparo.x, 145)  # 100 + 45
        self.assertEqual(self.disparo.y, 115)  # 100 + 15
        self.assertEqual(self.disparo.laser_speed, 5)

    def test_update(self):
        old_x = self.disparo.x
        self.disparo.update()
        self.assertEqual(self.disparo.x, old_x - self.disparo.laser_speed)

    def test_fuera_de_pantalla(self):
        self.disparo.x = -1
        self.assertTrue(self.disparo.fuera_de_pantalla())
        self.disparo.x = 10
        self.assertFalse(self.disparo.fuera_de_pantalla())