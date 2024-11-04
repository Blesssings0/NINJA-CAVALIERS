# personaje.py
import pygame
import constantes
from letras_flotantes import LetrasFlotantes  # Importar la clase LetrasFlotantes

class Personaje:
    def __init__(self, x, y, animaciones, animaciones_ataque):
        self.flip = False
        self.animaciones = animaciones
        self.animaciones_ataque = animaciones_ataque
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, constantes.Ancho_PERSONAJE, constantes.Alto_personaje)
        self.forma.center = (x, y)
        self.atacando = False

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        pygame.draw.rect(interfaz, (0, 255, 0), self.forma, 2)  # Verde con grosor de 2 píxeles

    def Update_Frame(self):
        cooldown_animaciones = 100
        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()  

        if self.atacando:
            if self.frame_index >= len(self.animaciones_ataque):    
                self.frame_index = 0
                self.atacando = False
            self.image = self.animaciones_ataque[self.frame_index]
        else:
            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0
            self.image = self.animaciones[self.frame_index]

    def movimiento(self, posicion_x, posicion_y, grilla):
        if not self.verificar_colision(grilla, posicion_x, 0):
            self.forma.x += posicion_x
        if not self.verificar_colision(grilla, 0, posicion_y):
            self.forma.y += posicion_y

        if posicion_x < 0:
            self.flip = True
        if posicion_x > 0:
            self.flip = False 

    def verificar_colision(self, grilla, dx, dy):
        tile_size = constantes.Tile_Size
        jugador_rect = self.forma.copy()
        jugador_rect.x += dx
        jugador_rect.y += dy

        for y, row in enumerate(grilla):
            for x, tile in enumerate(row):
                if tile == 1:
                    obstaculo_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    if jugador_rect.colliderect(obstaculo_rect):
                        return True
        return False

    def atacar(self, enemigos, letras_flotantes):
        self.atacando = True
        for enemigo in enemigos:
            if self.forma.colliderect(enemigo.forma):
                dano = 10  # Cantidad de daño infligido
                enemigo.recibir_dano(dano)
                letras_flotantes.append(LetrasFlotantes(enemigo.forma.centerx, enemigo.forma.centery, str(dano), (255, 0, 0)))