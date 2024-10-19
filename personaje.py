import pygame
import constantes



class Personaje:
    def __init__(self, x, y, animaciones, animaciones_ataque):
        self.flip = False
        self.animaciones = animaciones
        self.animaciones_ataque = animaciones_ataque
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect( 0, 0, constantes.Ancho_PERSONAJE, constantes.Alto_personaje)
        self.forma.center = (x, y)
        self.atacando = False

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)

    def Update_Frame(self):
        cooldown_animaciones = 100
        if self.atacando:
            self.image = self.animaciones_ataque[self.frame_index]
        else:
            self.image = self.animaciones[self.frame_index]

        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()  

        if self.atacando and self.frame_index >= len(self.animaciones_ataque):
            self.frame_index = 0
            self.atacando = False
        elif not self.atacando and self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def movimiento (self, posicion_x, posicion_y):
        if posicion_x < 0:
            self.flip = True
        if posicion_x > 0:
            self.flip = False 
        self.forma.x = self.forma.x + posicion_x
        self.forma.y = self.forma.y + posicion_y

    # Método para atacar a los enemigos
    def atacar(self, enemigo):
        if self.atacando | self.forma.colliderect(enemigo.forma):
            enemigo.recibir_dano(1)  # Aplica daño de 10 unidades al enemigo


