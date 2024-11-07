# inicializar.py
# Autor: [Julio Antonio Solis]
# Matrícula: [22-SISN-2-027]
import pygame
import constantes

def inicializar_juego():
    # Inicializa todos los módulos de Pygame
    pygame.init()
    # Crea un objeto reloj para controlar el tiempo
    reloj = pygame.time.Clock()
    # Configura la pantalla con las dimensiones especificadas en constantes
    screen = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
    # Carga la imagen de fondo
    background_image = pygame.image.load("Assets/MUNDO/Battleground2.png")
    # Escala la imagen de fondo a las dimensiones de la pantalla
    background_image = pygame.transform.scale(background_image, (constantes.WIDTH, constantes.HEIGHT))
    # Retorna la pantalla, la imagen de fondo y el reloj
    return screen, background_image, reloj