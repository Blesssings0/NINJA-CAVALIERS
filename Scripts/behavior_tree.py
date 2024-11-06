import pygame

# behavior_tree.py

class Node:
    def run(self):
        raise NotImplementedError

class Selector(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        for child in self.children:
            if child.run():
                return True
        return False

class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        for child in self.children:
            if not child.run():
                return False
        return True

class Action(Node):
    def __init__(self, func):
        self.func = func

    def run(self):
        return self.func()

class Timer(Node):
    def __init__(self, duration, child):
        self.duration = duration
        self.child = child
        self.start_time = None

    def run(self):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.start_time = None
            return self.child.run()
        return False