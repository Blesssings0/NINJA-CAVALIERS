# Coliciones.py
import pygame
import constantes

def manejar_colisiones(Jugador, cavalier, Lanzador, Soldier, world, posicion_x, posicion_y):
    separar_objetos(Jugador, cavalier)
    separar_objetos(Jugador, Lanzador)
    separar_objetos(Jugador, Soldier)
    manejar_colisiones_obstaculos(Jugador, world.grilla, posicion_x, posicion_y)

def separar_objetos(Jugador, objeto):
    # Empuja al jugador fuera del objeto en caso de colisión
    if Jugador.forma.colliderect(objeto.forma):
        dx = (Jugador.forma.centerx - objeto.forma.centerx)
        dy = (Jugador.forma.centery - objeto.forma.centery)
        if abs(dx) > abs(dy):
            if dx > 0:
                Jugador.forma.left = objeto.forma.right
            else:
                Jugador.forma.right = objeto.forma.left
        else:
            if dy > 0:
                Jugador.forma.top = objeto.forma.bottom
            else:
                Jugador.forma.bottom = objeto.forma.top

def manejar_colisiones_obstaculos(Jugador, grilla, posicion_x, posicion_y):
    tile_size = constantes.Tile_Size
    jugador_rect = Jugador.forma.copy()
    jugador_rect.x += posicion_x
    jugador_rect.y += posicion_y

    for y, row in enumerate(grilla):
        for x, tile in enumerate(row):
            if tile == 1:
                obstaculo_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if jugador_rect.colliderect(obstaculo_rect):
                    if posicion_x > 0:  # Se mueve hacia la derecha
                        Jugador.forma.right = obstaculo_rect.left
                    elif posicion_x < 0:  # Se mueve hacia la izquierda
                        Jugador.forma.left = obstaculo_rect.right
                    if posicion_y > 0:  # Se mueve hacia abajo
                        Jugador.forma.bottom = obstaculo_rect.top
                    elif posicion_y < 0:  # Se mueve hacia arriba
                        Jugador.forma.top = obstaculo_rect.bottom

def dibujar_colisiones(surface, grilla):
    tile_size = constantes.Tile_Size
    for y, row in enumerate(grilla):
        for x, tile in enumerate(row):
            if tile == 1:
                obstaculo_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(surface, (255, 0, 0), obstaculo_rect, 2)  # Rojo con grosor de 2 píxeles