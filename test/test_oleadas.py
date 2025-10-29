import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock
from oleadas import ManejadorOleadas

class TestManejadorOleadas(TestCase):

    @patch('oleadas.pygame.transform.scale', side_effect=lambda img, size: img)
    @patch('oleadas.pygame.image.load', return_value=MagicMock())
    @patch('oleadas.time.sleep', return_value=None)
    @patch('oleadas.random.randint', return_value=3)
    def test_ciclo_oleadas_primera(self, mock_randint, mock_sleep, mock_load, mock_scale):
        spawn_callback = MagicMock()
        manejador = ManejadorOleadas(spawn_callback)
        manejador._detener = False
        manejador.oleada_actual = 1

        def detener_despues_un_ciclo(*args, **kwargs):
            if not hasattr(detener_despues_un_ciclo, "called"):
                detener_despues_un_ciclo.called = True
                return None
            manejador._detener = True
            return None

        mock_sleep.side_effect = detener_despues_un_ciclo

        manejador._ciclo_oleadas()

        llamadas = [call.args[0] for call in spawn_callback.call_args_list]
        tipos_esperados = ["asteroide", "nave_enemiga", "asteroide_grande", "nave_veloz"]
        for tipo in tipos_esperados:
            self.assertTrue(
                llamadas.count(tipo) >= 1,
                f"Se esperaba al menos 1 enemigo tipo '{tipo}' pero se spawnearon {llamadas.count(tipo)}"
            )

    @patch('oleadas.pygame.transform.scale', side_effect=lambda img, size: img)
    @patch('oleadas.pygame.image.load', return_value=MagicMock())
    @patch('oleadas.time.sleep', return_value=None)
    @patch('oleadas.random.randint', return_value=2)
    @patch('oleadas.random.choice', side_effect=["nave_enemiga", "asteroide_grande", "asteroide"])
    def test_ciclo_oleadas_siguientes(self, mock_choice, mock_randint, mock_sleep, mock_load, mock_scale):
        spawn_callback = MagicMock()
        manejador = ManejadorOleadas(spawn_callback)
        manejador._detener = False
        manejador.oleada_actual = 2

        def detener_despues_un_ciclo(*args, **kwargs):
            if not hasattr(detener_despues_un_ciclo, "called"):
                detener_despues_un_ciclo.called = True
                return None
            manejador._detener = True
            return None

        mock_sleep.side_effect = detener_despues_un_ciclo

        manejador._ciclo_oleadas()

        llamadas = [call.args[0] for call in spawn_callback.call_args_list]
        tipos_esperados = ["nave_enemiga", "asteroide_grande", "asteroide"]
        for tipo in tipos_esperados:
            self.assertGreaterEqual(
                llamadas.count(tipo),
                1,
                f"Se esperaba al menos 1 '{tipo}' pero se spawnearon {llamadas.count(tipo)}."
            )

if __name__ == "__main__":
    unittest.main()