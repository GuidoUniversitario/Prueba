import pygame
from nave import Nave
from disparo import Disparo
from fondo import Fondo
from asteroide import Asteroide
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

            disparo.update()
            nave.mover(screen, dt)
            asteroide.mover(screen)

            if explosion is None and nave.get_rect().colliderect(asteroide.get_rect()):
                explosion = Explosion(nave.spaceship_x, nave.spaceship_y)

        if explosion:
            explosion.update(screen, dt)
            if explosion.finished:
                vidas.restar()
                if vidas.esta_sin_vidas():
                    font = pygame.font.SysFont(None, 80)
                    texto = font.render("GAME OVER", True, (255, 0, 0))
                    text_rect = texto.get_rect(center=(320, 240))

                    screen.blit(texto, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(2000)

                    pygame.quit()
                    return
                else:
                    jugar(vidas.vidas)
                    return
        vidas.mostrar()
        pygame.display.flip()

jugar()
