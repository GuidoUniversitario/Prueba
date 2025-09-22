import pygame
from nave import Nave
from disparo import Disparo
from fondo import Fondo
from asteroide import Asteroide
from nave_enemiga import Nave_Enemiga
from disparo_enemigo import Disparo_Enemigo
from nave_veloz import Nave_Veloz
from explosion import Explosion
from vidas import Vidas

def jugar(vidas_restantes=3):
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mi primer juego")
    nave = Nave()

    fondo = Fondo(screen)
    disparo = Disparo(screen)
    asteroide = Asteroide()
    nave_enemiga = Nave_Enemiga(screen)
    nave_veloz = Nave_Veloz(nave)
    disparos_enemigos = []
    explosion = None
    vidas = Vidas(vidas_restantes, screen)

    clock = pygame.time.Clock()

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
            if asteroide.fuera_de_pantalla():
                asteroide = Asteroide()

            if nave_enemiga.fuera_de_pantalla():
                nave_enemiga = Nave_Enemiga(screen)

            disparo.update()
            nave.mover(screen, dt)
            asteroide.mover(screen)
            disparo_enemigo_nuevo = nave_enemiga.mover(screen, dt)
            if disparo_enemigo_nuevo:
                disparos_enemigos.append(disparo_enemigo_nuevo)
            nave_veloz.update(dt)
            screen.blit(nave_veloz.image, nave_veloz.rect)

            if explosion is None and nave.get_rect().colliderect(asteroide.get_rect()):
                explosion = Explosion(nave.spaceship_x, nave.spaceship_y)

            if explosion is None and nave.get_rect().colliderect(nave_enemiga.get_rect()):
                explosion = Explosion(nave.spaceship_x, nave.spaceship_y)

            if explosion is None and nave.get_rect().colliderect(nave_veloz.get_rect()):
                explosion = Explosion(nave.spaceship_x, nave.spaceship_y)

        for laser in disparo.lasers:
            if laser["rect"].colliderect(asteroide.rect):
                disparo.lasers.remove(laser)
                asteroide = Asteroide()
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

                    pygame.quit()
                    return
                else:
                    jugar(vidas.vidas)
                    return

        vidas.mostrar()
        pygame.display.flip()

jugar()
