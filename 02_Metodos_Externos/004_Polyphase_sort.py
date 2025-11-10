#Algoritmo de Polyphase sort

# --- Importaciones Necesarias ---
import heapq 
import os 
import random 
import shutil # Para borrar carpetas con contenido

# --- Constantes de Simulación ---
INPUT_FILE = 'datos_gigantes.txt'
OUTPUT_FILE = 'datos_ordenados_final.txt'

# Directorio principal para la simulación
TEMP_DIR = 'simulacion_discos_poly' 

# Polyphase Sort funciona con K discos. Usaremos 3 
NUM_DISCOS = 3

# Tamaño de nuestra "RAM" simulada
TAMANO_RAM = 10 
TOTAL_NUMEROS = 50 

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
                    heapq.heappush(min_heap, (int(linea_siguiente), indice_archivo))
    finally:
        for f in archivos_abiertos:
            f.close()


def crear_tramos_iniciales_distribuidos(discos_destino):
    num_discos_destino = len(discos_destino)
    print(f"--- FASE 1: Creando tramos (Natural Merging) y distribuyendo en {num_discos_destino} discos ---")
    
    heap_primario = []
    heap_secundario = []
    total_tramos_creados = 0
    
    try:
        f_in = open(INPUT_FILE, 'r')
        for _ in range(TAMANO_RAM):
            linea = f_in.readline().strip()
            if linea: heap_primario.append(int(linea))
            else: break
        heapq.heapify(heap_primario)
        
        while heap_primario:
            # Distribuir equitativamente entre los discos de destino
            indice_disco_actual = total_tramos_creados % num_discos_destino
            disco_actual = discos_destino[indice_disco_actual]
            
            nombre_tramo = os.path.join(disco_actual, f'tramo_inicial_{total_tramos_creados}.txt')
            
            f_out = open(nombre_tramo, 'w')
            print(f"  -> Creando '{nombre_tramo}'...")
            
            ultimo_valor_escrito = float('-inf')
            
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
            
            f_out.close()
            total_tramos_creados += 1
            
            heap_primario = heap_secundario
            heap_secundario = []
            if heap_primario:
                heapq.heapify(heap_primario)
    finally:
        f_in.close()
    print(f"--- FASE 1: Completada. {total_tramos_creados} tramos creados. ---")
    return total_tramos_creados

#Funciones de ayuda
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

# --- Función auxiliar para la Fase 2 Polyphase ---
def obtener_listas_de_archivos_por_disco(rutas_discos):
    # Devuelve una lista de listas, ej: [['disco0/tramo1.txt'], ['disco1/tramoA.txt', 'disco1/tramoB.txt'], []]
    listas_globales = []
    for disco_ruta in rutas_discos:
        archivos_en_disco = [os.path.join(disco_ruta, f) for f in os.listdir(disco_ruta) if f.endswith('.txt')]
        archivos_en_disco.sort() # Ordenar para consistencia
        listas_globales.append(archivos_en_disco)
    return listas_globales



if __name__ == "__main__":
    
  
    
    try:
        # 0. Crear el archivo de datos de entrada
        crear_archivo_gigante_ejemplo()
        
        # 1. Crear las carpetas que simulan nuestros N discos
        rutas_discos = preparar_directorios_discos() # Ej: ['sim/disco_0', 'sim/disco_1', 'sim/disco_2']
        
        # 2. FASE 1: Crear tramos iniciales y distribuirlos en N-1 discos
        discos_para_fase1 = rutas_discos[:-1] # Ej: ['sim/disco_0', 'sim/disco_1']
        crear_tramos_iniciales_distribuidos(discos_para_fase1)
        
        # 3. FASE 2: Bucle Principal de Mezcla Polifásica
        print("\n--- FASE 2: Iniciando Mezcla Polifásica ---")
        
        num_pase = 0
        
        while True:
            
            num_pase += 1
            print(f"\n--- PASE DE MEZCLA POLIFÁSICA {num_pase} ---")
            
            # --- 1. Inspeccionar el estado de los discos ---
            listas_de_archivos = obtener_listas_de_archivos_por_disco(rutas_discos)
            conteo_de_archivos = [len(lista) for lista in listas_de_archivos]
            
            print(f"  Estado actual de tramos por disco: {conteo_de_archivos}")
            
            indices_discos_entrada = [i for i, count in enumerate(conteo_de_archivos) if count > 0]
            indices_discos_salida = [i for i, count in enumerate(conteo_de_archivos) if count == 0]
            
            # --- 2. Comprobar si hemos terminado ---
            if len(indices_discos_entrada) == 1 and conteo_de_archivos[indices_discos_entrada[0]] == 1:
                print("  Un solo tramo final detectado. ¡Ordenamiento completado!")
                disco_final = rutas_discos[indices_discos_entrada[0]]
                nombre_archivo_final = listas_de_archivos[indices_discos_entrada[0]][0]
                shutil.copy(nombre_archivo_final, OUTPUT_FILE)
                print(f"Resultado copiado a: {OUTPUT_FILE}")
                break # Salimos del bucle 'while True'
                
            # --- 3. Comprobar Errores ---
            if not indices_discos_salida:
                 # ¡Esto pasaría si NINGÚN disco está vacío, un estado imposible!
                 print("  ¡¡¡ERROR FATAL!!! No hay disco de salida disponible. Todos los discos tienen tramos.")
                 raise Exception("¡Error Polyphase! No hay disco de salida disponible.")

            if len(indices_discos_salida) != 1:
                 print(f"  Alerta: Se encontraron {len(indices_discos_salida)} discos vacíos. Se usará el primero.")

            # Asignamos los roles
            indice_salida = indices_discos_salida[0]
            
            print(f"  Discos de ENTRADA: {indices_discos_entrada}")
            print(f"  Disco de SALIDA: {indice_salida}")
            
            # --- 4. Determinar cuántas mezclas hacer ---
            if not indices_discos_entrada:
                 print("  No hay discos de entrada. ¿Archivo inicial vacío?")
                 break # Salir si el archivo de entrada estaba vacío

            min_tramos_en_entrada = min(conteo_de_archivos[i] for i in indices_discos_entrada)
            print(f"  Se ejecutarán {min_tramos_en_entrada} mezclas ({len(indices_discos_entrada)}-a-1) en este pase.")
            
            # --- 5. Ejecutar las mezclas ---
            for i in range(min_tramos_en_entrada):
                
                archivos_para_mezcla_actual = []
                archivos_para_borrar_despues = []
                
                for idx_disco_in in indices_discos_entrada:
                    tramo_a_mezclar = listas_de_archivos[idx_disco_in].pop(0)
                    archivos_para_mezcla_actual.append(tramo_a_mezclar)
                    archivos_para_borrar_despues.append(tramo_a_mezclar)
                    
                nombre_tramo_salida = os.path.join(
                    rutas_discos[indice_salida], 
                    f'pase_{num_pase}_tramo_{i}.txt'
                )
                
                # --- Ejecutar la Mezcla ---
                print(f"    Mezclando {len(archivos_para_mezcla_actual)} tramos -> {os.path.basename(nombre_tramo_salida)} ...", end="")
                k_way_merge_simple(archivos_para_mezcla_actual, nombre_tramo_salida)
                print("OK.")
                
                # --- Borrar los tramos de entrada ---
                print(f"    Borrando tramos de entrada usados:")
                for f in archivos_para_borrar_despues:
                    try:
                        os.remove(f)
                        print(f"      - Borrado: {os.path.basename(f)}")
                    except Exception as e:
                        # Si esto se imprime, encontramos el problema
                        print(f"      - ¡¡¡ERROR AL BORRAR {f}: {e}!!!") 
                        
            print(f"  --- Fin del Pase {num_pase} ---")
            
    except Exception as e:
        print(f"\n¡¡¡HA OCURRIDO UN ERROR INESPERADO!!!: {e}")
    
    finally:
        print("\nEjecución terminada. (Limpieza manual pendiente si 'limpiar_todo' está comentado)")