import pygame


class Mundo():
    def __init__(self, window_width, window_height, background_image_path):
        self.map_tiles = []
        self.window_width = window_width
        self.window_height = window_height

        # Load and scale the background image
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.window_width, self.window_height))

    def proceso_datos(self, data, tile_list):
        self.level_length = len(data)
        num_rows = len(data)
        num_cols = len(data[0]) if num_rows > 0 else 0

        # Calcula el nuevo tamaño de cada tile
        tile_width = self.window_width // num_cols
        tile_height = self.window_height // num_rows

        # contador e iterador de filas y columnas del mapa
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image = pygame.transform.scale(
                    image, (tile_width, tile_height))
                image_rect = image.get_rect()
                image_X = x * tile_width
                image_Y = y * tile_height
                # Asignar las coordenadas correctas
                image_rect.topleft = (image_X, image_Y)
                tile_data = [image, image_rect]
                self.map_tiles.append(tile_data)

    def draw(self, surface):
        # Draw the background image
        surface.blit(self.background_image, (0, 0))

        # Draw the tiles
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
