#Metodo de Straight merging


# 'heapq' nos da la funcionalidad de Min-Heap.
# Es crucial para mezclar K archivos eficientemente.
import heapq 

#'os' nos permite crear y eliminar archivos y carpetas.
import os 

# 'random' lo usaremos solo para crear nuestro archivo de datos gigante de ejemplo.
import random 

# --- Constantes de Simulación ---

# El nombre de nuestro archivo gigante de entrada (simulado).
INPUT_FILE = 'datos_gigantes.txt'

# El nombre del archivo final donde quedará todo ordenado.
OUTPUT_FILE = 'datos_ordenados_final.txt'

# El nombre de la carpeta para guardar los tramos intermedios.
TEMP_DIR = 'tramos_temporales'

# ¿Cuántos números caben en nuestra "RAM" simulada?
# En un caso real, esto serían millones, pero para el ejemplo usamos 10.
TAMANO_RAM = 10 

# ¿Cuántos números vamos a generar para el archivo de entrada?
TOTAL_NUMEROS = 50 

# --- FASE 1: Creación de Tramos (Sort) ---
# Esta función lee pedazos de "datos_gigantes.txt", los ordena en RAM y los escribe en archivos temporales dentro de la carpeta "tramos_temporales".

def crear_tramos_iniciales():
    
    # Imprime un mensaje para saber en qué fase estamos.
    print(f"--- FASE 1: Creando tramos iniciales (RAM = {TAMANO_RAM} elementos) ---")
    
    # Crea la carpeta de tramos temporales si no existe.
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Una lista para guardar los nombres de los archivos de tramo que creemos.
    nombres_tramos = [] # <- La variable se define correctamente aquí
    
    # 'numero_tramo' es un contador para nombrar los archivos (tramo_0.txt, tramo_1.txt...).
    numero_tramo = 0
    
    # Abre el archivo de entrada gigante para leerlo ("r").
    with open(INPUT_FILE, 'r') as f_in:
        
        # Un bucle 'while True' que se romperá cuando leamos todo el archivo.
        while True:
            
            # 'pedazo_ram' simula nuestra memoria RAM.
            # Leemos 'TAMANO_RAM' líneas del archivo de entrada.
            pedazo_ram = [f_in.readline() for _ in range(TAMANO_RAM)]
            
            # Filtramos líneas vacías (que pueden ocurrir al final del archivo).
            pedazo_ram = [line.strip() for line in pedazo_ram if line.strip()]
            
            # Si el pedazo está vacío (llegamos al final del archivo), rompemos el bucle.
            if not pedazo_ram:
                break
                
            # Convertimos los números (que se leyeron como texto) a enteros.
            pedazo_ram_numeros = [int(num) for num in pedazo_ram]
            
        
            # Usamos un algoritmo interno para ordenar el pedazo que sí cabe en nuestra "RAM".
            pedazo_ram_numeros.sort()
            
            # Creamos el nombre del archivo para este tramo.
            nombre_tramo = os.path.join(TEMP_DIR, f'tramo_{numero_tramo}.txt')
            
            # Abrimos el nuevo archivo de tramo para escribir ("w").
            with open(nombre_tramo, 'w') as f_tramo:
                
                # Escribimos cada número ordenado en el archivo de tramo.
                for num in pedazo_ram_numeros:
                    f_tramo.write(f"{num}\n")
                    
            nombres_tramos.append(nombre_tramo)
            
            # Imprimimos progreso.
            print(f"  -> Creado '{nombre_tramo}' con {len(pedazo_ram_numeros)} elementos.")
            
            # Incrementamos el contador para el siguiente tramo.
            numero_tramo += 1
            
    # La función devuelve la lista con todos los nombres de tramos que creó.
    return nombres_tramos

# Esta es la función "Straight Merging".
# Recibe la lista de tramos ordenados y los mezcla en un solo archivo de salida.

def straight_k_way_merge(archivos_tramos, archivo_salida):
    
    # Imprime un mensaje para saber que empezamos la Fase 2.
    print(f"\n--- FASE 2: Iniciando Mezcla Directa (K-Way Merge) de {len(archivos_tramos)} tramos ---")
    
    # 'min_heap' es nuestra cola de prioridad (Min-Heap).
    # Almacenará tuplas: (valor, indice_del_archivo)
    min_heap = []
    
    # 'archivos_abiertos' es una lista para mantener "abiertos" todos los archivos de tramo que vamos a leer.
    archivos_abiertos = []
    
    try:
        # --- Inicialización ---
        # Abrimos todos los archivos de tramo.
        for i, nombre_tramo in enumerate(archivos_tramos):
            
            # Abre el archivo de tramo 'i' para leerlo ("r").
            f = open(nombre_tramo, 'r')
            
            # Lo añadimos a nuestra lista de archivos abiertos.
            archivos_abiertos.append(f)
            
            # Leemos la PRIMERA línea (el primer número) del archivo.
            linea = f.readline().strip()
            
            # Si la línea no está vacía...
            if linea:
                # Convertimos el valor a entero.
                valor = int(linea)
                
                # --- ¡El corazón del K-Way Merge! ---
                # Añadimos (push) al heap una tupla.
                # El heap se ordenará automáticamente por el 'valor'.
                # 'i' es el índice que nos dice de qué archivo (tramo) vino este valor.
                heapq.heappush(min_heap, (valor, i))
                
        # --- Bucle Principal de Mezcla ---
        # Abrimos el archivo de salida final para escribir ("w").
        with open(archivo_salida, 'w') as f_out:
            
            # El bucle se ejecuta mientras nuestro heap tenga elementos.
            # (Cuando el heap esté vacío, significa que procesamos todos los tramos).
            while min_heap:
                
                # --- 1. Extraer el Mínimo ---
                # Hacemos 'pop' del heap. Esto NOS DA el elemento
                # MÁS PEQUEÑO de todos los elementos que están
                # en la "cabeza" de todos los archivos de tramo.
                valor_minimo, indice_archivo = heapq.heappop(min_heap)
                
                # --- 2. Escribir en Salida ---
                # Escribimos ese valor mínimo en el archivo de salida final.
                f_out.write(f"{valor_minimo}\n")
                
                # --- 3. Recargar el Heap ---
                # Ahora, debemos leer el SIGUIENTE elemento del MISMO archivo
                # de donde sacamos el 'valor_minimo'.
                
                # Obtenemos el manejador del archivo usando el 'indice_archivo'.
                f_siguiente = archivos_abiertos[indice_archivo]
                
                # Leemos la siguiente línea de ese archivo.
                linea_siguiente = f_siguiente.readline().strip()
                
                # Si esa línea existe (el archivo de tramo aún no se acaba)...
                if linea_siguiente:
                    
                    # Convertimos el valor a entero.
                    valor_siguiente = int(linea_siguiente)
                    
                    # Añadimos (push) el nuevo valor (y su índice de archivo) al heap.
                    # El heap se re-ordenará solo, encontrando el nuevo mínimo.
                    heapq.heappush(min_heap, (valor_siguiente, indice_archivo))
                    
        print(f"--- ¡Mezcla completada! Resultado en '{archivo_salida}' ---")

    finally:
        # Aseguramos que TODOS los archivos de tramo que abrimos se cierren.
        print("\n--- Limpieza: Cerrando archivos de tramos ---")
        for f in archivos_abiertos:
            f.close()


def crear_archivo_gigante_ejemplo():
    # Esta función solo crea el archivo de entrada para simular.
    print(f"--- Preparación: Creando '{INPUT_FILE}' con {TOTAL_NUMEROS} números... ---")
    with open(INPUT_FILE, 'w') as f:
        for _ in range(TOTAL_NUMEROS):
            # Escribe números aleatorios entre 1 y 1000.
            f.write(f"{random.randint(1, 1000)}\n")

def limpiar_archivos_temporales(archivos_tramos):
    # Esta función borra todos los archivos .tmp y la carpeta.
    print(f"--- Limpieza: Borrando {len(archivos_tramos)} archivos de tramo... ---")
    for nombre_tramo in archivos_tramos:
        os.remove(nombre_tramo) # Borra el archivo
    os.rmdir(TEMP_DIR) # Borra la carpeta
    print("--- Limpieza completada. ---")


if __name__ == "__main__":
    
    # 1. Creamos el archivo de datos de entrada.
    crear_archivo_gigante_ejemplo()
    
    # 2. FASE 1: Ordenar los pedazos en RAM y crear los tramos en disco.
    lista_de_tramos = crear_tramos_iniciales()
    
    # 3. FASE 2: Mezclar todos los tramos en el archivo de salida final.
    straight_k_way_merge(lista_de_tramos, OUTPUT_FILE)
    
    # 4. Borrar los archivos temporales que creamos.
    limpiar_archivos_temporales(lista_de_tramos)