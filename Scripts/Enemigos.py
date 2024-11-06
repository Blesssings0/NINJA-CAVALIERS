# Enemigos.py
import pygame
import personaje
import constantes
from astar import astar
from behavior_tree import Selector, Sequence, Action, Timer
from texto_dano import TextoDano

class Enemigo:
    def __init__(self, x, y, animaciones, animaciones_ataque):
        self.flip = False
        self.jugador = None  # Referencia al jugador
        self.animaciones = animaciones
        self.animaciones_ataque = animaciones_ataque
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, constantes.Ancho_ENEMIGO, constantes.Alto_ENEMIGO)
        self.forma.center = (x, y)
        self.salud = 100
        self.max_salud = 100
        self.attack_damage = 2
        self.attack_cooldown = 500
        self.last_attack_time = 0
        self.attack_range = 5

        self.camino = []
        self.velocidad = constantes.Velocidad_Enemigo
        self.jugador = None  # Referencia al jugador
        self.grilla = None  # Referencia a la grilla del mapa
        self.distancia_perseguida = 0  # Distancia que el enemigo ha perseguido al jugador
        self.distancia_max_persecucion = 1000  # Distancia máxima de persecución aumentada
        self.atacando = False
        self.derrotado = False  # Flag to indicate if the enemy is defeated
        self.textos_dano = []  # List to store damage texts

        # Definir el árbol de comportamiento
        self.behavior_tree = Selector([
            Sequence([
                Action(self.detectar_jugador),
                Action(self.perseguir_jugador)
            ]),
            Timer(5, Action(self.patrullar))  # Temporizador de 5 segundos para patrullar
        ])

        # Definir puntos de patrullaje (por defecto)
        self.puntos_patrullaje = [(x, y), (x + 100, y), (x + 100, y + 100), (x, y + 100)]
        self.punto_actual = 0

    def dibujar(self, interfaz):
        if not self.derrotado:  # Only draw if the enemy is not defeated
            imagen_flip = pygame.transform.flip(self.image, self.flip, False)
            interfaz.blit(imagen_flip, self.forma)
            pygame.draw.rect(interfaz, (0, 255, 0), self.forma, 2)  # Verde con grosor de 2 píxeles
            self.draw_textos_dano(interfaz)  # Draw damage texts

    def Update_Frame(self):
        if not self.derrotado:  # Only update if the enemy is not defeated
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

            self.update_textos_dano()  # Update damage texts

    def movimiento(self, velocidad_x, velocidad_y, grilla):
        if not self.derrotado:  # Only move if the enemy is not defeated
            if not self.verificar_colision(grilla, velocidad_x, 0):
                self.forma.x += velocidad_x
                if velocidad_x < 0:
                    self.flip = True
                elif velocidad_x > 0:
                    self.flip = False
            if not self.verificar_colision(grilla, 0, velocidad_y):
                self.forma.y += velocidad_y

    def verificar_colision(self, grilla, dx, dy):
        if self.derrotado:  # No collision if the enemy is defeated
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

    def recibir_dano(self, cantidad: int) -> None:
        if self.derrotado:
            return

        self.salud = max(0, self.salud - cantidad)
        if self.salud == 0:
            print("Enemigo derrotado")
            self.derrotado = True  # Set the flag instead of setting forma to None

        # Add damage text
        texto_dano = TextoDano(self.forma.centerx, self.forma.centery, cantidad)
        self.textos_dano.append(texto_dano)

    def update_textos_dano(self):
        for texto in self.textos_dano[:]:
            texto.update()
            if texto.tiempo_vida <= 0:
                self.textos_dano.remove(texto)

    def draw_textos_dano(self, screen):
        for texto in self.textos_dano:
            texto.draw(screen)

    def buscar_camino(self, grilla, objetivo):
        if not self.derrotado:  # Only search path if the enemy is not defeated
            inicio = (self.forma.centerx // constantes.Tile_Size, self.forma.centery // constantes.Tile_Size)
            objetivo = (objetivo[0] // constantes.Tile_Size, objetivo[1] // constantes.Tile_Size)
            self.camino = astar(grilla, inicio, objetivo)

    def seguir_camino(self):
        if not self.derrotado and self.camino:  # Only follow path if the enemy is not defeated
            siguiente = self.camino[0]
            dx = siguiente[0] * constantes.Tile_Size + constantes.Tile_Size // 2 - self.forma.centerx
            dy = siguiente[1] * constantes.Tile_Size + constantes.Tile_Size // 2 - self.forma.centery
            distancia = (dx ** 2 + dy ** 2) ** 0.5
            if distancia < self.velocidad:
                self.forma.center = (siguiente[0] * constantes.Tile_Size + constantes.Tile_Size // 2,
                                     siguiente[1] * constantes.Tile_Size + constantes.Tile_Size // 2)
                self.camino.pop(0)
            else:
                self.movimiento(dx / distancia * max(self.velocidad, 1), dy / distancia * max(self.velocidad, 1), self.grilla)

    def detectar_jugador(self):
        if not self.jugador or self.derrotado:  # Verify that both the enemy and the player exist and the enemy is not defeated
            return False
        # Calcular la distancia entre el enemigo y el jugador
        distancia = ((self.forma.centerx - self.jugador.forma.centerx) ** 2 + 
                    (self.forma.centery - self.jugador.forma.centery) ** 2) ** 0.5
        return distancia < 110  # Distancia de detección ajustada a 110

    def atacar_jugador(self, jugador) -> None:
        if self.derrotado:
            return
        current_time = pygame.time.get_ticks()

        if current_time - self.last_attack_time < self.attack_cooldown:
            return

        dx = jugador.forma.centerx - self.forma.centerx
        dy = jugador.forma.centery - self.forma.centery

        if abs(dx) > abs(dy):
            direccion = 'derecha' if dx > 0 else 'izquierda'
        else:
            direccion = 'abajo' if dy > 0 else 'arriba'

        attack_hitbox = self.get_attack_hitbox(direccion)
        if attack_hitbox.colliderect(jugador.forma):
            self.atacando = True
            self.last_attack_time = current_time
            jugador.recibir_dano(self.attack_damage, direccion)

    def get_attack_hitbox(self, dirreccion : str) -> pygame.Rect:
        attack_hitbox = pygame.Rect(0,0,self.attack_range,self.attack_range)

        if dirreccion == 'derecha':
            attack_hitbox.midleft = self.forma.midright
        elif dirreccion == 'izquierda':
            attack_hitbox.midright = self.forma.midleft
        elif dirreccion == 'arriba':
            attack_hitbox.midbottom = self.forma.midtop
        else : #? abajo
            attack_hitbox.midtop = self.forma.midbottom

        return attack_hitbox

    def recibir_dano(self,cantidad: int) -> None:
        if self.derrotado:
            return

        self.salud = max(0,self.salud - cantidad)
        if self.salud == 0:
            print("Enemigo derrotado")
            self.derrotado = True  # Set the flag instead of setting forma to None

    def perseguir_jugador(self):
        # Perseguir al jugador
        if self.distancia_perseguida < self.distancia_max_persecucion:
            self.buscar_camino(self.grilla, self.jugador.forma.center)
            self.seguir_camino()
            self.distancia_perseguida += self.velocidad
            return True
        else:
            self.distancia_perseguida = 0  # Resetear la distancia perseguida
            return False

    def patrullar(self):
        # Patrullar en un área definida
        if not self.camino:
            self.punto_actual = (self.punto_actual + 1) % len(self.puntos_patrullaje)
            objetivo = self.puntos_patrullaje[self.punto_actual]
            self.buscar_camino(self.grilla, objetivo)
        self.seguir_camino()
        return True

    def ajustar_direccion(self):
        # Ajustar la dirección del enemigo para evitar colisiones con otros enemigos o el jugador
        if self.jugador and self.forma and not self.derrotado and self.forma.colliderect(self.jugador.forma):
            if self.flip:
                self.movimiento(-self.velocidad, 0, self.grilla)
            else:
                self.movimiento(self.velocidad, 0, self.grilla)

    def actualizar_comportamiento(self):
        if not self.derrotado:
            self.behavior_tree.run()
            self.ajustar_direccion()  # Ajustar la dirección después de ejecutar el árbol de comportamiento
            if self.jugador and self.detectar_jugador():
                self.atacar_jugador(self.jugador)   # Atacar al jugador si está cerca