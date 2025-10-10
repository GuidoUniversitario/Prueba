import time
import threading
import random
import pygame

class ManejadorOleadas:
    def __init__(self, spawn_callback, esta_nodriza_viva):
        """
        :param spawn_callback: Función para crear enemigos.
        :param esta_nodriza_viva: Función que devuelve True si la nave nodriza aún no ha sido destruida.
        """
        self.spawn_callback = spawn_callback
        self.esta_nodriza_viva = esta_nodriza_viva
        self.oleada_actual = 1
        self._detener = False
        self._hilo = threading.Thread(target=self._ciclo_oleadas)
        self._hilo.daemon = True

        # Cargar imágenes de los números
        self.numero_imgs = [
            pygame.image.load(f"img/future_numbers_000{i}.png") for i in range(10)
        ]
        self.numero_imgs = [pygame.transform.scale(img, (15, 20)) for img in self.numero_imgs]

    def iniciar(self):
        self._hilo.start()

    def detener(self):
        self._detener = True

    def _ciclo_oleadas(self):
        while not self._detener:
            print(f"\n🌊 Iniciando oleada {self.oleada_actual} en 5 segundos...")
            time.sleep(5)

            if self.oleada_actual % 10 == 0:
                # OLEADA ESPECIAL: JEFE
                print(f"🚨 Oleada {self.oleada_actual}: ¡Aparece la NAVE NODRIZA!")
                self.spawn_callback("nave_nodriza")

                # Esperar hasta que la nave nodriza sea destruida
                while self.esta_nodriza_viva():
                    if self._detener:
                        return
                    time.sleep(1)

                print("✅ Nave nodriza destruida. Continuando con la siguiente oleada.")

            elif self.oleada_actual == 1:
                tipos_fijos = ["asteroide", "nave_enemiga", "asteroide_grande", "nave_veloz"]
                for tipo in tipos_fijos:
                    if self._detener:
                        return
                    cantidad = random.randint(2, 5)
                    print(f"➡️ [Oleada 1] Spawneando {cantidad} enemigos tipo '{tipo}'")
                    for _ in range(cantidad):
                        if self._detener:
                            return
                        self.spawn_callback(tipo)
                        time.sleep(0.5)
                    time.sleep(2)
            else:
                # Oleadas normales
                for _ in range(5):
                    if self._detener:
                        return
                    tipo = random.choice(["asteroide", "asteroide_grande", "nave_enemiga", "nave_veloz"])
                    cantidad = random.randint(2, 5)
                    print(f"➡️ Spawneando {cantidad} enemigos tipo '{tipo}'")
                    for _ in range(cantidad):
                        if self._detener:
                            return
                        self.spawn_callback(tipo)
                        time.sleep(0.5)
                    time.sleep(2)

            self.oleada_actual += 1

    def dibujar(self, screen):
        """Dibuja el número de la oleada actual en el centro superior de la pantalla."""
        num_str = str(self.oleada_actual)
        total_width = 0
        num_imgs = []

        for char in num_str:
            img = self.numero_imgs[int(char)]
            num_imgs.append(img)
            total_width += img.get_width()

        x = (screen.get_width() - total_width) // 2
        y = 10  # distancia desde el borde superior

        for img in num_imgs:
            screen.blit(img, (x, y))
            x += img.get_width()