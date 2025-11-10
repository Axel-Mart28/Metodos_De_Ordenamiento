# Algoritmo de Natural Merging
import heapq 
import os 
import random 

INPUT_FILE = 'datos_gigantes.txt'
OUTPUT_FILE = 'datos_ordenados_final.txt'
TEMP_DIR = 'tramos_temporales'
TAMANO_RAM = 10 
TOTAL_NUMEROS = 50 

# Esta función implementa "Natural Merging" usando la técnica de Selección por Reemplazo con un heap.


def crear_tramos_iniciales():
    
    # Imprime un mensaje para saber en qué fase estamos.
    print(f"--- FASE 1: Creando tramos (Natural Merging / Replacement Selection) ---")
    
    # Crea la carpeta de tramos temporales si no existe.
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Una lista para guardar los nombres de los archivos de tramo que creemos.
    nombres_tramos = []
    
    # 'numero_tramo' es un contador para nombrar los archivos (tramo_0.txt, tramo_1.txt...).
    numero_tramo = 0
    
    # 'heap_primario' simula nuestra RAM. Es un Min-Heap.
    heap_primario = []
    
    # 'heap_secundario' es donde "apartamos" los números que son mas pequeños que el último que escribimos, para usarlos en el PRÓXIMO tramo.
    heap_secundario = []
    
    # Abrimos el archivo de entrada gigante para leerlo ("r").
    try:
        f_in = open(INPUT_FILE, 'r')
        
        # --- Llenado inicial de la RAM (heap_primario) ---
        # Leemos los primeros 'TAMANO_RAM' números del archivo.
        for _ in range(TAMANO_RAM):
            linea = f_in.readline().strip()
            if linea:
                heap_primario.append(int(linea))
            else:
                break # El archivo era más pequeño que la RAM
                
        # Convertimos la lista 'heap_primario' en un Min-Heap.
        heapq.heapify(heap_primario)
        
        # --- Bucle Principal de Creación de Tramos ---
        # Continuaremos mientras el heap primario (RAM) o el secundario tengan datos.
        while heap_primario:
            
            # --- Iniciar un nuevo tramo ---
            # Creamos el nombre del archivo para este nuevo tramo.
            nombre_tramo = os.path.join(TEMP_DIR, f'tramo_{numero_tramo}.txt')
            
            # Añadimos el nombre de este nuevo archivo a nuestra lista.
            nombres_tramos.append(nombre_tramo)
            
            # Abrimos el nuevo archivo de tramo para escribir ("w").
            f_out = open(nombre_tramo, 'w')
            
            print(f"  -> Creando '{nombre_tramo}'...")
            
            # 'ultimo_valor_escrito' guarda el último número que escribimos en el tramo actual. Es -infinito al inicio de cada tramo.
            ultimo_valor_escrito = float('-inf')
            
            # --- Bucle Interno (Llenar el tramo actual) ---
            # Mientras el heap primario tenga elementos, los procesamos.
            while heap_primario:
                
                # 1. Sacamos el valor MÁS PEQUEÑO del heap (la raíz).
                valor_minimo = heapq.heappop(heap_primario)
                
                # 2. Escribimos este valor en el archivo de tramo actual.
                f_out.write(f"{valor_minimo}\n")
                
                # Actualizamos el último valor que escribimos.
                ultimo_valor_escrito = valor_minimo
                
                # 3. Leer el SIGUIENTE número del archivo de entrada
                linea_nueva = f_in.readline().strip()
                
                # Si el archivo de entrada aun tiene números...
                if linea_nueva:
                    valor_nuevo = int(linea_nueva)
                    
                    
                    # 4. Comparar el nuevo valor con el que acabamos de escribir.
                    if valor_nuevo >= ultimo_valor_escrito:
                        
                        # Si es mayor o igual, "cabe" en el TRAMO ACTUAL.
                        # Lo añadimos al heap_primario.
                        heapq.heappush(heap_primario, valor_nuevo)
                        
                    else:
                        # Si es más pequeño, romperia el orden del tramo actual.
                        # Lo "apartamos" al heap_secundario para el PRÓXIMO tramo.
                        heap_secundario.append(valor_nuevo)
                
                # Si no hay más líneas (linea_nueva es Falso), simplemente no añadimos nada al heap. El bucle 'while heap_primario' se encargará de vaciar la RAM.
            
            # --- Fin del Bucle Interno ---
            # El 'heap_primario' está vacío. El tramo actual está completo.
            f_out.close() # Cerramos el archivo de tramo
            print(f"  -> Terminado '{nombre_tramo}'.")
            
            # Incrementamos el contador de tramos.
            numero_tramo += 1
            
            # --- Preparar la Siguiente Ronda ---
            # El heap_secundario (los "apartados") se convierte en el nuevo heap_primario para el siguiente tramo.
            heap_primario = heap_secundario
            
            # El heap_secundario se vacía para la nueva ronda.
            heap_secundario = []
            
            # Convertimos la lista en un heap (si tiene elementos)
            if heap_primario:
                heapq.heapify(heap_primario)
                
        # --- Fin del Bucle Principal ---
        # 'heap_primario' y 'heap_secundario' están vacíos.
        # Todos los datos han sido escritos en tramos.
        
    finally:
        # Aseguramos que el archivo de entrada se cierre.
        f_in.close()
            
    # La función devuelve la lista con todos los nombres de tramos que creo.
    return nombres_tramos


def straight_k_way_merge(archivos_tramos, archivo_salida):
    
    # Imprime un mensaje para saber que empezamos la Fase 2.
    print(f"\n--- FASE 2: Iniciando Mezcla Directa (K-Way Merge) de {len(archivos_tramos)} tramos ---")
    
    # 'min_heap' es nuestra cola de prioridad (Min-Heap).
    min_heap = []
    
    # 'archivos_abiertos' es una lista para mantener "abiertos"
    # todos los archivos de tramo que vamos a leer.
    archivos_abiertos = []
    
    try:
        # --- Inicialización ---
        for i, nombre_tramo in enumerate(archivos_tramos):
            f = open(nombre_tramo, 'r')
            archivos_abiertos.append(f)
            linea = f.readline().strip()
            if linea:
                valor = int(linea)
                heapq.heappush(min_heap, (valor, i))
                
        # --- Bucle Principal de Mezcla ---
        with open(archivo_salida, 'w') as f_out:
            while min_heap:
                
                # 1. Extraer el Mínimo
                valor_minimo, indice_archivo = heapq.heappop(min_heap)
                
                # 2. Escribir en Salida
                f_out.write(f"{valor_minimo}\n")
                
                # 3. Recargar el Heap
                f_siguiente = archivos_abiertos[indice_archivo]
                linea_siguiente = f_siguiente.readline().strip()
                
                if linea_siguiente:
                    valor_siguiente = int(linea_siguiente)
                    heapq.heappush(min_heap, (valor_siguiente, indice_archivo))
                    
        print(f"---Mezcla completada Resultado en '{archivo_salida}' ---")

    finally:
        # --- Limpieza ---
        print("\n--- Limpieza: Cerrando archivos de tramos ---")
        for f in archivos_abiertos:
            f.close()



def crear_archivo_gigante_ejemplo():
    # Esta función solo crea el archivo de entrada para simular.
    print(f"--- Preparación: Creando '{INPUT_FILE}' con {TOTAL_NUMEROS} números... ---")
    with open(INPUT_FILE, 'w') as f:
        for _ in range(TOTAL_NUMEROS):
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
    
    # 2. FASE 1: (Ahora usa Natural Merging)
    lista_de_tramos = crear_tramos_iniciales()
    
    # 3. FASE 2: (Usa el mismo K-Way Merge)
    straight_k_way_merge(lista_de_tramos, OUTPUT_FILE)
    
    limpiar_archivos_temporales(lista_de_tramos)