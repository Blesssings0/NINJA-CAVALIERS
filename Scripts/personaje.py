# personaje.py
# Autor: [Julio Antonio Solis]
# Matrícula: [22-SISN-2-027]

import pygame
import constantes
from Enemigos import Enemigo
from typing import List
from texto_dano import TextoDano

class Personaje:
    def __init__(self, x, y, animaciones, animaciones_ataque):
        # Inicializa el personaje con su posición, animaciones y otros atributos
        self.flip = False
        self.animaciones = animaciones
        self.animaciones_ataque = animaciones_ataque
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, constantes.Ancho_PERSONAJE, constantes.Alto_personaje)
        self.forma.center = (x, y)
        self.atacando = False
        self.direccion = "derecha"
        self.salud = 100
        self.max_salud = 100
        self.sonido_ataque = pygame.mixer.Sound("Assets/Sounds/attack.mp3")
        self.attack_cooldown = 200  # Milisegundos entre ataques
        self.last_attack_time = 0
        self.attack_range = 10  # Rango de ataque en píxeles
        self.attack_damage = 10
        self.derrotado = False  # Indicador de si el jugador está derrotado

    def dibujar(self, interfaz):
        # Dibuja el personaje en la interfaz si no está derrotado
        if not self.derrotado:
            imagen_flip = pygame.transform.flip(self.image, self.flip, False)
            interfaz.blit(imagen_flip, self.forma)
            self.dibujar_barra_vida(interfaz)  # Dibuja la barra de vida

    def dibujar_barra_vida(self, interfaz):
        # Calcula las dimensiones de la barra de vida
        barra_ancho = self.forma.width
        barra_alto = 5
        barra_x = self.forma.x
        barra_y = self.forma.y - 10

        # Asegura que la barra de vida no se salga de los límites de la pantalla
        if barra_x < 0:
            barra_x = 0
        if barra_x + barra_ancho > constantes.WIDTH:
            barra_x = constantes.WIDTH - barra_ancho
        if barra_y < 0:
            barra_y = 0

        # Calcula el porcentaje de vida
        porcentaje_vida = self.salud / self.max_salud

        # Dibuja el fondo de la barra de vida
        pygame.draw.rect(interfaz, (255, 0, 0), (barra_x, barra_y, barra_ancho, barra_alto))

        # Dibuja el frente de la barra de vida
        pygame.draw.rect(interfaz, (0, 255, 0), (barra_x, barra_y, barra_ancho * porcentaje_vida, barra_alto))

    def Update_Frame(self):
        # Actualiza el frame de la animación si el jugador no está derrotado
        if not self.derrotado:
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
        # Mueve el personaje si no está derrotado
        if not self.derrotado:
            nueva_x = self.forma.x + posicion_x
            nueva_y = self.forma.y + posicion_y

            # Verifica colisiones con los bordes de la ventana
            if nueva_x < 0:
                nueva_x = 0
            elif nueva_x + self.forma.width > constantes.WIDTH:
                nueva_x = constantes.WIDTH - self.forma.width

            if nueva_y < 0:
                nueva_y = 0
            elif nueva_y + self.forma.height > constantes.HEIGHT:
                nueva_y = constantes.HEIGHT - self.forma.height

            if not self.verificar_colision(grilla, nueva_x - self.forma.x, 0):
                self.forma.x = nueva_x
            if not self.verificar_colision(grilla, 0, nueva_y - self.forma.y):
                self.forma.y = nueva_y

            if posicion_x < 0:
                self.flip = True
                self.direccion = "izquierda"
            if posicion_x > 0:
                self.flip = False
                self.direccion = "derecha"
            if posicion_y < 0:
                self.direccion = "arriba"
            if posicion_y > 0:
                self.direccion = "abajo"

    def verificar_colision(self, grilla, dx, dy):
        # Verifica colisiones con los obstáculos en la grilla
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

    def atacar(self, enemigos: List[Enemigo]) -> None:
        # Realiza un ataque si el jugador no está derrotado y el cooldown ha pasado
        if self.derrotado:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.last_attack_time < self.attack_cooldown:
            return

        self.atacando = True
        self.sonido_ataque.play()
        self.last_attack_time = current_time

        attack_hitbox = self.get_attack_hitbox()
        for enemigo in enemigos:
            if enemigo.forma and attack_hitbox.colliderect(enemigo.forma):
                enemigo.recibir_dano(self.attack_damage)
                # Añade texto de daño
                texto_dano = TextoDano(enemigo.forma.centerx, enemigo.forma.centery, self.attack_damage)
                enemigo.textos_dano.append(texto_dano)

    def get_attack_hitbox(self) -> pygame.Rect:
        # Obtiene el área de colisión del ataque basado en la dirección del personaje
        attack_hitbox = pygame.Rect(0, 0, self.attack_range, self.attack_range)

        if self.direccion == "derecha":
            attack_hitbox.midleft = self.forma.midright
        elif self.direccion == "izquierda":
            attack_hitbox.midright = self.forma.midleft
        elif self.direccion == "arriba":
            attack_hitbox.midbottom = self.forma.midtop
        else:
            attack_hitbox.midtop = self.forma.midbottom

        return attack_hitbox

    def recibir_dano(self, cantidad: int, direccion: str = None) -> None:
        # Reduce la salud del personaje y verifica si ha sido derrotado
        if self.derrotado:
            return

        self.salud = max(0, self.salud - cantidad)

        if self.salud <= 0:
            self.derrotado = True  # Marca al jugador como derrotado en lugar de eliminar la forma
