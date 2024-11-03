# search_algorithms.py
from collections import deque

def bfs(grilla, inicio, objetivo):
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ancho, alto = len(grilla[0]), len(grilla)
    cola = deque([inicio])
    padres = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]

        for dx, dy in vecinos:
            vecino = (actual[0] + dx, actual[1] + dy)
            if 0 <= vecino[0] < ancho and 0 <= vecino[1] < alto and grilla[vecino[1]][vecino[0]] == 0 and vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)

    return None

def dfs(grilla, inicio, objetivo):
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ancho, alto = len(grilla[0]), len(grilla)
    pila = [inicio]
    padres = {inicio: None}

    while pila:
        actual = pila.pop()

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]

        for dx, dy in vecinos:
            vecino = (actual[0] + dx, actual[1] + dy)
            if 0 <= vecino[0] < ancho and 0 <= vecino[1] < alto and grilla[vecino[1]][vecino[0]] == 0 and vecino not in padres:
                padres[vecino] = actual
                pila.append(vecino)

    return None

def bidirectional_search(grilla, inicio, objetivo):
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ancho, alto = len(grilla[0]), len(grilla)
    cola_inicio = deque([inicio])
    cola_objetivo = deque([objetivo])
    padres_inicio = {inicio: None}
    padres_objetivo = {objetivo: None}

    while cola_inicio and cola_objetivo:
        if cola_inicio:
            actual_inicio = cola_inicio.popleft()
            for dx, dy in vecinos:
                vecino = (actual_inicio[0] + dx, actual_inicio[1] + dy)
                if 0 <= vecino[0] < ancho and 0 <= vecino[1] < alto and grilla[vecino[1]][vecino[0]] == 0 and vecino not in padres_inicio:
                    padres_inicio[vecino] = actual_inicio
                    cola_inicio.append(vecino)
                    if vecino in padres_objetivo:
                        return reconstruir_camino(padres_inicio, padres_objetivo, vecino)

        if cola_objetivo:
            actual_objetivo = cola_objetivo.popleft()
            for dx, dy in vecinos:
                vecino = (actual_objetivo[0] + dx, actual_objetivo[1] + dy)
                if 0 <= vecino[0] < ancho and 0 <= vecino[1] < alto and grilla[vecino[1]][vecino[0]] == 0 and vecino not in padres_objetivo:
                    padres_objetivo[vecino] = actual_objetivo
                    cola_objetivo.append(vecino)
                    if vecino in padres_inicio:
                        return reconstruir_camino(padres_inicio, padres_objetivo, vecino)

    return None

def reconstruir_camino(padres_inicio, padres_objetivo, punto_encuentro):
    camino_inicio = []
    camino_objetivo = []
    actual = punto_encuentro

    while actual:
        camino_inicio.append(actual)
        actual = padres_inicio[actual]

    actual = punto_encuentro
    while actual:
        camino_objetivo.append(actual)
        actual = padres_objetivo[actual]

    return camino_inicio[::-1] + camino_objetivo[1:]