import unittest
from unittest.mock import Mock, patch
import pygame
import sys
import os

# Importar la clase desde el archivo fuente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from nave_enemiga import Nave_Enemiga

class TestNaveEnemiga(unittest.TestCase):

    @patch('pygame.transform.scale')
    @patch('pygame.image.load')
    def setUp(self, mock_load, mock_scale):
        # Mocks de imágenes
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        self.mock_screen = Mock()
        self.nave = Nave_Enemiga(self.mock_screen)

    def test_inicializacion_correcta(self):
        self.assertEqual(len(self.nave.nave_enemiga_frames), 3)
        self.assertIn(self.nave.direccion, [0, 1])
        self.assertEqual(self.nave.x, 480)
        if self.nave.direccion == 1:
            self.assertEqual(self.nave.y, 480)
            self.assertEqual(self.nave.velocidad, -3)
        else:
            self.assertEqual(self.nave.y, 0)
            self.assertEqual(self.nave.velocidad, 3)

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    @patch('pygame.time.get_ticks')
    def test_mover_dispara_en_intervalo(self, mock_get_ticks, mock_scale, mock_load):
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        # Simula el paso del tiempo para que dispare
        mock_get_ticks.return_value = self.nave.ultimo_disparo + self.nave.intervalo_disparo + 1

        disparo = self.nave.mover(self.mock_screen, dt=200)
        self.assertIsNotNone(disparo)

    @patch('pygame.time.get_ticks')
    def test_mover_sin_disparo_fuera_de_intervalo(self, mock_get_ticks):
        # Simula que no ha pasado suficiente tiempo
        mock_get_ticks.return_value = self.nave.ultimo_disparo + self.nave.intervalo_disparo - 1

        disparo = self.nave.mover(self.mock_screen, dt=200)
        self.assertIsNone(disparo)

    def test_fuera_de_pantalla(self):
        if self.nave.direccion == 1:
            self.nave.y = -1
            self.assertTrue(self.nave.fuera_de_pantalla())
        else:
            self.nave.y = 481
            self.assertTrue(self.nave.fuera_de_pantalla())