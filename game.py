# game.py
import pygame
import constantes
from utils import scalar_imagen
from personaje import Personaje
from Enemigos import Enemigo
from Mapa import Mundo
from Coliciones import manejar_colisiones

def dibujar_elementos(screen, background_image, world, Jugador, cavalier, Lanzador, Soldier):
    screen.blit(background_image, (0, 0))  # Draw the background image
    world.draw(screen)
    Jugador.dibujar(screen)
    cavalier.dibujar(screen)
    Lanzador.dibujar(screen)
    Soldier.dibujar(screen)
    # dibujar_grid()

def manejar_eventos(Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, Jugador, enemigos):
    atacando = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, atacando

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Mover_arriba = True
            if event.key == pygame.K_DOWN:
                Mover_abajo = True
            if event.key == pygame.K_LEFT:
                Mover_izquierda = True
            if event.key == pygame.K_RIGHT:
                Mover_derecha = True
            if event.key == pygame.K_a:
                atacando = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                Mover_arriba = False
            if event.key == pygame.K_DOWN:
                Mover_abajo = False
            if event.key == pygame.K_LEFT:
                Mover_izquierda = False
            if event.key == pygame.K_RIGHT:
                Mover_derecha = False
            if event.key == pygame.K_a:
                atacando = False


    return True, Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, atacando