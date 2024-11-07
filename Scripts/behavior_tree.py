# behavior_tree.py
# Autor: [Julio Antonio Solis]
# Matrícula: [22-SISN-2-027]

import pygame

class Node:
    def run(self):
        raise NotImplementedError

class Selector(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        # Ejecuta los nodos hijos hasta que uno tenga éxito
        for child in self.children:
            if child.run():
                return True
        return False

class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        # Ejecuta los nodos hijos hasta que uno falle
        for child in self.children:
            if not child.run():
                return False
        return True

class Action(Node):
    def __init__(self, func):
        self.func = func

    def run(self):
        # Ejecuta la función asociada a la acción
        return self.func()

class Timer(Node):
    def __init__(self, duration, child):
        self.duration = duration
        self.child = child
        self.start_time = None

    def run(self):
        # Ejecuta el nodo hijo después de que el temporizador expire
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.start_time = None
            return self.child.run()
        return False