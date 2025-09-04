import unittest
from unittest.mock import Mock, patch
from src.fondo import Fondo  # asumiendo que la clase está en fondo.py


class TestFondo(unittest.TestCase):

    def setUp(self):
        # Parchamos pygame.image.load para que no cargue archivos reales
        patcher = patch("pygame.image.load")
        self.addCleanup(patcher.stop)
        self.mock_image_load = patcher.start()
        self.fake_surface = Mock()
        self.mock_image_load.return_value = self.fake_surface

        # Creamos una pantalla falsa
        self.mock_screen = Mock()

        # Instanciamos la clase a probar
        self.fondo = Fondo(self.mock_screen)

    def test_init_sets_attributes(self):
        self.assertEqual(self.fondo.screen, self.mock_screen)
        self.assertEqual(self.fondo.tile_size, 64)
        self.assertEqual(self.fondo.scroll_speed, 1)
        self.assertEqual(self.fondo.offset_x, 0)
        self.mock_image_load.assert_called_once_with("img/stars_big.png")

    def test_mover_disminuye_offset(self):
        self.fondo.offset_x = 0
        self.fondo.mover()

        self.assertEqual(self.fondo.offset_x, -1)
        self.mock_screen.fill.assert_called_once_with((0, 0, 0))
        self.assertGreater(self.mock_screen.blit.call_count, 0)

    def test_mover_reinicia_offset_al_salir_de_pantalla(self):
        self.fondo.offset_x = -64  # límite exacto
        self.fondo.mover()

        self.assertEqual(self.fondo.offset_x, 0)

    def test_mover_dibuja_tiles_esperados(self):
        self.fondo.mover()

        # En 480px de alto con tile_size=64 → 8 filas
        # En 640px de ancho + 64 extra con tile_size=64 → 11 columnas
        expected_tiles = 8 * 11

        self.assertEqual(self.mock_screen.blit.call_count, expected_tiles)


if __name__ == "__main__":
    unittest.main()
