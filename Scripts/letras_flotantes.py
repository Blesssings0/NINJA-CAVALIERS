# letras_flotantes.py
import pygame

class LetrasFlotantes:
    def __init__(self, x, y, texto, color):
        self.x = x
        self.y = y
        self.texto = texto
        self.color = color
        self.font = pygame.font.Font(None, 36)  # Puedes ajustar la fuente y el tamaño
        self.image = self.font.render(self.texto, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.velocidad = -5  # Velocidad de movimiento hacia arriba
        self.tiempo_vida = 20  # Duración en frames

    def actualizar(self):
        self.rect.y += self.velocidad
        self.tiempo_vida -= 1

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)

    def ha_terminado(self):
        return self.tiempo_vida <= 0