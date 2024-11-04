# Mapa.py
import pygame

class Mundo:
    def __init__(self, window_width, window_height, background_image_path):
        self.map_tiles = []
        self.window_width = window_width
        self.window_height = window_height

        # Load and scale the background image
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))

        # Definir la grilla (0 = espacio libre, 1 = obstáculo)
        self.grilla = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
            
        ]

    def draw(self, surface):
        # Draw the background image
        surface.blit(self.background_image, (0, 0))

        # Draw the grid
        tile_size = self.window_width // len(self.grilla[0])
        for y, row in enumerate(self.grilla):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if tile == 1:
                    pygame.draw.rect(surface, ("#9b7440"), rect)  # Draw obstacles in red
                # pygame.draw.rect(surface, (255, 255, 255), rect, 1)  # Draw grid lines in white