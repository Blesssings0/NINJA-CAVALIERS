# astar.py
import heapq

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grilla, inicio, objetivo):
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ancho, alto = len(grilla[0]), len(grilla)
    cola = [(0, inicio)]
    costos = {inicio: 0}
    padres = {inicio: None}

    while cola:
        _, actual = heapq.heappop(cola)

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]

        for dx, dy in vecinos:
            vecino = (actual[0] + dx, actual[1] + dy)
            nuevo_costo = costos[actual] + 1

            if 0 <= vecino[0] < ancho and 0 <= vecino[1] < alto and grilla[vecino[1]][vecino[0]] == 0:
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    prioridad = nuevo_costo + heuristica(vecino, objetivo)
                    heapq.heappush(cola, (prioridad, vecino))
                    padres[vecino] = actual

    return None