# game.py
import pygame
import constantes
from utils import scalar_imagen
from personaje import Personaje
from Enemigos import Enemigo
from Mapa import Mundo
from Coliciones import manejar_colisiones, dibujar_colisiones

class FuenteVida:
    def __init__(self, x, y):
        self.forma = pygame.Rect(x, y, 20, 20)  # Tamaño de la fuente de vida
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Color verde para la fuente de vida

    def dibujar(self, screen):
        screen.blit(self.image, self.forma)

def dibujar_elementos(screen, background_image, world, Jugador, cavalier, lanzador, soldier, fuentes_vida):
    screen.blit(background_image, (0, 0))  # Draw the background image
    world.draw(screen)
    Jugador.dibujar(screen)
    cavalier.dibujar(screen)
    lanzador.dibujar(screen)
    soldier.dibujar(screen)
    for fuente in fuentes_vida:
        fuente.dibujar(screen)
    dibujar_colisiones(screen, world.grilla)  # Dibujar colisiones
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

def manejar_colisiones_fuentes(Jugador, fuentes_vida):
    for fuente in fuentes_vida[:]:
        if Jugador.forma.colliderect(fuente.forma):
            Jugador.salud = min(Jugador.max_salud, Jugador.salud + 10)
            fuentes_vida.remove(fuente)