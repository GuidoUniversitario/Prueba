import pygame
import random
from nave import Nave
from disparo import Disparo
from fondo import Fondo
from asteroide import Asteroide
from asteroide_grande import Asteroide_Grande
from nave_enemiga import Nave_Enemiga
from disparo_enemigo import Disparo_Enemigo
from nave_veloz import Nave_Veloz
from explosion import Explosion
from vidas import Vidas
from oleadas import ManejadorOleadas
from powerup import PowerUp

def jugar(vidas_restantes=3):
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mi primer juego")
    nave = Nave()
    fondo = Fondo(screen)
    disparo = Disparo(screen)

    asteroides = []
    asteroides_grandes = []
    naves_enemigas = []
    naves_veloces = []
    disparos_enemigos = []
    explosion = None
    vidas = Vidas(vidas_restantes, screen)
    explosiones = []
    powerups = []

    def spawn_enemigo(tipo):
        if tipo == "asteroide":
            asteroides.append(Asteroide())
        elif tipo == "asteroide_grande":
            asteroides_grandes.append(Asteroide_Grande())
        elif tipo == "nave_enemiga":
            naves_enemigas.append(Nave_Enemiga(screen))
        elif tipo == "nave_veloz":
            naves_veloces.append(Nave_Veloz(nave))

    clock = pygame.time.Clock()

    manejador_oleadas = ManejadorOleadas(spawn_enemigo)
    manejador_oleadas.iniciar()

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if nave.modo_disparo == "disparo_triple":
                        disparo.shoot_triple(nave.spaceship_x, nave.spaceship_y)
                    elif nave.modo_disparo == "misil":
                        enemigos_todos = asteroides + asteroides_grandes + naves_enemigas + naves_veloces
                        disparo.shoot_misil(nave.spaceship_x, nave.spaceship_y, enemigos_todos)
                    elif nave.modo_disparo == "normal":
                        disparo.shoot(nave.spaceship_x, nave.spaceship_y)

            # Verificar si el power-up expiró
            if nave.modo_disparo != "normal" and nave.powerup_inicio:
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - nave.powerup_inicio
                if tiempo_transcurrido >= nave.powerup_tiempo:
                    nave.modo_disparo = "normal"
                    nave.powerup_inicio = None
                    nave.powerup_tiempo = 0

        keys = pygame.key.get_pressed()
        if nave.modo_disparo == "auto_disparo" and keys[pygame.K_SPACE]:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - disparo.auto_timer >= disparo.auto_cooldown:
                disparo.shoot(nave.spaceship_x, nave.spaceship_y)
                disparo.auto_timer = tiempo_actual

        fondo.mover()

        if explosion is None:
            disparo.update(dt)
            nave.mover(screen, dt)
            for asteroide in asteroides:
                asteroide.mover(screen)
            for ast in asteroides[:]:
                if ast.fuera_de_pantalla():
                    asteroides.remove(ast)
            for asteroide_grande in asteroides_grandes:
                asteroide_grande.mover(screen)
            for ast_g in asteroides_grandes[:]:
                if ast_g.fuera_de_pantalla():
                    asteroides_grandes.remove(ast_g)
            for nave_e in naves_enemigas:
                disparo_enemigo_nuevo = nave_e.mover(screen, dt)
                if disparo_enemigo_nuevo:
                    disparos_enemigos.append(disparo_enemigo_nuevo)
            for nave_e in naves_enemigas[:]:
                if nave_e.fuera_de_pantalla():
                    naves_enemigas.remove(nave_e)
            for nave_v in naves_veloces:
                nave_v.update(dt)
                screen.blit(nave_v.image, nave_v.rect)
            for nave_v in naves_veloces[:]:
                if nave_v.fuera_de_pantalla():
                    naves_veloces.remove(nave_v)
            for powerup in powerups[:]:
                powerup.mover()
                powerup.draw(screen)
                if powerup.fuera_de_pantalla():
                    powerups.remove(powerup)

            for ast in asteroides:
                if nave.get_rect().colliderect(ast.get_rect()):
                    explosion = Explosion(nave.spaceship_x, nave.spaceship_y)
                    break
            for ast_g in asteroides_grandes:
                if nave.get_rect().colliderect(ast_g.get_rect()):
                    explosion = Explosion(nave.spaceship_x, nave.spaceship_y)
                    break
            for nave_e in naves_enemigas:
                if nave.get_rect().colliderect(nave_e.get_rect()):
                    explosion = Explosion(nave.spaceship_x, nave.spaceship_y)
                    break
            for nave_v in naves_veloces:
                if nave.get_rect().colliderect(nave_v.get_rect()):
                    explosion = Explosion(nave.spaceship_x, nave.spaceship_y)
                    break
            for powerup in powerups[:]:
                if nave.get_rect().colliderect(powerup.get_rect()):
                    powerups.remove(powerup)
                    nave.modo_disparo = powerup.tipo
                    nave.powerup_tiempo = 20000  # 20 segundos
                    nave.powerup_inicio = pygame.time.get_ticks()
                    print(f"Power-up recogido: {nave.modo_disparo}")

        for laser in disparo.lasers[:]:
            colision_detectada = False
            for ast in asteroides[:]:
                if laser["rect"].colliderect(ast.get_rect()):
                    colision_detectada = True
                    disparo.lasers.remove(laser)
                    explosiones.append(Explosion(ast.x, ast.y))
                    asteroides.remove(ast)
                    if random.random() < 0.1:
                        powerups.append(PowerUp(ast.x, ast.y))
                    break  # Salir del bucle de asteroides
            if not colision_detectada:
                for ast_g in asteroides_grandes[:]:
                    if laser["rect"].colliderect(ast_g.get_rect()):
                        colision_detectada = True
                        explosiones.append(Explosion(ast_g.x, ast_g.y))
                        asteroides_grandes.remove(ast_g)
                        # Crear dos asteroides pequeños en su lugar
                        for i in range(2):
                            nuevo_ast = Asteroide()
                            nuevo_ast.x = ast_g.x
                            nuevo_ast.y = ast_g.y + random.randint(-45, 45)
                            # Velocidad vertical: uno hacia arriba, otro hacia abajo
                            if i == 0:
                                nuevo_ast.velocidad_y = -2  # Hacia arriba
                            else:
                                nuevo_ast.velocidad_y = 2  # Hacia abajo
                            nuevo_ast.rect.x = nuevo_ast.x
                            nuevo_ast.rect.y = nuevo_ast.y
                            asteroides.append(nuevo_ast)
                        break  # Salir del bucle de asteroides grandes
            if colision_detectada:
                if laser in disparo.lasers:
                    disparo.lasers.remove(laser)
            for nave_e in naves_enemigas[:]:
                if laser["rect"].colliderect(nave_e.get_rect()):
                    colision_detectada = True
                    disparo.lasers.remove(laser)
                    explosiones.append(Explosion(nave_e.x, nave_e.y))
                    naves_enemigas.remove(nave_e)
                    if random.random() < 0.1:
                        powerups.append(PowerUp(nave_e.x, nave_e.y))
                    break
            for nave_v in naves_veloces:
                if laser["rect"].colliderect(nave_v.get_rect()):
                    colision_detectada = True
                    disparo.lasers.remove(laser)
                    explosiones.append(Explosion(nave_v.rect.x, nave_v.rect.y))
                    naves_veloces.remove(nave_v)
                    if random.random() < 0.1:
                        powerups.append(PowerUp(nave_v.rect.x, nave_v.rect.y))
                    break

        for misil in disparo.misiles[:]:
            misil.update(screen, dt)  # ← ahora recibe dt para manejar su temporizador

            # Si el misil explotó automáticamente o por impacto
            if misil.ha_explotado():
                disparo.misiles.remove(misil)
                continue  # Ya terminó su ciclo

            # Comprobaciones de colisiones (solo si aún no explotó)
            colision = False

            for ast in asteroides[:]:
                if misil.get_rect().colliderect(ast.get_rect()):
                    colision = True
                    disparo.misiles.remove(misil)
                    asteroides.remove(ast)
                    explosiones.append(Explosion(ast.x, ast.y))
                    break

            if colision:
                continue

            for ast_g in asteroides_grandes[:]:
                if misil.get_rect().colliderect(ast_g.get_rect()):
                    colision = True
                    disparo.misiles.remove(misil)
                    asteroides_grandes.remove(ast_g)
                    explosiones.append(Explosion(ast_g.x, ast_g.y))

                    # Dividir en dos asteroides pequeños
                    for i in range(2):
                        nuevo_ast = Asteroide()
                        nuevo_ast.x = ast_g.x
                        nuevo_ast.y = ast_g.y + random.randint(-45, 45)
                        nuevo_ast.velocidad_y = -2 if i == 0 else 2
                        nuevo_ast.rect.x = nuevo_ast.x
                        nuevo_ast.rect.y = nuevo_ast.y
                        asteroides.append(nuevo_ast)
                    break

            if colision:
                continue

            for nave_e in naves_enemigas[:]:
                if misil.get_rect().colliderect(nave_e.get_rect()):
                    colision = True
                    disparo.misiles.remove(misil)
                    naves_enemigas.remove(nave_e)
                    explosiones.append(Explosion(nave_e.x, nave_e.y))
                    break

            if colision:
                continue

            for nave_v in naves_veloces[:]:
                if misil.get_rect().colliderect(nave_v.get_rect()):
                    colision = True
                    disparo.misiles.remove(misil)
                    naves_veloces.remove(nave_v)
                    explosiones.append(Explosion(nave_v.rect.x, nave_v.rect.y))
                    break

        for disparo_enemigo in disparos_enemigos[:]:
            disparo_enemigo.update()
            disparo_enemigo.draw()
            if disparo_enemigo.fuera_de_pantalla():
                disparos_enemigos.remove(disparo_enemigo)
            if explosion is None and nave.get_rect().colliderect(disparo_enemigo.get_rect()):
                explosion = Explosion(nave.spaceship_x, nave.spaceship_y)
                break

        if explosion:
            explosion.update(screen, dt)
            if explosion.finished:
                vidas.restar()
                if vidas.esta_sin_vidas():
                    font = pygame.font.SysFont(None, 80)
                    pygame.time.delay(1500)
                    texto = font.render("GAME OVER", True, (255, 0, 0))
                    text_rect = texto.get_rect(center=(320, 240))

                    screen.blit(texto, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(4500)
                    manejador_oleadas.detener()
                    pygame.quit()
                    return
                else:
                    jugar(vidas.vidas)
                    return
        vidas.mostrar()
        for explosion_obj in explosiones[:]:
            explosion_obj.update(screen, dt)
            if explosion_obj.finished:
                explosiones.remove(explosion_obj)
        manejador_oleadas.dibujar(screen)
        if nave.modo_disparo != "normal" and nave.powerup_inicio:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - nave.powerup_inicio
            tiempo_restante = max(0, nave.powerup_tiempo - tiempo_transcurrido)

            # Tamaño de la barra (proporcional al tiempo restante)
            barra_ancho_total = 200
            barra_alto = 15
            barra_x = 10
            barra_y = 455  # Parte inferior izquierda

            proporcion = tiempo_restante / nave.powerup_tiempo
            ancho_actual = int(barra_ancho_total * proporcion)

            # Fondo gris
            pygame.draw.rect(screen, (100, 100, 100), (barra_x, barra_y, barra_ancho_total, barra_alto))
            # Barra roja o azul (según tipo, opcional)
            color = (0, 255, 0)  # Verde, por defecto
            if nave.modo_disparo == "disparo_triple":
                color = (225, 135, 52)
            elif nave.modo_disparo == "auto_disparo":
                color = (72, 25, 173)
            elif nave.modo_disparo == "misil":
                color = (0, 100, 33)

            pygame.draw.rect(screen, color, (barra_x, barra_y, ancho_actual, barra_alto))
        pygame.display.flip()
jugar()
