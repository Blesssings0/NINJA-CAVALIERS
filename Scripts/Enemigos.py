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
        self.velocidad = constantes.Velocidad_Enemigo

    def dibujar(self, interfaz):
        if self.forma:  # Solo dibujar si el enemigo no ha sido eliminado
            imagen_flip = pygame.transform.flip(self.image, self.flip, False)
            interfaz.blit(imagen_flip, self.forma)
            pygame.draw.rect(interfaz, (0, 255, 0), self.forma, 2)  # Verde con grosor de 2 píxeles

    def Update_Frame(self):
        if self.forma:  # Solo actualizar si el enemigo no ha sido eliminado
            cooldown_animaciones = 100
            self.image = self.animaciones[self.frame_index]

            if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0

    def movimiento(self, velocidad_x, velocidad_y, grilla):
        if self.forma:  # Solo mover si el enemigo no ha sido eliminado
            if not self.verificar_colision(grilla, velocidad_x, 0):
                self.forma.x += velocidad_x
                if velocidad_x < 0:
                    self.flip = True
                elif velocidad_x > 0:
                    self.flip = False
            if not self.verificar_colision(grilla, 0, velocidad_y):
                self.forma.y += velocidad_y

    def verificar_colision(self, grilla, dx, dy):
        if not self.forma:  # Si el enemigo ha sido eliminado, no hay colisión
            return False
        tile_size = constantes.Tile_Size
        enemigo_rect = self.forma.copy()
        enemigo_rect.x += dx
        enemigo_rect.y += dy

        for y, row in enumerate(grilla):
            for x, tile in enumerate(row):
                if tile == 1:
                    obstaculo_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    if enemigo_rect.colliderect(obstaculo_rect):
                        return True
        return False

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            print("¡Enemigo derrotado!")

    def buscar_camino(self, grilla, objetivo):
        if self.forma:  # Solo buscar camino si el enemigo no ha sido eliminado
            inicio = (self.forma.centerx // constantes.Tile_Size, self.forma.centery // constantes.Tile_Size)
            objetivo = (objetivo[0] // constantes.Tile_Size, objetivo[1] // constantes.Tile_Size)
            self.camino = astar(grilla, inicio, objetivo)

    def seguir_camino(self):
        if self.forma and self.camino:  # Solo seguir camino si el enemigo no ha sido eliminado
            siguiente = self.camino.pop(0)
            self.forma.center = (siguiente[0] * constantes.Tile_Size + constantes.Tile_Size // 2,
                                 siguiente[1] * constantes.Tile_Size + constantes.Tile_Size // 2)

    def perseguir_jugador(self, grilla, jugador):
        if self.forma:  # Solo perseguir si el enemigo no ha sido eliminado
            distancia = ((self.forma.centerx - jugador.forma.centerx) ** 2 + (self.forma.centery - jugador.forma.centery) ** 2) ** 0.5
            if distancia < 200:  # Distancia de detección
                self.buscar_camino(grilla, jugador.forma.center)
                if self.forma.centerx < jugador.forma.centerx:
                    self.flip = False
                else:
                    self.flip = True