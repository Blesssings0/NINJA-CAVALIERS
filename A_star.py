class A_S:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.g = 0  # Costo desde el inicio hasta este nodo
        self.h = 0  # Heurística (distancia estimada hasta el objetivo)
        self.f = 0  # Costo total

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Distancia Manhattan

def astar(mapa, inicio, objetivo):
    open_list = []
    closed_list = []

    nodo_inicio = Nodo(inicio)
    nodo_objetivo = Nodo(objetivo)

    open_list.append(nodo_inicio)

    while open_list:
        nodo_actual = min(open_list, key=lambda o: o.f)
        open_list.remove(nodo_actual)
        closed_list.append(nodo_actual)

        if nodo_actual.posicion == nodo_objetivo.posicion:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1]  # Devuelve el camino desde el inicio hasta el objetivo

        # Generar vecinos
        for movimiento in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Arriba, Abajo, Izquierda, Derecha
            posicion_vecino = (nodo_actual.posicion[0] + movimiento[0], nodo_actual.posicion[1] + movimiento[1])

            # Verificar límites del mapa y si el nodo ya está en la lista cerrada
            if (0 <= posicion_vecino[0] < len(mapa) and
                    0 <= posicion_vecino[1] < len(mapa[0]) and
                    mapa[posicion_vecino[1]][posicion_vecino[0]] != 1 and  # 1 es un obstáculo
                    posicion_vecino not in [nodo.posicion for nodo in closed_list]):

                vecino = Nodo(posicion_vecino, nodo_actual)

                # Calcular costos g, h y f
                vecino.g = nodo_actual.g + 1
                vecino.h = heuristica(vecino.posicion, nodo_objetivo.posicion)
                vecino.f = vecino.g + vecino.h

                # Verificar si el vecino está en la lista abierta
                if vecino not in open_list:
                    open_list.append(vecino)

    return []  # Si no se encuentra un camino
