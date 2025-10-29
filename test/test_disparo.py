import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir path a src/ para poder importar disparo.py y misil.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from disparo import Disparo


class TestDisparo(unittest.TestCase):

    def setUp(self):
        # Mock de funciones de pygame
        patcher_load = patch('pygame.image.load', return_value=MagicMock())
        patcher_scale = patch('pygame.transform.scale', side_effect=lambda img, size: img)
        patcher_rect = patch('pygame.Rect', side_effect=lambda x, y, w, h: MagicMock(x=x, y=y, width=w, height=h))
        self.addCleanup(patcher_load.stop)
        self.addCleanup(patcher_scale.stop)
        self.addCleanup(patcher_rect.stop)
        patcher_load.start()
        patcher_scale.start()
        patcher_rect.start()

        # Mock de pantalla
        self.mock_screen = MagicMock()

        # Mock de misil (para no cargar imágenes ni usar lógica real)
        misil_patch = patch('disparo.Misil', autospec=True)
        self.MockMisil = misil_patch.start()
        self.addCleanup(misil_patch.stop)

        self.disparo = Disparo(screen=self.mock_screen)

    def test_inicializacion(self):
        """Debe inicializar correctamente sus listas y atributos básicos."""
        self.assertEqual(self.disparo.lasers, [])
        self.assertEqual(self.disparo.misiles, [])
        self.assertEqual(self.disparo.laser_speed, 20)
        self.assertIs(self.disparo.screen, self.mock_screen)

    def test_dispara_laser(self):
        """Debe agregar un láser con las coordenadas correctas."""
        self.disparo.shoot(100, 200)
        self.assertEqual(len(self.disparo.lasers), 1)
        laser = self.disparo.lasers[0]
        self.assertIn("x", laser)
        self.assertIn("y", laser)
        self.assertEqual(laser["x"], 145)  # 100 + 45
        self.assertEqual(laser["y"], 215)  # 200 + 15

    def test_mueve_lasers_y_dibuja(self):
        self.disparo.lasers = [{
            "x": 100,
            "y": 50,
            "dx": self.disparo.laser_speed,
            "dy": 0,
            "rect": MagicMock(),
            "image": MagicMock()
        }]
        self.disparo.update(dt=16)
        self.assertEqual(self.disparo.lasers[0]["x"], 100 + self.disparo.laser_speed)

    def test_elimina_lasers_fuera_de_pantalla(self):
        self.disparo.lasers = [
            {"x": 619, "y": 10, "dx": self.disparo.laser_speed, "dy": 0, "rect": MagicMock(), "image": MagicMock()},
            {"x": 640, "y": 20, "dx": self.disparo.laser_speed, "dy": 0, "rect": MagicMock(), "image": MagicMock()},
            {"x": 800, "y": 30, "dx": self.disparo.laser_speed, "dy": 0, "rect": MagicMock(), "image": MagicMock()}
        ]
        self.disparo.update(dt=16)
        # Solo el primero debe quedarse porque los otros están fuera de pantalla
        self.assertEqual(len(self.disparo.lasers), 1)
        self.assertEqual(self.disparo.lasers[0]["x"], 639)

    def test_dibuja_lasers(self):
        self.disparo.lasers = [{
            "x": 100,
            "y": 50,
            "dx": self.disparo.laser_speed,
            "dy": 0,
            "rect": MagicMock(),
            "image": MagicMock()
        }]
        self.disparo.update(dt=16)
        self.mock_screen.blit.assert_called_with(self.disparo.lasers[0]["image"],(self.disparo.lasers[0]["x"], self.disparo.lasers[0]["y"]))

    def test_shoot_misil_agrega_objeto(self):
        """Debe crear un misil al usar shoot_misil()."""
        enemigos_mock = [MagicMock()]
        self.disparo.shoot_misil(50, 100, enemigos_mock)
        self.assertEqual(len(self.disparo.misiles), 1)
        self.MockMisil.assert_called_once()  # Se creó un misil

    def test_update_misiles_llama_update(self):
        """Cada misil debe llamar a su metodo update()."""
        mock_misil = MagicMock()
        self.disparo.misiles = [mock_misil]
        self.disparo.update(dt=33)
        mock_misil.update.assert_called_once_with(self.mock_screen, 33)


if __name__ == '__main__':
    unittest.main()