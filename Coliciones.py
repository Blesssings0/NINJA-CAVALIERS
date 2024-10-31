# Función para ajustar la posición del jugador en caso de colisión
def ajustar_colision(jugador, enemigo):
    if jugador.forma.colliderect(enemigo.forma):
        # Determinar la distancia de colisión en X y Y
        dx = (jugador.forma.centerx - enemigo.forma.centerx)
        dy = (jugador.forma.centery - enemigo.forma.centery)
        
        # La separación mínima necesaria para evitar la colisión
        overlap_x = (jugador.forma.width / 2 + enemigo.forma.width / 2) - abs(dx)
        overlap_y = (jugador.forma.height / 2 + enemigo.forma.height / 2) - abs(dy)

        if overlap_x < overlap_y:  # Colisión más fuerte en X
            if dx > 0:  # Jugador está a la derecha del enemigo
                jugador.forma.right = enemigo.forma.left
            else:  # Jugador está a la izquierda del enemigo
                jugador.forma.left = enemigo.forma.right
        else:  # Colisión más fuerte en Y
            if dy > 0:  # Jugador está por debajo del enemigo
                jugador.forma.bottom = enemigo.forma.top
            else:  # Jugador está por encima del enemigo
                jugador.forma.top = enemigo.forma.bottom
