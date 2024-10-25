# Example file showing a circle moving on screen
import pygame
import constantes
import os
from personaje import Personaje
from Enemigos import Enemigo
from Mapa import Mundo


#ESCALAR LA IMAGEN
def scalar_imagen(image,scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image,(w*scale, h*scale))
    return nueva_imagen


#CONTAR ELEMENTOS EN CARPETA
def Contar_elementos(directorio):
    return len(os.listdir(directorio))
#LISTAR NOMBRES DE LAS CARPETAS

def name_carpeta(directorio):
    return os.listdir(directorio)



# pygame setup
pygame.init()
reloj = pygame.time.Clock()

screen = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))


Mover_derecha = False
Mover_izquierda = False
Mover_arriba = False
Mover_abajo = False

running = True
pygame.display.set_caption("Mi primer Juego")





# Función para dibujar el mapa con colores
# Función para dibujar la cuadrícula
# Función para dibujar la grid del mapa con líneas
def dibujar_grid():
    
      # Dibujar las líneas verticales
    for x in range(30):  # +1 para dibujar la última línea
        pygame.draw.line(screen, constantes.COLOR_LINEA, (x*constantes.Tile_Size, 0), (x*constantes.Tile_Size, constantes.HEIGHT))  # Línea vertical
        pygame.draw.line(screen, constantes.COLOR_LINEA, (0 ,x *constantes.Tile_Size), (constantes.WIDTH, x*40 ))  # Línea horizontal




#FUNCION PARA CARGAR LAS IMAGENES DEL MUNDO
# FUNCION PARA CARGAR LAS IMAGENES DEL MUNDO
tile_list = []

for x in range(constantes.Tiles_Type):
    tile_image = pygame.image.load(f"Assets/Tiles/Tile ({x+1}).png")
    # Corregido a solo dos dimensiones (ancho y alto)
    tile_image = pygame.transform.scale(tile_image, (constantes.Tile_Size, constantes.Tile_Size))
    tile_list.append(tile_image)

world_data = [
    [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 16, 8, 8, 8, 8, 8, 18, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11],
    [16, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,  11]
]

world = Mundo()
world.proceso_datos(world_data, tile_list)














#Vida del Jugador principal



#ANIMACION DEL PERSONAJE
animaciones = []
for i in range (7):
     img = pygame.image.load(f"Assets//Walk//{i}.png")
     img =scalar_imagen(img,constantes.Scala_personaje)
     animaciones.append(img)
     
#ANIMACION DE ATAQUE
animaciones_ataque = []
for enemigos in range(3):  # Suponiendo que tienes 5 frames de ataque
    img_ataque = pygame.image.load(f"Assets/Attack_3/{enemigos}.png")
    img_ataque = scalar_imagen(img_ataque, constantes.Scala_personaje)
    animaciones_ataque.append(img_ataque)

#Animacion DEL ENEMIGO
animaciones_enemigo =[]
for a_enemigo in range(7):
    img_enemigo = pygame.image.load(f"Assets/Enemy/Cavalier/{a_enemigo}.png")
    img_enemigo = scalar_imagen(img_enemigo, constantes.Escalar_enemigos)
    animaciones_enemigo.append(img_enemigo)

#ANIMACION DEL LANZADOR
animaciones_enemigo2 =[]
for a_enemigo in range(7):
    img_enemigo2 = pygame.image.load(f"Assets/Enemy/Lanzador/{a_enemigo}.png")
    img_enemigo2 = scalar_imagen(img_enemigo2, constantes.Escalar_enemigos)
    animaciones_enemigo2.append(img_enemigo2)

   
    
    
#CREAR JUGADOR
Jugador = Personaje(70, 70, animaciones, animaciones_ataque)


#Creando ENEMIGOS
cavalier = Enemigo(300, 400, animaciones_enemigo)


Lanzador = Enemigo(100, 250, animaciones_enemigo2 )



while running:
    # FRAME A 60 FPS
    reloj.tick(60)
    
    



    # MOVIMIENTO DEL JUGADOR
    posicion_x = 0
    posicion_y = 0

    # Actualiza las posiciones dependiendo de las teclas presionadas
    if Mover_derecha:
        posicion_x = constantes.Velocidad_Personaje
    if Mover_izquierda:
        posicion_x = -constantes.Velocidad_Personaje
    if Mover_arriba:
        posicion_y = -constantes.Velocidad_Personaje
    if Mover_abajo:
        posicion_y = constantes.Velocidad_Personaje
        
    # Actualiza los frames de los personajes y enemigos
    Jugador.Update_Frame()
    cavalier.Update_Frame()
    Lanzador.Update_Frame()

    # Control del jugador en los ejes X e Y
    Jugador.movimiento(posicion_x, posicion_y)
   
        # Detectar colisiones y daño
    if Jugador.atacando:
        Jugador.atacar(cavalier)
        Jugador.atacar(Lanzador)


    # Detectar colisiones y ajustar el movimiento
    if Jugador.forma.colliderect(cavalier.forma):
        print("¡Colisión con Cavalier!")
        if posicion_x > 0:  # Se mueve hacia la derecha
            Jugador.forma.right = cavalier.forma.left
        elif posicion_x < 0:  # Se mueve hacia la izquierda
            Jugador.forma.left = cavalier.forma.right
        if posicion_y > 0:  # Se mueve hacia abajo
            Jugador.forma.bottom = cavalier.forma.top
        elif posicion_y < 0:  # Se mueve hacia arriba
            Jugador.forma.top = cavalier.forma.bottom

    if Jugador.forma.colliderect(Lanzador.forma):
        print("¡Colisión con Lanzador!")
        if posicion_x > 0:  # Se mueve hacia la derecha
            Jugador.forma.right = Lanzador.forma.left
        elif posicion_x < 0:  # Se mueve hacia la izquierda
            Jugador.forma.left = Lanzador.forma.right
        if posicion_y > 0:  # Se mueve hacia abajo
            Jugador.forma.bottom = Lanzador.forma.top
        elif posicion_y < 0:  # Se mueve hacia arriba
            Jugador.forma.top = Lanzador.forma.bottom
            

    # Dibujar elementos en pantalla
    world.draw(screen)
    Jugador.dibujar(screen)
    cavalier.dibujar(screen)
    Lanzador.dibujar(screen)
    dibujar_grid()
    
    
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Mover_arriba = True
            if event.key == pygame.K_DOWN:
                Mover_abajo = True
            if event.key == pygame.K_LEFT:
                Mover_izquierda = True
            if event.key == pygame.K_RIGHT:
                Mover_derecha = True
            if event.key == pygame.K_a:  # Tecla de ataque
                Jugador.atacando = True
                Jugador.frame_index = 0
                            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                Mover_arriba = False
            if event.key == pygame.K_DOWN:
                Mover_abajo = False
            if event.key == pygame.K_LEFT:
                Mover_izquierda = False
            if event.key == pygame.K_RIGHT:
                Mover_derecha = False

    # Actualizar la pantalla
    pygame.display.update()
    screen.fill((0, 0, 0))  # Limpiamos la pantalla
    
pygame.quit()