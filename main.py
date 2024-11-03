# main.py
import pygame
from inicializar import inicializar_juego
from game import manejar_colisiones, dibujar_elementos, manejar_eventos
from personaje import Personaje
from Enemigos import Enemigo
from Mapa import Mundo
import constantes
from Cargar_imagenes import cargar_animaciones

# Inicializar el juego
screen, background_image, reloj = inicializar_juego()

# Cargar animaciones
animaciones, animaciones_ataque, animaciones_enemigo, animaciones_enemigo2, animaciones_enemigo3 = cargar_animaciones()

# Inicializar otros elementos del juego
world = Mundo(constantes.WIDTH, constantes.HEIGHT, "Assets/MUNDO/battleground2.png")
Jugador = Personaje(100, 100, animaciones, animaciones_ataque)  # Inicializar el jugador
cavalier = Enemigo(200, 200, animaciones_enemigo)  # Inicializar el cavalier
Lanzador = Enemigo(300, 300, animaciones_enemigo2)  # Inicializar el lanzador
Soldier = Enemigo(400, 400, animaciones_enemigo3)  # Inicializar el soldier

# Inicializar posiciones
posicion_x = 0  # Inicializar la posición x
posicion_y = 0  # Inicializar la posición y

# Inicializar variables de movimiento
Mover_arriba = Mover_abajo = Mover_izquierda = Mover_derecha = False

running = True
while running:
    # Manejar eventos
    running, Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, atacando = manejar_eventos(Mover_arriba, Mover_abajo, Mover_izquierda, Mover_derecha, Jugador, [cavalier, Lanzador, Soldier])
    
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
    manejar_colisiones(Jugador, cavalier, Lanzador, Soldier, posicion_x, posicion_y)
    
    # Dibujar elementos
    dibujar_elementos(screen, background_image, world, Jugador, cavalier, Lanzador, Soldier)

    # Actualizar frames de animación
    Jugador.Update_Frame()
    cavalier.Update_Frame()
    Soldier.Update_Frame()
    Lanzador.Update_Frame()

    # Control del jugador en los ejes X e Y
    Jugador.movimiento(posicion_x, posicion_y)

    # Manejar ataque
    if atacando:
        Jugador.atacar([cavalier, Lanzador, Soldier])

    # Enemigos buscan camino hacia el jugador
    cavalier.buscar_camino(world.grilla, Jugador.forma.center)
    Lanzador.buscar_camino(world.grilla, Jugador.forma.center)
    Soldier.buscar_camino(world.grilla, Jugador.forma.center)

    # Enemigos siguen el camino
    cavalier.seguir_camino()
    Lanzador.seguir_camino()
    Soldier.seguir_camino()

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()