# personaje.py
import pygame
import constantes
from Enemigos import Enemigo
from typing import List
from texto_dano import TextoDano

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
        self.direccion = "derecha"
        self.salud = 100
        self.max_salud = 100
        self.sonido_ataque = pygame.mixer.Sound("Assets/Sounds/attack.mp3")
        self.attack_cooldown = 200  # Milliseconds between attacks
        self.last_attack_time = 0
        self.attack_range = 50  # Attack range in pixels
        self.attack_damage = 10
        self.derrotado = False  # Flag to indicate if the player is defeated


    def dibujar(self, interfaz):
        if not self.derrotado:  # Only draw if the player is not defeated
            imagen_flip = pygame.transform.flip(self.image, self.flip, False)
            interfaz.blit(imagen_flip, self.forma)
            pygame.draw.rect(interfaz, (0, 255, 0), self.forma, 2)  # Dibujar el rectángulo de colisión del jugador en verde

    def Update_Frame(self):
        if not self.derrotado:  # Only update if the player is not defeated
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
        if not self.derrotado:  # Only move if the player is not defeated
            nueva_x = self.forma.x + posicion_x
            nueva_y = self.forma.y + posicion_y

            # Verificar colisiones con los bordes de la ventana
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
                # Add damage text
                texto_dano = TextoDano(enemigo.forma.centerx, enemigo.forma.centery, self.attack_damage)
                enemigo.textos_dano.append(texto_dano)
        
    def get_attack_hitbox(self) -> pygame.Rect:
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
        if self.derrotado:
            return

        self.salud = max(0, self.salud - cantidad)

        if self.salud <= 0:
            print("Jugador Derrotado")
            self.derrotado = True  # Set the flag instead of setting forma to None
