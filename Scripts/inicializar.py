# inicializar.py
import pygame
import constantes

def inicializar_juego():
    pygame.init()
    reloj = pygame.time.Clock()
    screen = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
    background_image = pygame.image.load("Assets/MUNDO/Battleground2.png")
    background_image = pygame.transform.scale(background_image, (constantes.WIDTH, constantes.HEIGHT))
    return screen, background_image, reloj