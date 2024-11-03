# Enemigos.py
import pygame
import constantes
from astar import astar

class Enemigo:
    def __init__(self, x, y, animaciones):
        # Inicializa el enemigo con su posición, animaciones y velocidad
        self.flip = False  # Indica si el sprite debe ser volteado horizontalmente
        self.animaciones = animaciones  # Lista de animaciones del enemigo
        self.frame_index = 0  # Índice del frame actual de la animación
        self.update_time = pygame.time.get_ticks()  # Tiempo de la última actualización del frame
        self.image = animaciones[self.frame_index]  # Imagen actual del enemigo
        self.forma = pygame.Rect(0, 0, constantes.Ancho_ENEMIGO, constantes.Alto_ENEMIGO)  # Rectángulo que representa la forma del enemigo
        self.forma.center = (x, y)  # Posición inicial del enemigo
        self.salud = 100  # Salud del enemigo
        self.camino = []  # Lista de posiciones que forman el camino a seguir
        self.velocidad = constantes.Velocidad_Enemigo  # Utilizar la constante Velocidad_Enemigo

    def dibujar(self, interfaz):
        # Dibuja el enemigo en la interfaz
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)  # Voltea la imagen si es necesario
        interfaz.blit(imagen_flip, self.forma)  # Dibuja la imagen en la posición del rectángulo

    def Update_Frame(self):
        # Actualiza el frame de la animación del enemigo
        cooldown_animaciones = 100  # Tiempo entre frames de la animación
        self.image = self.animaciones[self.frame_index]  # Actualiza la imagen actual

        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1  # Avanza al siguiente frame
            self.update_time = pygame.time.get_ticks()  # Actualiza el tiempo de la última actualización

        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0  # Reinicia el índice de frames si llega al final

    def movimiento(self, velocidad_x, velocidad_y, grilla):
        # Mueve al enemigo en la dirección indicada, verificando colisiones
        if not self.verificar_colision(grilla, velocidad_x, 0):
            self.forma.x += velocidad_x
            if velocidad_x < 0:
                self.flip = True  # Voltea la imagen si se mueve a la izquierda
            elif velocidad_x > 0:
                self.flip = False  # No voltea la imagen si se mueve a la derecha
        if not self.verificar_colision(grilla, 0, velocidad_y):
            self.forma.y += velocidad_y

    def verificar_colision(self, grilla, dx, dy):
        # Verifica si el enemigo colisiona con algún obstáculo en la grilla
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
        # Reduce la salud del enemigo al recibir daño
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            print("¡Enemigo derrotado!")

    def buscar_camino(self, grilla, objetivo):
        # Calcula el camino hacia el objetivo usando el algoritmo A*
        inicio = (self.forma.centerx // constantes.Tile_Size, self.forma.centery // constantes.Tile_Size)
        objetivo = (objetivo[0] // constantes.Tile_Size, objetivo[1] // constantes.Tile_Size)
        self.camino = astar(grilla, inicio, objetivo)

    def seguir_camino(self):
        # Sigue el camino calculado hacia el objetivo
        if self.camino:
            siguiente = self.camino.pop(0)
            self.forma.center = (siguiente[0] * constantes.Tile_Size + constantes.Tile_Size // 2,
                                 siguiente[1] * constantes.Tile_Size + constantes.Tile_Size // 2)

    def perseguir_jugador(self, grilla, jugador):
        # Persigue al jugador si está dentro de la distancia de detección
        distancia = ((self.forma.centerx - jugador.forma.centerx) ** 2 + (self.forma.centery - jugador.forma.centery) ** 2) ** 0.5
        if distancia < 200:  # Distancia de detección
            self.buscar_camino(grilla, jugador.forma.center)
            # Ajustar la dirección de mirada en función de la posición del jugador
            if self.forma.centerx < jugador.forma.centerx:
                self.flip = False
            else:
                self.flip = True