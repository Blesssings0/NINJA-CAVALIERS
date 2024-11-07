# cargar_animaciones.py
import pygame
from utils import scalar_imagen
import constantes

# Función para cargar imágenes desde una ruta específica, escalar y devolver una lista de imágenes
def cargar_imagenes(ruta, cantidad, escala):
    imagenes = []
    for i in range(cantidad):
        imagen = pygame.image.load(f"{ruta}/{i}.png").convert_alpha()
        imagen = scalar_imagen(imagen, escala)
        imagenes.append(imagen)
    return imagenes

# Función para cargar todas las animaciones necesarias
def cargar_animaciones():
    # ANIMACIÓN DEL PERSONAJE
    animaciones = []
    for i in range(7): # tiene 7 frames de ataque
        img = pygame.image.load(f"Assets/Walk/{i}.png")
        img = scalar_imagen(img, constantes.Scala_personaje)
        animaciones.append(img)

    # ANIMACIÓN DE ATAQUE
    animaciones_ataque = []
    for enemigos in range(3):  # tiene 3 frames de ataque
        img_ataque = pygame.image.load(f"Assets/Attack_3/{enemigos}.png")
        img_ataque = scalar_imagen(img_ataque, constantes.Scala_personaje)
        animaciones_ataque.append(img_ataque)

    # ANIMACIÓN DEL ENEMIGO
    animaciones_enemigo = []
    for a_enemigo in range(7):  # tiene 7 frames de ataque
        img_enemigo = pygame.image.load(f"Assets/Enemy/Cavalier/{a_enemigo}.png")
        img_enemigo = scalar_imagen(img_enemigo, constantes.Escalar_enemigos)
        animaciones_enemigo.append(img_enemigo)

    # ANIMACIÓN DE ATAQUE DEL ENEMIGO
    animaciones_ataque_enemigo = []
    for a_enemigo in range(4):  # tiene 4 frames de ataque
        img_ataque_enemigo = pygame.image.load(f"Assets/Enemy/Cavalier/Attack_1/{a_enemigo}.png")
        img_ataque_enemigo = scalar_imagen(img_ataque_enemigo, constantes.Escalar_enemigos)
        animaciones_ataque_enemigo.append(img_ataque_enemigo)

    # ANIMACIÓN DEL LANZADOR
    animaciones_enemigo2 = []
    for a_enemigo in range(7): # tiene 4 frames de ataque
        img_enemigo2 = pygame.image.load(f"Assets/Enemy/Lanzador/{a_enemigo}.png")
        img_enemigo2 = scalar_imagen(img_enemigo2, constantes.Escalar_enemigos)
        animaciones_enemigo2.append(img_enemigo2)

    # ANIMACIÓN DE ATAQUE DEL LANZADOR
    animaciones_ataque_enemigo2 = []
    for a_enemigo in range(4):  # tiene 4 frames de ataque
        img_ataque_enemigo2 = pygame.image.load(f"Assets/Enemy/Lanzador/Attack_2/{a_enemigo}.png")
        img_ataque_enemigo2 = scalar_imagen(img_ataque_enemigo2, constantes.Escalar_enemigos)
        animaciones_ataque_enemigo2.append(img_ataque_enemigo2)

    # ANIMACIÓN DEL SOLDIER
    animaciones_enemigo3 = []
    for soldier in range(6):
        img_enemigo3 = pygame.image.load(f"Assets/Enemy/Soldier/{soldier + 1}.png")
        img_enemigo3 = scalar_imagen(img_enemigo3, constantes.Escalar_enemigos)
        animaciones_enemigo3.append(img_enemigo3)

    # ANIMACIÓN DE ATAQUE DEL SOLDIER
    animaciones_ataque_enemigo3 = []
    for soldier in range(5):  #  tiene 5 frames de ataque
        img_ataque_enemigo3 = pygame.image.load(f"Assets//Enemy//Soldier//Attack_4//Tile ({soldier +1}).png")
        img_ataque_enemigo3 = scalar_imagen(img_ataque_enemigo3, constantes.Escalar_enemigos)
        animaciones_ataque_enemigo3.append(img_ataque_enemigo3)

    return (animaciones, animaciones_ataque, animaciones_enemigo, animaciones_ataque_enemigo, 
            animaciones_enemigo2, animaciones_ataque_enemigo2, animaciones_enemigo3, animaciones_ataque_enemigo3)