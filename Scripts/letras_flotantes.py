# letras_flotantes.py
import pygame

class LetrasFlotantes(pygame.sprite.Sprite):
    def __init__(self, x, y, texto, color):
        super().__init__()
        self.image = pygame.font.Font(None, 36).render(texto, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = -1  # Velocidad de movimiento hacia arriba
        self.tiempo_vida = 60  # Duración en frames

    def update(self):
        self.rect.y += self.velocidad
        self.tiempo_vida -= 1
        if self.tiempo_vida <= 0:
            self.kill()