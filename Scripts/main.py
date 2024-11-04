# main.py
import pygame
from inicializar import inicializar_juego
from game import manejar_colisiones, dibujar_elementos, manejar_eventos
from personaje import Personaje
from Enemigos import Enemigo
from Mapa import Mundo
import constantes
from Cargar_imagenes import cargar_animaciones
from letras_flotantes import LetrasFlotantes

# Inicializar el juego
screen, background_image, reloj = inicializar_juego()

# Cargar animaciones
animaciones, animaciones_ataque, animaciones_enemigo, animaciones_enemigo2, animaciones_enemigo3 = cargar_animaciones()

# Inicializar otros elementos del juego
world = Mundo(constantes.WIDTH, constantes.HEIGHT, "Assets/MUNDO/battleground2.png")
Jugador = Personaje(30, 30, animaciones, animaciones_ataque)  # Inicializar el jugador
cavalier = Enemigo(140, 100, animaciones_enemigo)  # Inicializar el cavalier
Lanzador = Enemigo(300, 455, animaciones_enemigo2)  # Inicializar el lanzador
Soldier = Enemigo(250, 300, animaciones_enemigo3)  # Inicializar el soldier

# Inicializar posiciones
posicion_x = 0  # Inicializar la posición x
posicion_y = 0  # Inicializar la posición y

# Inicializar variables de movimiento
Mover_arriba = Mover_abajo = Mover_izquierda = Mover_derecha = False

# Inicializar letras flotantes
letras_flotantes = []

# Lista de enemigos
enemigos = [cavalier, Lanzador, Soldier]

running = True
while running:
    # Manejar eventos
    running, Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, atacando = manejar_eventos(Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, Jugador, enemigos)
    
    # Actualizar posición del jugador
    posicion_x = 0
    posicion_y = 0
    if Mover_arriba:
        posicion_y -= constantes.Velocidad_Personaje
    if Mover_abajo:
        posicion_y += constantes.Velocidad_Personaje
    if Mover_izquierda:
        posicion_x -= constantes.Velocidad_Personaje
    if Mover_derecha:
        posicion_x += constantes.Velocidad_Personaje

    # Lógica del juego
    manejar_colisiones(Jugador, cavalier, Lanzador, Soldier, world, posicion_x, posicion_y)
    
    # Dibujar elementos
    dibujar_elementos(screen, background_image, world, Jugador, cavalier, Lanzador, Soldier)

    # Actualizar frames de animación
    Jugador.Update_Frame()
    for enemigo in enemigos:
        enemigo.Update_Frame()

    # Control del jugador en los ejes X e Y
    Jugador.movimiento(posicion_x, posicion_y, world.grilla)

    # Manejar ataque
    if atacando:
        Jugador.atacar(enemigos, letras_flotantes)

    # Actualizar y dibujar letras flotantes
    for letra in letras_flotantes[:]:
        letra.actualizar()
        letra.dibujar(screen)
        if letra.ha_terminado():
            letras_flotantes.remove(letra)

    # Enemigos buscan camino hacia el jugador
    for enemigo in enemigos:
        enemigo.perseguir_jugador(world.grilla, Jugador)
        enemigo.seguir_camino()

    # Eliminar enemigos derrotados
    enemigos = [enemigo for enemigo in enemigos if enemigo.forma]

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()