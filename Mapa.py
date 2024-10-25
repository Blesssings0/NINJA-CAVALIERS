import constantes


class Mundo():
    def __init__(self):
        self.map_tiles = []

    def proceso_datos(self, data, tile_list):
        self.level_length = len(data)

        # contador e iterador de filas y columnas del mapa
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_X = x * constantes.Tile_Size
                image_Y = y * constantes.Tile_Size
                image_rect.topleft = (image_X, image_Y)  # Asignar las coordenadas correctas
                tile_data = [image, image_rect]
                self.map_tiles.append(tile_data)

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])