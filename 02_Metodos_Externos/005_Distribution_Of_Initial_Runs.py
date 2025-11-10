#Algoritmo de Distribution Of Initial Runs

# --- Importaciones Necesarias ---
import heapq 
import os 
import random 
import shutil # Para borrar carpetas con contenido

# --- Constantes de Simulación ---
INPUT_FILE = 'datos_gigantes.txt'
OUTPUT_FILE = 'datos_ordenados_final.txt'

# Directorio principal para la simulación
TEMP_DIR = 'simulacion_discos' 

# Simularemos 4 discos (2 de entrada, 2 de salida, que luego intercambian)
NUM_DISCOS = 4

# Tamaño de nuestra "RAM" simulada
TAMANO_RAM = 10 
TOTAL_NUMEROS = 50 

# --- FUNCIÓN AUXILIAR DE MEZCLA (K-Way Merge) ---
# (Esta función no cambia, es nuestra herramienta de mezcla)
def k_way_merge_simple(archivos_entrada_nombres, archivo_salida_nombre):
    min_heap = []
    archivos_abiertos = []
    try:
        for i, nombre_tramo in enumerate(archivos_entrada_nombres):
            f = open(nombre_tramo, 'r')
            archivos_abiertos.append(f)
            linea = f.readline().strip()
            if linea:
                heapq.heappush(min_heap, (int(linea), i))
                
        with open(archivo_salida_nombre, 'w') as f_out:
            while min_heap:
                valor_minimo, indice_archivo = heapq.heappop(min_heap)
                f_out.write(f"{valor_minimo}\n")
                
                f_siguiente = archivos_abiertos[indice_archivo]
                linea_siguiente = f_siguiente.readline().strip()
                
                if linea_siguiente:
                    heapq.heappush(min_heap, (int(linea_siguiente), i))
    finally:
        for f in archivos_abiertos:
            f.close()

# --- FASE 1: Creación de Tramos + ESTRATEGIA DE DISTRIBUCIÓN ---
# Esta función implementa "Natural Merging" Y la estrategia de
# "Distribución Equilibrada de Corridas Iniciales".

def crear_tramos_iniciales_distribuidos(discos_destino):
    
    # 'discos_destino' es una lista de rutas, ej: ['sim/disco_0', 'sim/disco_1']
    num_discos_destino = len(discos_destino)
    
    print(f"--- FASE 1: Creando tramos (Natural Merging) y distribuyendo en {num_discos_destino} discos ---")
    
    # (Lógica de Natural Merging / Replacement Selection)
    heap_primario = []
    heap_secundario = []
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
            
        
            # Esta es la "estrategia de distribución". En este caso,
            # usamos una "Distribución Equilibrada" (Round-Robin)
            # usando el operador módulo (%).
            
            # 'total_tramos_creados' es un contador (0, 1, 2, 3, ...)
            
            # (0 % 2) -> asigna al disco 0
            # (1 % 2) -> asigna al disco 1
            # (2 % 2) -> asigna al disco 0
            # (3 % 2) -> asigna al disco 1
            # y asi sucesivamente.
            indice_disco_actual = total_tramos_creados % num_discos_destino
            
            # 'disco_actual' es la RUTA (la carpeta) donde se escribira este tramo.
            disco_actual = discos_destino[indice_disco_actual]
            
            
            # El nombre del tramo incluye el disco donde vivirá
            nombre_tramo = os.path.join(disco_actual, f'tramo_inicial_{total_tramos_creados}.txt')
            
            # (El resto es la lógica de "Natural Merging" para escribir
            # el tramo en el archivo 'nombre_tramo' que acabamos de definir)
            
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
# (Esta es la Fase 2 que "sabe" que los tramos están
# distribuidos equitativamente y actúa en consecuencia)

def ejecutar_pase_mezcla(discos_in, discos_out, num_pase):
    
    print(f"\n--- PASE DE MEZCLA {num_pase} ---")
    print(f"  Leyendo de: {[os.path.basename(d) for d in discos_in]}")
    print(f"  Escribiendo en: {[os.path.basename(d) for d in discos_out]}")
    
    tramos_por_disco = []
    for d in discos_in:
        tramos = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.txt')]
        tramos.sort() 
        tramos_por_disco.append(tramos)
        
    num_mezclas = max(len(t) for t in tramos_por_disco) if tramos_por_disco else 0
    num_tramos_creados = 0
    
    for i in range(num_mezclas):
        
        archivos_para_mezcla_actual = []
        
        # Tomamos el tramo 'i' de CADA disco de entrada
        for lista_tramos in tramos_por_disco:
            if i < len(lista_tramos):
                archivos_para_mezcla_actual.append(lista_tramos[i])
                
        if not archivos_para_mezcla_actual:
            continue
            
        # Elegimos el disco de SALIDA de forma rotativa (balanceada)
        indice_disco_salida = num_tramos_creados % len(discos_out)
        disco_salida_actual = discos_out[indice_disco_salida]
        
        nombre_tramo_salida = os.path.join(disco_salida_actual, f'pase_{num_pase}_tramo_{num_tramos_creados}.txt')
        
        # Ejecutar la Mezcla
        k_way_merge_simple(archivos_para_mezcla_actual, nombre_tramo_salida)
        
        print(f"    -> Mezclados {len(archivos_para_mezcla_actual)} tramos -> '{os.path.basename(nombre_tramo_salida)}'")
        
        num_tramos_creados += 1
        
    # Limpieza del Pase
    print(f"  Limpiando tramos antiguos de {[os.path.basename(d) for d in discos_in]}...")
    for d in discos_in:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
            
    return num_tramos_creados

# --- Funciones de Ayuda ---

def crear_archivo_gigante_ejemplo():
    print(f"--- Preparación: Creando '{INPUT_FILE}' con {TOTAL_NUMEROS} números... ---")
    with open(INPUT_FILE, 'w') as f:
        for _ in range(TOTAL_NUMEROS):
            f.write(f"{random.randint(1, 1000)}\n")

def preparar_directorios_discos():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    lista_discos = []
    for i in range(NUM_DISCOS):
        ruta_disco = os.path.join(TEMP_DIR, f'disco_{i}')
        os.makedirs(ruta_disco, exist_ok=True)
        lista_discos.append(ruta_disco)
        
    print(f"--- Preparación: Simulando {NUM_DISCOS} discos en '{TEMP_DIR}' ---")
    return lista_discos
    
def limpiar_todo():
    print(f"\n--- Limpieza: Borrando '{INPUT_FILE}', '{OUTPUT_FILE}' y '{TEMP_DIR}' ---")
    if os.path.exists(INPUT_FILE): os.remove(INPUT_FILE)
    if os.path.exists(OUTPUT_FILE): os.remove(OUTPUT_FILE)
    if os.path.exists(TEMP_DIR): shutil.rmtree(TEMP_DIR)
    print("--- Limpieza completada. ---")

# --- Ejecución Principal del Script ---
if __name__ == "__main__":
    
    try:
        crear_archivo_gigante_ejemplo()
        rutas_discos = preparar_directorios_discos()
        
        mitad = NUM_DISCOS // 2
        discos_fase1_entrada = rutas_discos[:mitad]
        discos_fase1_salida = rutas_discos[mitad:]

        # 2. FASE 1: Aquí se ejecuta la "Distribución de Corridas"
        total_tramos_iniciales = crear_tramos_iniciales_distribuidos(discos_fase1_entrada)
        
        if total_tramos_iniciales == 0:
            print("No se crearon tramos. Terminando.")
        else:
            # 3. FASE 2: Pases de Mezcla Equilibrada
            num_pase = 0
            discos_entrada_actuales = discos_fase1_entrada
            discos_salida_actuales = discos_fase1_salida
            num_tramos_en_juego = total_tramos_iniciales
            
            while num_tramos_en_juego > 1:
                
                num_tramos_creados = ejecutar_pase_mezcla(
                    discos_entrada_actuales, 
                    discos_salida_actuales, 
                    num_pase
                )
                
                num_tramos_en_juego = num_tramos_creados
                discos_entrada_actuales, discos_salida_actuales = discos_salida_actuales, discos_entrada_actuales
                num_pase += 1
                
            # --- Finalización ---
            disco_final = discos_entrada_actuales[0]
            nombre_archivo_final = os.path.join(disco_final, os.listdir(disco_final)[0])
            
            shutil.copy(nombre_archivo_final, OUTPUT_FILE)
            
            print(f"\n--- ¡Ordenamiento Completado! ---")
            print(f"Total de Pases de Mezcla: {num_pase}")
            print(f"Resultado final guardado en: '{OUTPUT_FILE}'")

    finally:
        # 4. Limpieza
        limpiar_todo()