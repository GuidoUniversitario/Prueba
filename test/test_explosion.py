import unittest
from unittest.mock import patch, Mock
from explosion import Explosion

class TestExplosion(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_explosion_animacion_completa(self, mock_scale, mock_load):
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        explosion = Explosion(100, 100)
        tiempo_total = 0
        dt = 150

        mock_screen = Mock()
        while not explosion.finished:
            explosion.update(mock_screen, dt)
            tiempo_total += dt

        self.assertTrue(explosion.finished)
        self.assertGreaterEqual(tiempo_total, 450)

if __name__ == "__main__":
    unittest.main()