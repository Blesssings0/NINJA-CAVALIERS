# personaje.py
import pygame
import constantes

class Personaje:
    def __init__(self, x, y, animaciones, animaciones_ataque):
        # Inicializa el personaje con su posición, animaciones y estado inicial
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
        # Dibuja el personaje en la pantalla, con la imagen posiblemente volteada
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)

    def Update_Frame(self):
        # Actualiza el frame de animación del personaje
        cooldown_animaciones = 160
        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()  

        if self.atacando:
            # Si el personaje está atacando, usa las animaciones de ataque
            if self.frame_index >= len(self.animaciones_ataque):
                self.frame_index = 0
                self.atacando = False
            self.image = self.animaciones_ataque[self.frame_index]
        else:
            # Si el personaje no está atacando, usa las animaciones normales
            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0
            self.image = self.animaciones[self.frame_index]

    def movimiento(self, posicion_x, posicion_y):
        # Mueve el personaje y ajusta la dirección de la imagen
        if posicion_x < 0:
            self.flip = True
        if posicion_x > 0:
            self.flip = False 
        self.forma.x += posicion_x
        self.forma.y += posicion_y

    def atacar(self, enemigos):
        # Inicia el ataque del personaje y verifica colisiones con enemigos
        self.atacando = True
        for enemigo in enemigos:
            if self.forma.colliderect(enemigo.forma):
                enemigo.recibir_dano(1)