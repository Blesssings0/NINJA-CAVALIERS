# utils.py
import os
import pygame

def scalar_imagen(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

def Contar_elementos(directorio):
    return len(os.listdir(directorio))

def name_carpeta(directorio):
    return os.listdir(directorio)