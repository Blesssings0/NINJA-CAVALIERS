# Coliciones.py
def manejar_colisiones(Jugador, cavalier, Lanzador, Soldier, posicion_x, posicion_y):
    separar_objetos(Jugador, cavalier)
    separar_objetos(Jugador, Lanzador)
    separar_objetos(Jugador, Soldier)

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