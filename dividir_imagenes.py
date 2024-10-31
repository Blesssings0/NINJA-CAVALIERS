from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen, carpeta_destino, divisiones_columna):
    # Cargar imagen
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size
    
        # Calcular el tamaño de cada tile
        tamano_cuadrado = ancho // divisiones_columna
        divisiones_por_fila = alto // tamano_cuadrado
    
        # Crear carpeta de destino si no existe
        os.makedirs(carpeta_destino, exist_ok=True)
    
        # Dividir y guardar cada tile
        contador = 0
        for i in range(divisiones_por_fila):
            for j in range(divisiones_columna):
                izquierda = j * tamano_cuadrado
                superior = i * tamano_cuadrado
                derecha = izquierda + tamano_cuadrado
                inferior = superior + tamano_cuadrado
                
                # Cortar y guardar el tile
                cuadrado = img.crop((izquierda, superior, derecha, inferior))
                nombre_archivo = f"tile_{contador + 1}.png"
                cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
                contador += 1  # Aumentar el contador después de guardar el tile

# Llamada a la función
dividir_guardar_imagen("Assets/PRUEBITAS/map.png", "Assets/PRUEBITAS/", 10)
