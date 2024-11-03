# Enemigos.py
import pygame
import constantes
from astar import astar

class Enemigo:
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, constantes.Ancho_ENEMIGO, constantes.Alto_ENEMIGO)
        self.forma.center = (x, y)
        self.salud = 100
        self.camino = []

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        # pygame.draw.rect(interfaz, (255, 0, 0), self.forma, 2)  # Rojo con grosor de 2 píxeles

    def Update_Frame(self):
        cooldown_animaciones = 100
        self.image = self.animaciones[self.frame_index]

        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def movimiento(self, velocidad_x, velocidad_y):
        self.forma.x += velocidad_x
        self.forma.y += velocidad_y

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            print("¡Enemigo derrotado!")

    def buscar_camino(self, grilla, objetivo):
        inicio = (self.forma.centerx // constantes.Tile_Size, self.forma.centery // constantes.Tile_Size)
        objetivo = (objetivo[0] // constantes.Tile_Size, objetivo[1] // constantes.Tile_Size)
        self.camino = astar(grilla, inicio, objetivo)

    def seguir_camino(self):
        if self.camino:
            siguiente = self.camino.pop(0)
            self.forma.center = (siguiente[0] * constantes.Tile_Size + constantes.Tile_Size // 2,
                                 siguiente[1] * constantes.Tile_Size + constantes.Tile_Size // 2)