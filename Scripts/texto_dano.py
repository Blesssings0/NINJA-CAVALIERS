# texto_dano.py
import pygame

class TextoDano:
    def __init__(self, x, y, cantidad):
        self.font = pygame.font.Font(None, 36)  # Puedes cambiar la fuente y el tamaño según sea necesario
        self.image = self.font.render(str(cantidad), True, (255, 0, 0))  # Texto en color rojo
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = -1  # Velocidad a la que el texto se moverá hacia arriba
        self.tiempo_vida = 60  # Tiempo de vida del texto en frames

    def update(self):
        self.rect.y += self.velocidad
        self.tiempo_vida -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)