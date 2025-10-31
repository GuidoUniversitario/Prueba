import unittest
from unittest.mock import patch, MagicMock
from collections import defaultdict
import pygame
import sys
import os

# Añadir el path para importar nave.py desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nave import Nave


class TestNave(unittest.TestCase):

    def setUp(self):
        # Mock general de las funciones de pygame para evitar carga de imágenes reales
        patcher_load = patch('pygame.image.load', return_value=MagicMock())
        patcher_scale = patch('pygame.transform.scale', side_effect=lambda img, size: img)
        self.addCleanup(patcher_load.stop)
        self.addCleanup(patcher_scale.stop)
        patcher_load.start()
        patcher_scale.start()

        # Evitar inicialización completa de pygame
        pygame.display.set_mode = MagicMock()

        self.nave = Nave()

    def test_inicializacion(self):
        """Verifica los valores iniciales de la nave."""
        self.assertEqual(len(self.nave.spaceship_frames), 3)
        self.assertEqual(self.nave.spaceship_x, 50)
        self.assertEqual(self.nave.spaceship_y, 200)
        self.assertEqual(self.nave.frame_index, 0)
        self.assertEqual(self.nave.animation_timer, 0)
        self.assertEqual(self.nave.animation_speed, 100)
        self.assertEqual(self.nave.modo_disparo, "normal")

    @patch('pygame.key.get_pressed')
    def test_mover_sin_tecla(self, mock_get_pressed):
        """Si no se presionan teclas, la nave no debe moverse."""
        mock_get_pressed.return_value = defaultdict(lambda: False)

        screen = MagicMock()
        x_antes, y_antes = self.nave.spaceship_x, self.nave.spaceship_y

        self.nave.mover(screen, dt=50)

        self.assertEqual(self.nave.spaceship_x, x_antes)
        self.assertEqual(self.nave.spaceship_y, y_antes)
        screen.blit.assert_called_once()  # Debe dibujar aunque no se mueva

    @patch('pygame.key.get_pressed')
    def test_mover_con_teclas(self, mock_get_pressed):
        """Debe moverse hacia arriba e izquierda cuando se presionan las teclas."""
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
        """La nave no debe salir de los límites de la pantalla."""
        mock_get_pressed.return_value = defaultdict(lambda: False)

        self.nave.spaceship_x = -10
        self.nave.spaceship_y = -20
        screen = MagicMock()
        self.nave.mover(screen, dt=0)

        self.assertGreaterEqual(self.nave.spaceship_x, 0)
        self.assertGreaterEqual(self.nave.spaceship_y, 0)

        self.nave.spaceship_x = 700
        self.nave.spaceship_y = 500
        self.nave.mover(screen, dt=0)

        self.assertLessEqual(self.nave.spaceship_x, 640 - 50)
        self.assertLessEqual(self.nave.spaceship_y, 480 - 50)

    @patch('pygame.key.get_pressed')
    def test_animacion_cambia_frame(self, mock_get_pressed):
        """Debe avanzar al siguiente frame de animación si el timer >= speed."""
        mock_get_pressed.return_value = defaultdict(lambda: False)

        screen = MagicMock()
        frame_inicial = self.nave.frame_index

        self.nave.mover(screen, dt=100)

        frame_final = self.nave.frame_index
        esperado = (frame_inicial + 1) % len(self.nave.spaceship_frames)
        self.assertEqual(frame_final, esperado)

    @patch('pygame.key.get_pressed')
    def test_animacion_no_cambia_si_dt_chico(self, mock_get_pressed):
        """Si el delta time es muy bajo, no debe cambiar el frame."""
        mock_get_pressed.return_value = defaultdict(lambda: False)

        screen = MagicMock()
        self.nave.animation_timer = 99
        self.nave.frame_index = 1

        self.nave.mover(screen, dt=0)

        self.assertEqual(self.nave.frame_index, 1)

    def test_get_rect(self):
        """El rectángulo debe coincidir con las coordenadas y tamaño esperados."""
        rect = self.nave.get_rect()
        self.assertEqual(rect.x, self.nave.spaceship_x)
        self.assertEqual(rect.y, self.nave.spaceship_y)
        self.assertEqual(rect.width, 50)
        self.assertEqual(rect.height, 50)


if __name__ == '__main__':
    unittest.main()