import pygame
import constantes



class Enemigo:
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, constantes.Alto_ENEMIGO, constantes.Ancho_ENEMIGO)
        self.forma.center = (x, y)
        self.salud = 100  # Agregamos la salud

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)

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

    # Método para recibir daño
    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            print("¡Enemigo derrotado!")
