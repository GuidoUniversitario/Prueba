import unittest
from unittest.mock import Mock, patch
import pygame
from nave_nodriza import Nave_Nodriza


class TestNaveNodriza(unittest.TestCase):

    def setUp(self):
        # Mock de pantalla
        self.screen_mock = Mock()

        # Lista de disparos simulada
        self.disparos_enemigos = []
        self.disparos_jugador = pygame.sprite.Group()

        # Parcheamos las funciones de pygame que cargan imágenes
        with patch('pygame.image.load', return_value=pygame.Surface((150, 150))):
            self.nave = Nave_Nodriza(self.screen_mock, self.disparos_enemigos, self.disparos_jugador)

    def test_inicializacion(self):
        """Verifica que la nave se inicializa correctamente."""
        self.assertEqual(self.nave.estado, "entrando")
        self.assertEqual(self.nave.vida, 20)
        self.assertFalse(self.nave.esta_destruida)
        self.assertEqual(self.nave.velocidad_movimiento, 2)

    def test_entrada_a_estado_activo(self):
        """La nave cambia de 'entrando' a 'activo' al llegar a x <= 500."""
        self.nave.rect.x = 501
        self.nave.update()
        # Al moverse 1 píxel, debe quedar en 500 y volverse activa
        self.assertEqual(self.nave.rect.x, 500)
        self.assertEqual(self.nave.estado, "activo")

    def test_mover_vertical_cambia_direccion_en_limites(self):
        """Debe cambiar dirección al llegar a los límites superior o inferior."""
        self.nave.rect.top = self.nave.limite_superior
        self.nave.direccion_movimiento = -1
        self.nave.mover_vertical()
        self.assertEqual(self.nave.direccion_movimiento, 1)

        self.nave.rect.bottom = self.nave.limite_inferior
        self.nave.direccion_movimiento = 1
        self.nave.mover_vertical()
        self.assertEqual(self.nave.direccion_movimiento, -1)

    @patch("nave_nodriza.Disparo_Enemigo")
    def test_disparo_abanico_crea_5_disparos(self, mock_disparo):
        self.nave.disparo_abanico()
        self.assertEqual(len(self.disparos_enemigos), 5)
        mock_disparo.assert_called()  # Asegura que fue instanciado

    def test_recibir_dano_y_destruccion(self):
        """Verifica que recibir daño reduce vida y marca destrucción al llegar a 0."""
        self.nave.estado = "activo"
        self.nave.vida = 2
        self.nave.recibir_dano()
        self.assertEqual(self.nave.vida, 1)
        self.assertFalse(self.nave.esta_destruida)

        self.nave.recibir_dano()
        self.assertTrue(self.nave.esta_destruida)

    def test_dibujar_llama_a_blit(self):
        self.nave.draw()
        self.screen_mock.blit.assert_called_with(self.nave.imagen, self.nave.rect)

    def test_detectar_colisiones_resta_vida(self):
        """Si hay colisión con disparos del jugador, la vida debe disminuir."""

        class FakeBullet(pygame.sprite.Sprite):
            pass

        fake_bullet = FakeBullet()
        self.nave.disparos_jugador.add(fake_bullet)

        with patch('pygame.sprite.spritecollide', return_value=[fake_bullet]):
            self.nave.detectar_colisiones()

        self.assertLess(self.nave.vida, 20)

if __name__ == "__main__":
    unittest.main()