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
    nave_nodriza = None

    def spawn_enemigo(tipo):
        nonlocal nave_nodriza
        
        if tipo == "asteroide":
            asteroides.append(Asteroide())
        elif tipo == "asteroide_grande":
            asteroides_grandes.append(Asteroide_Grande())
        elif tipo == "nave_enemiga":
            naves_enemigas.append(Nave_Enemiga(screen))
        elif tipo == "nave_veloz":
            naves_veloces.append(Nave_Veloz(nave))
        elif tipo == "nave_nodriza":
            if nave_nodriza is None:
                from nave_nodriza import Nave_Nodriza
                nave_nodriza = Nave_Nodriza(screen, disparos_enemigos, disparo.lasers)

    clock = pygame.time.Clock()

    def esta_nodriza_viva():
        return nave_nodriza is not None and not nave_nodriza.esta_destruida

    manejador_oleadas = ManejadorOleadas(spawn_enemigo, esta_nodriza_viva)
    manejador_oleadas.iniciar()

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    disparo.shoot(nave.spaceship_x, nave.spaceship_y)

        fondo.mover()

        if explosion is None:
            disparo.update()
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

            if nave_nodriza:
                nave_nodriza.update()
                nave_nodriza.draw()
                if nave_nodriza.esta_destruida:
                    explosiones.append(Explosion(nave_nodriza.rect.x, nave_nodriza.rect.y, 150))
                    nave_nodriza = None

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

        for laser in disparo.lasers[:]:
            colision_detectada = False
            for ast in asteroides[:]:
                if laser["rect"].colliderect(ast.get_rect()):
                    colision_detectada = True
                    disparo.lasers.remove(laser)
                    explosiones.append(Explosion(ast.x, ast.y))
                    asteroides.remove(ast)
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
                    break
            for nave_v in naves_veloces:
                if laser["rect"].colliderect(nave_v.get_rect()):
                    colision_detectada = True
                    disparo.lasers.remove(laser)
                    explosiones.append(Explosion(nave_v.rect.x, nave_v.rect.y))
                    naves_veloces.remove(nave_v)
                    break
            if nave_nodriza and not nave_nodriza.esta_destruida:
                for laser in disparo.lasers[:]:
                    if nave_nodriza.get_rect().colliderect(laser["rect"]):
                        explosiones.append(Explosion(laser["rect"].x, laser["rect"].y))
                        disparo.lasers.remove(laser)
                        nave_nodriza.recibir_dano()

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
        pygame.display.flip()
jugar()
