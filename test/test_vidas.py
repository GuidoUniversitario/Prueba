import unittest
from unittest.mock import patch, Mock
from vidas import Vidas

class TestVidas(unittest.TestCase):

    @patch("pygame.transform.scale")
    @patch("pygame.image.load")
    def test_restar_y_resetear_vidas(self, mock_load, mock_scale):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        screen_mock = Mock()
        vidas = Vidas(3, screen_mock)

        vidas.restar()
        self.assertEqual(vidas.vidas, 2)

        vidas.restar()
        vidas.restar()
        self.assertTrue(vidas.esta_sin_vidas())

        vidas.reset(5)
        self.assertEqual(vidas.vidas, 5)

    @patch("pygame.transform.scale")
    @patch("pygame.image.load")
    def test_mostrar_vidas_no_crashea(self, mock_load, mock_scale):
        mock_img = Mock()
        mock_load.return_value = mock_img
        mock_scale.return_value = mock_img

        screen_mock = Mock()
        vidas = Vidas(3, screen_mock)
        vidas.mostrar()  # solo queremos que no falle

if __name__ == "__main__":
    unittest.main()