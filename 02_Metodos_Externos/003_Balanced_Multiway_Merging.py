#Algoritmo de Balanced Multiway Merginig

import heapq 
import os 
import random 
import shutil # Para borrar carpetas con contenido

# Constantes de Simulación ---
INPUT_FILE = 'datos_gigantes.txt'
OUTPUT_FILE = 'datos_ordenados_final.txt'

# Directorio principal para la simulación
TEMP_DIR = 'simulacion_discos' 

# Simularemos 4 discos (2 de entrada, 2 de salida, que luego intercambian)
NUM_DISCOS = 4

# Tamaño de nuestra "RAM" simulada
TAMANO_RAM = 10 
TOTAL_NUMEROS = 50 

# Esta es la lógica de "Straight Merge" convertida en una función auxiliar. Su unico trabajo es tomar una lista de archivos de entrada y mezclarlos en un solo archivo de salida.

def k_way_merge_simple(archivos_entrada_nombres, archivo_salida_nombre):
    
    # 'min_heap' para encontrar el elemento más pequeño entre todos los archivos
    min_heap = []
    
    # 'archivos_abiertos' para mantener los manejadores de los archivos de entrada
    archivos_abiertos = []
    
    try:
        # --- Inicialización ---
        # Abrimos todos los archivos de entrada
        for i, nombre_tramo in enumerate(archivos_entrada_nombres):
            f = open(nombre_tramo, 'r')
            archivos_abiertos.append(f)
            linea = f.readline().strip()
            if linea:
                valor = int(linea)
                # Guardamos (valor, índice del archivo)
                heapq.heappush(min_heap, (valor, i))
                
        # --- Bucle Principal de Mezcla ---
        with open(archivo_salida_nombre, 'w') as f_out:
            while min_heap:
                
                # 1. Extraer el valor más pequeño
                valor_minimo, indice_archivo = heapq.heappop(min_heap)
                
                # 2. Escribirlo en la salida
                f_out.write(f"{valor_minimo}\n")
                
                # 3. Recargar desde el mismo archivo
                f_siguiente = archivos_abiertos[indice_archivo]
                linea_siguiente = f_siguiente.readline().strip()
                
                if linea_siguiente:
                    valor_siguiente = int(linea_siguiente)
                    heapq.heappush(min_heap, (valor_siguiente, indice_archivo))
                    
    finally:
        # Asegurar que todos los archivos de entrada se cierren
        for f in archivos_abiertos:
            f.close()

# --- FASE 1: Creación de Tramos (Natural Merging) + distribucion Modificada para distribuir los tramos entre 'discos_destino'

def crear_tramos_iniciales_distribuidos(discos_destino):
    
    # 'discos_destino' es una lista de rutas, ej: ['sim/disco_0', 'sim/disco_1']
    num_discos_destino = len(discos_destino)
    
    print(f"--- FASE 1: Creando tramos (Natural Merging) y distribuyendo en {num_discos_destino} discos ---")
    
    # Logica de Natural Merging 
    heap_primario = []
    heap_secundario = []
    
    # 'total_tramos_creados' es un contador general
    total_tramos_creados = 0
    
    try:
        f_in = open(INPUT_FILE, 'r')
        
        # Llenado inicial de la RAM
        for _ in range(TAMANO_RAM):
            linea = f_in.readline().strip()
            if linea:
                heap_primario.append(int(linea))
            else:
                break
        heapq.heapify(heap_primario)
        
        # Bucle Principal de Creación de Tramos
        while heap_primario:
            
            
            # Elegimos el disco de destino de forma rotativa (Round-Robin)
            # ej. 0 % 2 = 0, 1 % 2 = 1, 2 % 2 = 0, 
            indice_disco_actual = total_tramos_creados % num_discos_destino
            disco_actual = discos_destino[indice_disco_actual]
            
            # El nombre del tramo incluye el disco donde vivirá
            nombre_tramo = os.path.join(disco_actual, f'tramo_inicial_{total_tramos_creados}.txt')
            
            f_out = open(nombre_tramo, 'w')
            print(f"  -> Creando '{nombre_tramo}'...")
            
            ultimo_valor_escrito = float('-inf')
            
            # Bucle Interno (Llenar el tramo actual)
            while heap_primario:
                valor_minimo = heapq.heappop(heap_primario)
                f_out.write(f"{valor_minimo}\n")
                ultimo_valor_escrito = valor_minimo
                
                linea_nueva = f_in.readline().strip()
                if linea_nueva:
                    valor_nuevo = int(linea_nueva)
                    if valor_nuevo >= ultimo_valor_escrito:
                        heapq.heappush(heap_primario, valor_nuevo)
                    else:
                        heap_secundario.append(valor_nuevo)
            
            # Fin del tramo actual
            f_out.close()
            total_tramos_creados += 1
            
            # Preparar la siguiente ronda
            heap_primario = heap_secundario
            heap_secundario = []
            if heap_primario:
                heapq.heapify(heap_primario)
                
    finally:
        f_in.close()
            
    # Devuelve el número total de tramos creados.
    return total_tramos_creados

# --- FASE 2: Lógica de Pases de Mezcla Equilibrada ---

def ejecutar_pase_mezcla(discos_in, discos_out, num_pase):
    
    # 'discos_in': lista de rutas de discos de entrada (ej. ['sim/d0', 'sim/d1'])
    # 'discos_out': lista de rutas de discos de salida (ej. ['sim/d2', 'sim/d3'])
    
    print(f"\n--- PASE DE MEZCLA {num_pase} ---")
    print(f"  Leyendo de: {[os.path.basename(d) for d in discos_in]}")
    print(f"  Escribiendo en: {[os.path.basename(d) for d in discos_out]}")
    
    # Recolectamos todos los tramos de los discos de ENTRADA
    # tramos_por_disco[0] = lista de tramos en discos_in[0]
    # tramos_por_disco[1] = lista de tramos en discos_in[1]
    tramos_por_disco = []
    for d in discos_in:
        tramos = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.txt')]
        tramos.sort() # Aseguramos un orden consistente
        tramos_por_disco.append(tramos)
        
    # El número de mezclas que haremos es el max de tramos en cualquier disco
    # (ej. si d0 tiene 5 tramos y d1 tiene 4, haremos 5 mezclas)
    num_mezclas = max(len(t) for t in tramos_por_disco) if tramos_por_disco else 0
    
    # 'num_tramos_creados' es el contador para esta pasada
    num_tramos_creados = 0
    
    # Iteramos 'num_mezclas' veces
    for i in range(num_mezclas):
        
        # Preparamos los archivos que vamos a mezclar en esta iteración
        archivos_para_mezcla_actual = []
        
        # Tomamos el tramo 'i' de CADA disco de entrada (si existe)
        for lista_tramos in tramos_por_disco:
            if i < len(lista_tramos):
                archivos_para_mezcla_actual.append(lista_tramos[i])
                
        # Si no hay archivos (raro, pero por seguridad), saltamos
        if not archivos_para_mezcla_actual:
            continue
            
        # --- Distribución de Salida Equilibrada ---
        # Elegimos el disco de SALIDA de forma rotativa
        indice_disco_salida = num_tramos_creados % len(discos_out)
        disco_salida_actual = discos_out[indice_disco_salida]
        
        # Definimos el nombre del nuevo tramo (más largo)
        nombre_tramo_salida = os.path.join(disco_salida_actual, f'pase_{num_pase}_tramo_{num_tramos_creados}.txt')
        
        # --- Ejecutar la Mezcla ---
        # Llamamos a nuestra función auxiliar de mezcla
        k_way_merge_simple(archivos_para_mezcla_actual, nombre_tramo_salida)
        
        print(f"    -> Mezclados {len(archivos_para_mezcla_actual)} tramos -> '{os.path.basename(nombre_tramo_salida)}'")
        
        num_tramos_creados += 1
        
    # --- Limpieza del Pase ---
    # Una vez que terminamos el pase, borramos los tramos VIEJOS de los discos de ENTRADA
    print(f"  Limpiando tramos antiguos de {[os.path.basename(d) for d in discos_in]}...")
    for d in discos_in:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
            
    # Devolvemos cuántos tramos se crearon en esta pasada.
    return num_tramos_creados

# --- Funciones de Ayuda ---

def crear_archivo_gigante_ejemplo():
    print(f"--- Preparación: Creando '{INPUT_FILE}' con {TOTAL_NUMEROS} números... ---")
    with open(INPUT_FILE, 'w') as f:
        for _ in range(TOTAL_NUMEROS):
            f.write(f"{random.randint(1, 1000)}\n")

def preparar_directorios_discos():
    # Borra la simulación anterior si existe
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        
    # Crea el directorio principal
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Crea las carpetas que simulan cada disco
    lista_discos = []
    for i in range(NUM_DISCOS):
        ruta_disco = os.path.join(TEMP_DIR, f'disco_{i}')
        os.makedirs(ruta_disco, exist_ok=True)
        lista_discos.append(ruta_disco)
        
    print(f"--- Preparación: Simulando {NUM_DISCOS} discos en '{TEMP_DIR}' ---")
    return lista_discos
    
def limpiar_todo():
    # Limpia todos los archivos y carpetas de la simulación
    print(f"\n--- Limpieza: Borrando '{INPUT_FILE}', '{OUTPUT_FILE}' y '{TEMP_DIR}' ---")
    if os.path.exists(INPUT_FILE):
        os.remove(INPUT_FILE)
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR) # Borra la carpeta y todo su contenido
    print("--- Limpieza completada. ---")

# --- Ejecución Principal del Script ---
if __name__ == "__main__":
    
    try:
        # 0. Crear el archivo de datos de entrada
        crear_archivo_gigante_ejemplo()
        
        # 1. Crear las carpetas que simulan nuestros N discos
        rutas_discos = preparar_directorios_discos()
        
        # Definimos qué discos son de "entrada" y "salida" para la Fase 1
        # Dividimos los discos por la mitad
        mitad = NUM_DISCOS // 2
        discos_fase1_entrada = rutas_discos[:mitad]
        discos_fase1_salida = rutas_discos[mitad:]

        # 2. FASE 1: Crear tramos iniciales y distribuirlos en los primeros N/2 discos
        total_tramos_iniciales = crear_tramos_iniciales_distribuidos(discos_fase1_entrada)
        
        if total_tramos_iniciales == 0:
            print("No se crearon tramos. Terminando.")
        else:
            # 3. FASE 2: Pases de Mezcla Equilibrada
            
            num_pase = 0
            
            # Los discos de la Fase 1 ahora son la ENTRADA para el Pase 0
            discos_entrada_actuales = discos_fase1_entrada
            discos_salida_actuales = discos_fase1_salida
            
            num_tramos_en_juego = total_tramos_iniciales
            
            # El bucle se ejecuta mientras tengamos más de 1 tramo en total
            while num_tramos_en_juego > 1:
                
                # Ejecutamos un pase de mezcla
                num_tramos_creados = ejecutar_pase_mezcla(
                    discos_entrada_actuales, 
                    discos_salida_actuales, 
                    num_pase
                )
                
                # Actualizamos el número de tramos
                num_tramos_en_juego = num_tramos_creados
                
                
                # Los de salida ahora son de entrada, y viceversa.
                discos_entrada_actuales, discos_salida_actuales = discos_salida_actuales, discos_entrada_actuales
                
                num_pase += 1
                
           
            # El bucle terminó, significa que 'num_tramos_en_juego' es 1.
            # El unico tramo final está en el primer disco del último set de "discos de salida", que (por el último swap) ahora se llama 'discos_entrada_actuales'.
            
            disco_final = discos_entrada_actuales[0]
            nombre_archivo_final = os.path.join(disco_final, os.listdir(disco_final)[0])
            
            # Copiamos el resultado final al nombre de salida deseado
            shutil.copy(nombre_archivo_final, OUTPUT_FILE)
            
            print(f"\n--- ¡Ordenamiento Completado! ---")
            print(f"Total de Pases de Mezcla: {num_pase}")
            print(f"Resultado final guardado en: '{OUTPUT_FILE}'")

    finally:
        limpiar_todo()

