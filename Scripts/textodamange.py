import pygame.sprite

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = -1  # Velocidad hacia arriba

    def update(self):
        # Movimiento hacia arriba y desvanecimiento
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:  # Si sale de la pantalla, elimínalo
            self.kill()
