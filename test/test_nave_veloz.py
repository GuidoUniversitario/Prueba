import unittest
from unittest.mock import Mock, patch
import pygame
import sys

# Importa la clase Nave_Veloz aquí, o colócala en un archivo separado e impórtala.
from nave_veloz import Nave_Veloz

class TestNaveVeloz(unittest.TestCase):
    def setUp(self):
        # Mockear pygame.image.load y pygame.transform.scale
        self.patcher_load = patch('pygame.image.load', return_value=Mock())
        self.patcher_scale = patch('pygame.transform.scale', return_value=Mock())
        self.mock_load = self.patcher_load.start()
        self.mock_scale = self.patcher_scale.start()

        # Mockear las imágenes como superficies válidas
        self.mock_image = Mock()
        self.mock_image.get_rect.return_value = pygame.Rect(0, 0, 50, 50)
        self.mock_scale.return_value = self.mock_image

        # Crear jugador mock con get_rect
        self.jugador_mock = Mock()
        self.jugador_mock.get_rect.return_value = pygame.Rect(0, 200, 50, 50)

        self.nave = Nave_Veloz(jugador=self.jugador_mock)

    def tearDown(self):
        self.patcher_load.stop()
        self.patcher_scale.stop()

    def test_inicializacion(self):
        # Debe comenzar justo fuera del borde derecho
        self.assertGreaterEqual(self.nave.rect.x, 640)
        self.assertGreaterEqual(self.nave.rect.y, 0)
        self.assertLessEqual(self.nave.rect.bottom, 480)

        self.assertEqual(self.nave.vel_x, -2.0)
        self.assertEqual(self.nave.max_vel_x, -10.0)

    def test_animacion_avanza_frame(self):
        frame_actual = self.nave.frame_index
        self.nave.update(150)  # Más que animation_speed
        self.assertNotEqual(self.nave.frame_index, frame_actual)

    def test_movimiento_horizontal_acelera(self):
        # Llamar update varias veces para acelerar
        for _ in range(10):
            self.nave.update(100)
        self.assertLessEqual(self.nave.vel_x, -2.0)
        self.assertGreaterEqual(self.nave.vel_x, self.nave.max_vel_x)

    def test_movimiento_vertical_sigue_al_jugador(self):
        self.nave.rect.centery = 300  # Más abajo que el jugador (200)
        vel_y_anterior = self.nave.vel_y
        self.nave.update(100)
        self.assertLess(self.nave.vel_y, vel_y_anterior)

        self.nave.rect.centery = 100  # Más arriba que el jugador (200)
        self.nave.update(100)
        self.assertGreater(self.nave.vel_y, -self.nave.max_vel_y)

    def test_limites_verticales(self):
        self.nave.rect.top = -10
        self.nave.update(100)
        self.assertEqual(self.nave.rect.top, 0)
        self.assertEqual(self.nave.vel_y, 0)

        self.nave.rect.bottom = 490
        self.nave.update(100)
        self.assertEqual(self.nave.rect.bottom, 480)
        self.assertEqual(self.nave.vel_y, 0)

    def test_fuera_de_pantalla(self):
        self.nave.rect.right = -1
        self.assertTrue(self.nave.fuera_de_pantalla())

        self.nave.rect.right = 1
        self.assertFalse(self.nave.fuera_de_pantalla())

if __name__ == '__main__':
    pygame.init()  # Necesario para inicializar módulos antes de ejecutar tests
    unittest.main()