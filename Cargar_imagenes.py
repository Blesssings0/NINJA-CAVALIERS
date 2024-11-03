# cargar_animaciones.py
import pygame
from utils import scalar_imagen
import constantes

def cargar_imagenes(ruta, cantidad, escala):
    imagenes = []
    for i in range(cantidad):
        imagen = pygame.image.load(f"{ruta}/{i}.png").convert_alpha()
        imagen = scalar_imagen(imagen, escala)
        imagenes.append(imagen)
    return imagenes

def cargar_animaciones():
        # ANIMACION DEL PERSONAJE
    animaciones = []
    for i in range(7):
        img = pygame.image.load(f"Assets//Walk//{i}.png")
        img = scalar_imagen(img, constantes.Scala_personaje)
        animaciones.append(img)

    # ANIMACION DE ATAQUE
    animaciones_ataque = []
    for enemigos in range(3):  # Suponiendo que tienes 5 frames de ataque
        img_ataque = pygame.image.load(f"Assets/Attack_3/{enemigos}.png")
        img_ataque = scalar_imagen(img_ataque, constantes.Scala_personaje)
        animaciones_ataque.append(img_ataque)

    # Animacion DEL ENEMIGO
    animaciones_enemigo = []
    for a_enemigo in range(7):
        img_enemigo = pygame.image.load(f"Assets/Enemy/Cavalier/{a_enemigo}.png")
        img_enemigo = scalar_imagen(img_enemigo, constantes.Escalar_enemigos)
        animaciones_enemigo.append(img_enemigo)

    # ANIMACION DEL LANZADOR
    animaciones_enemigo2 = []
    for a_enemigo in range(7):
        img_enemigo2 = pygame.image.load(f"Assets/Enemy/Lanzador/{a_enemigo}.png")
        img_enemigo2 = scalar_imagen(img_enemigo2, constantes.Escalar_enemigos)
        animaciones_enemigo2.append(img_enemigo2)

    animaciones_enemigo3 = []
    for soldier in range(6):
        img_enemigo3 = pygame.image.load(f"Assets/Enemy/Soldier/{soldier + 1}.png")
        img_enemigo3 = scalar_imagen(img_enemigo3, constantes.Escalar_enemigos)
        animaciones_enemigo3.append(img_enemigo3)

    return animaciones, animaciones_ataque, animaciones_enemigo, animaciones_enemigo2, animaciones_enemigo3