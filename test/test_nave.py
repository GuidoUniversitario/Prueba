import unittest
from unittest.mock import patch, MagicMock
from collections import defaultdict
import pygame
import sys
import os

# Añadir el path para importar nave.py desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nave import Nave


class TestNave(unittest.TestCase):

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def setUp(self, mock_scale, mock_load):
        # Mockear el retorno de la imagen cargada y escalada
        mock_image = MagicMock()
        mock_scale.return_value = mock_image
        self.nave = Nave()

    def test_inicializacion(self):
        self.assertEqual(len(self.nave.spaceship_frames), 3)
        self.assertEqual(self.nave.spaceship_x, 50)
        self.assertEqual(self.nave.spaceship_y, 200)
        self.assertEqual(self.nave.frame_index, 0)
        self.assertEqual(self.nave.animation_timer, 0)
        self.assertEqual(self.nave.animation_speed, 100)

    @patch('pygame.key.get_pressed')
    def test_mover_sin_tecla(self, mock_get_pressed):
        # Simular que no se presiona ninguna tecla
        mock_get_pressed.return_value = defaultdict(lambda: False)

        screen = MagicMock()
        x_antes = self.nave.spaceship_x
        y_antes = self.nave.spaceship_y

        self.nave.mover(screen, dt=50)

        self.assertEqual(self.nave.spaceship_x, x_antes)
        self.assertEqual(self.nave.spaceship_y, y_antes)

    @patch('pygame.key.get_pressed')
    def test_mover_con_teclas(self, mock_get_pressed):
        # Simular teclas presionadas
        keys = defaultdict(lambda: False)
        keys[pygame.K_LEFT] = True
        keys[pygame.K_UP] = True
        mock_get_pressed.return_value = keys

        screen = MagicMock()
        self.nave.spaceship_x = 100
        self.nave.spaceship_y = 100

        self.nave.mover(screen, dt=100)

        self.assertLess(self.nave.spaceship_x, 100)
        self.assertLess(self.nave.spaceship_y, 100)

    @patch('pygame.key.get_pressed')
    def test_limites_movimiento(self, mock_get_pressed):
        mock_get_pressed.return_value = defaultdict(lambda: False)

        self.nave.spaceship_x = -10
        self.nave.spaceship_y = -20
        screen = MagicMock()

        self.nave.mover(screen, dt=0)  # No animación ni movimiento

        self.assertGreaterEqual(self.nave.spaceship_x, 0)
        self.assertGreaterEqual(self.nave.spaceship_y, 0)

        self.nave.spaceship_x = 700
        self.nave.spaceship_y = 500
        self.nave.mover(screen, dt=0)

        self.assertLessEqual(self.nave.spaceship_x, 640 - 50)
        self.assertLessEqual(self.nave.spaceship_y, 480 - 50)

    @patch('pygame.key.get_pressed')
    def test_animacion_cambia_frame(self, mock_get_pressed):
        mock_get_pressed.return_value = defaultdict(lambda: False)

        screen = MagicMock()
        frame_inicial = self.nave.frame_index

        self.nave.mover(screen, dt=100)

        frame_final = self.nave.frame_index
        esperado = (frame_inicial + 1) % len(self.nave.spaceship_frames)
        self.assertEqual(frame_final, esperado)

    @patch('pygame.key.get_pressed')
    def test_animacion_no_cambia_si_dt_chico(self, mock_get_pressed):
        mock_get_pressed.return_value = defaultdict(lambda: False)

        screen = MagicMock()
        self.nave.animation_timer = 99
        self.nave.frame_index = 1

        self.nave.mover(screen, dt=0)

        self.assertEqual(self.nave.frame_index, 1)


if __name__ == '__main__':
    unittest.main()