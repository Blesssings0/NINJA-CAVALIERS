# main.py
# Autor: [Julio Antonio Solis]
# Matrícula: [22-SISN-2-027]

import pygame
from inicializar import inicializar_juego
from game import manejar_colisiones, dibujar_elementos, manejar_eventos, FuenteVida, manejar_colisiones_fuentes
from personaje import Personaje
from Enemigos import Enemigo
from Mapa import Mundo
import constantes
from Cargar_imagenes import cargar_animaciones

# Tiempo límite en segundos (ajustable)
TIEMPO_LIMITE = 60

def mostrar_pantalla_inicio(screen, background_image):
    screen.blit(background_image, (0, 0))  # Set background image
    font = pygame.font.Font(None, 74)
    boton_inicio = pygame.Rect(constantes.WIDTH // 2 - 100, constantes.HEIGHT // 2 - 50, 200, 50)
    texto_inicio = font.render("Iniciar", True, (255, 255, 255))
    rect_texto_inicio = texto_inicio.get_rect(center=boton_inicio.center)
    
    boton_pausar_musica = pygame.Rect(constantes.WIDTH // 2 - 100, constantes.HEIGHT // 2 + 10, 200, 50)
    texto_pausar_musica = font.render("Pausar Musica", True, (255, 255, 255))
    rect_texto_pausar_musica = texto_pausar_musica.get_rect(center=boton_pausar_musica.center)
    
    pygame.draw.rect(screen, (0, 0, 0), boton_inicio)
    screen.blit(texto_inicio, rect_texto_inicio)
    pygame.draw.rect(screen, (0, 0, 0), boton_pausar_musica)
    screen.blit(texto_pausar_musica, rect_texto_pausar_musica)
    
    pygame.display.flip()
    
    return boton_inicio, boton_pausar_musica

def mostrar_pantalla_game_over(screen):
    screen.fill((0, 0, 0))  # Set background to black
    font = pygame.font.Font(None, 74)
    texto_game_over = font.render("Game Over", True, (255, 0, 0))
    rect_texto_game_over = texto_game_over.get_rect(center=(constantes.WIDTH // 2, constantes.HEIGHT // 2 - 50))
    
    boton_reinicio = pygame.Rect(constantes.WIDTH // 2 - 100, constantes.HEIGHT // 2 + 50, 200, 50)
    texto_reinicio = font.render("Reiniciar", True, (255, 255, 255))
    rect_texto_reinicio = texto_reinicio.get_rect(center=boton_reinicio.center)
    
    screen.blit(texto_game_over, rect_texto_game_over)
    pygame.draw.rect(screen, (0, 0, 0), boton_reinicio)
    screen.blit(texto_reinicio, rect_texto_reinicio)
    
    pygame.display.flip()
    
    return boton_reinicio

def mostrar_pantalla_game_win(screen):
    screen.fill((0, 0, 0))  # Set background to black
    font = pygame.font.Font(None, 64)
    texto_game_win = font.render("Game Win", True, (0, 255, 0))
    rect_texto_game_win = texto_game_win.get_rect(center=(constantes.WIDTH // 2, constantes.HEIGHT // 2 - 50))
    
    boton_reinicio = pygame.Rect(constantes.WIDTH // 2 - 100, constantes.HEIGHT // 2 + 50, 200, 50)
    texto_reinicio = font.render("Reiniciar", True, (255, 255, 255))
    rect_texto_reinicio = texto_reinicio.get_rect(center=boton_reinicio.center)
    
    screen.blit(texto_game_win, rect_texto_game_win)
    pygame.draw.rect(screen, (0, 0, 0), boton_reinicio)
    screen.blit(texto_reinicio, rect_texto_reinicio)
    
    pygame.display.flip()
    
    return boton_reinicio

def cambiar_imagen_fondo(ruta_imagen):
    global background_image
    background_image = pygame.image.load(ruta_imagen)

def reiniciar_juego():
    global screen, background_image, reloj, Jugador, cavalier, Lanzador, Soldier, enemigos, world, fuentes_vida, tiempo_inicio
    screen, background_image, reloj = inicializar_juego()
    (animaciones, animaciones_ataque, animaciones_enemigo, animaciones_ataque_enemigo, 
     animaciones_enemigo2, animaciones_ataque_enemigo2, animaciones_enemigo3, animaciones_ataque_enemigo3) = cargar_animaciones()
    world = Mundo(constantes.WIDTH, constantes.HEIGHT, "Assets/MUNDO/battleground2.png")
    Jugador = Personaje(30, 30, animaciones, animaciones_ataque)
    Jugador.vidas = 15  # Set player lives to 15
    cavalier = Enemigo(170, 125, animaciones_enemigo, animaciones_ataque_enemigo)
    Lanzador = Enemigo(200, 455, animaciones_enemigo2, animaciones_ataque_enemigo2)
    Soldier = Enemigo(480, 600, animaciones_enemigo3, animaciones_ataque_enemigo3)
    for enemigo in [cavalier, Lanzador, Soldier]:
        enemigo.jugador = Jugador
        enemigo.grilla = world.grilla
    enemigos = [cavalier, Lanzador, Soldier]
    fuentes_vida = [FuenteVida(100, 100), FuenteVida(300, 300), FuenteVida(500, 500)]  # Reiniciar fuentes de vida
    tiempo_inicio = pygame.time.get_ticks()  # Reiniciar el tiempo de inicio

def mostrar_tiempo_restante(screen, tiempo_inicio, tiempo_limite):
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000  # Convertir a segundos
    tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)

    font = pygame.font.Font(None, 36)
    texto_tiempo = font.render(f"Tiempo restante: {int(tiempo_restante)}s", True, (255, 255, 255))
    screen.blit(texto_tiempo, (10, 10))

def run_game():
    global screen, background_image, reloj, Jugador, cavalier, Lanzador, Soldier, enemigos, world, fuentes_vida, tiempo_inicio

    # Inicializar el juego
    screen, background_image, reloj = inicializar_juego()

    # Cargar música de fondo
    pygame.mixer.music.load("Assets/Sounds/background_music.mp3")
    pygame.mixer.music.play(-1)  # Reproducir en bucle

    # Cargar animaciones
    (animaciones, animaciones_ataque, animaciones_enemigo, animaciones_ataque_enemigo, 
    animaciones_enemigo2, animaciones_ataque_enemigo2, animaciones_enemigo3, animaciones_ataque_enemigo3) = cargar_animaciones()

    # Inicializar otros elementos del juego
    world = Mundo(constantes.WIDTH, constantes.HEIGHT, "Assets/MUNDO/battleground2.png")
    Jugador = Personaje(30, 30, animaciones, animaciones_ataque)  # Inicializar el jugador
    Jugador.vidas = 15  # Set player lives to 15
    cavalier = Enemigo(170, 125, animaciones_enemigo, animaciones_ataque_enemigo)  # Inicializar el cavalier
    Lanzador = Enemigo(200, 455, animaciones_enemigo2, animaciones_ataque_enemigo2)  # Inicializar el lanzador
    Soldier = Enemigo(480, 600, animaciones_enemigo3, animaciones_ataque_enemigo3)  # Inicializar el soldier6

    # Asignar referencias al jugador y la grilla en los enemigos
    for enemigo in [cavalier, Lanzador, Soldier]:
        enemigo.jugador = Jugador
        enemigo.grilla = world.grilla

    # Inicializar posiciones
    posicion_x = 0  # Inicializar la posición x
    posicion_y = 0  # Inicializar la posición y

    # Inicializar variables de movimiento
    Mover_arriba = Mover_abajo = Mover_izquierda = Mover_derecha = False

    # Lista de enemigos
    enemigos = [cavalier, Lanzador, Soldier]

    # Lista de fuentes de vida
    fuentes_vida = [FuenteVida(100, 100), FuenteVida(300, 300), FuenteVida(670, 450)]

    # Inicializar tiempo de inicio
    tiempo_inicio = pygame.time.get_ticks()

    running = True
    game_over = False
    game_win = False
    game_started = False
    while running:
        if not game_started:
            boton_inicio, boton_pausar_musica = mostrar_pantalla_inicio(screen, background_image)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_inicio.collidepoint(event.pos):
                        game_started = True
                        tiempo_inicio = pygame.time.get_ticks()  # Reiniciar el tiempo de inicio al comenzar el juego
                    elif boton_pausar_musica.collidepoint(event.pos):
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
        elif game_over:
            boton_reinicio = mostrar_pantalla_game_over(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_reinicio.collidepoint(event.pos):
                        reiniciar_juego()
                        game_over = False
                        game_started = True
        elif game_win:
            boton_reinicio = mostrar_pantalla_game_win(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_reinicio.collidepoint(event.pos):
                        reiniciar_juego()
                        game_win = False
                        game_started = True
        else:
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

            # Control del jugador en los ejes X e Y
            Jugador.movimiento(posicion_x, posicion_y, world.grilla)

            # Lógica del juego
            manejar_colisiones(Jugador, enemigos, world, posicion_x, posicion_y)
            manejar_colisiones_fuentes(Jugador, fuentes_vida)
            
            if atacando:
                Jugador.atacar(enemigos)

            # Dibujar elementos
            dibujar_elementos(screen, background_image, world, Jugador, cavalier, Lanzador, Soldier, fuentes_vida)

            # Mostrar tiempo restante
            mostrar_tiempo_restante(screen, tiempo_inicio, TIEMPO_LIMITE)

            # Actualizar frames de animación
            Jugador.Update_Frame()
            for enemigo in enemigos:
                enemigo.Update_Frame()

            # Enemigos buscan camino hacia el jugador y atacan
            for enemigo in enemigos:
                enemigo.actualizar_comportamiento()

            # Verificar si el tiempo límite se ha agotado
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000  # Convertir a segundos
            if tiempo_transcurrido >= TIEMPO_LIMITE:
                game_over = True

            if Jugador.derrotado:
                game_over = True

            # Check if all enemies are defeated
            if all(enemigo.derrotado for enemigo in enemigos):
                game_win = True

            pygame.display.flip()
            reloj.tick(60)

    pygame.quit()