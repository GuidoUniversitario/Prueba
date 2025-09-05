import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir path a src/ para poder importar disparo.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from disparo import Disparo


class TestDisparo(unittest.TestCase):

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def setUp(self, mock_scale, mock_load):
        # Mock de imagen y screen
        self.mock_image = MagicMock()
        mock_load.return_value = self.mock_image
        mock_scale.return_value = self.mock_image
        self.mock_screen = MagicMock()

        self.disparo = Disparo(screen=self.mock_screen)

    def test_inicializacion(self):
        self.assertEqual(self.disparo.lasers, [])
        self.assertEqual(self.disparo.laser_speed, 20)
        self.assertIs(self.disparo.screen, self.mock_screen)
        self.assertIs(self.disparo.laser_img, self.mock_image)

    def test_dispara_laser(self):
        self.disparo.shoot(100, 200)
        self.assertEqual(len(self.disparo.lasers), 1)
        laser = self.disparo.lasers[0]
        self.assertEqual(laser["x"], 145)  # 100 + 45
        self.assertEqual(laser["y"], 215)  # 200 + 15

    def test_mueve_lasers(self):
        # Añadir disparos manualmente
        self.disparo.lasers = [{"x": 100, "y": 50}]
        self.disparo.update()
        self.assertEqual(self.disparo.lasers[0]["x"], 120)  # Se movió 20 px

    def test_elimina_lasers_fuera_de_pantalla(self):
        # Uno dentro, uno fuera
        self.disparo.lasers = [
            {"x": 619, "y": 10},
            {"x": 640, "y": 20},
            {"x": 800, "y": 30}
        ]
        self.disparo.update()
        # Solo el primero debe quedarse
        self.assertEqual(len(self.disparo.lasers), 1)
        self.assertEqual(self.disparo.lasers[0]["x"], 639)

    def test_dibuja_lasers(self):
        self.disparo.lasers = [{"x": 100, "y": 50}]
        self.disparo.update()
        self.mock_screen.blit.assert_called_with(self.mock_image, (120, 50))


if __name__ == '__main__':
    unittest.main()