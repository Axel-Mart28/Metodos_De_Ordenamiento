#Algoritmo de RadixSort

# --- Sub-rutina: Counting Sort (Ordenamiento por Conteo) ---
# 'arr' es la lista a ordenar.
# 'exp' es el exponente (1, 10, 100...)
def counting_sort(arr, exp):
    
    # 'n' es el tamaño de la lista
    n = len(arr)
    
    # 'output' es una lista temporal del mismo tamaño para guardar el resultado ordenado.
    output = [0] * n
    
    # 'count' es una lista de 10 elementos (para los dígitos 0 al 9), inicializada en ceros.
    count = [0] * 10
    
    # --- Fase 1: Contar las apariciones de cada dígito ---
    # Recorremos la lista 'arr'.
    for i in range(n):
        
        # Obtenemos el dígito que nos interesa.
        # (ej. si arr[i]=175 y exp=10 -> (175 // 10) = 17 -> 17 % 10 = 7)
        digit = (arr[i] // exp) % 10
        
        # Incrementamos el contador para ese dígito.
        count[digit] += 1
        
    # --- Fase 2: Convertir 'count' en posiciones finales ---
    # 'count[i]' ahora almacenará la *posición* donde debe ir
    # el último elemento con ese dígito en la lista 'output'.
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    # --- Fase 3: Construir la lista 'output' ---
    # Recorremos la lista 'arr' EN REVERSA (de 'n-1' hasta '0').
    # Esto es CRUCIAL para que el ordenamiento sea estable
    # Estable = si dos números tienen el mismo dígito, mantienen el mismo orden relativo que tenían antes.
    i = n - 1
    while i >= 0:
        
        # Obtenemos el dígito del elemento actual.
        digit = (arr[i] // exp) % 10
        
        # Usamos 'count[digit]' para saber la posición correcta en 'output'.
        # Le restamos 1 porque los índices de 'count' están basados en 1 y los de 'output' en 0.
        output[count[digit] - 1] = arr[i]
        
        # Decrementamos el contador para ese dígito, asi el próximo elemento con el mismo dígito se colocara en la posición anterior.
        count[digit] -= 1
        
        # Pasamos al siguiente elemento (hacia la izquierda).
        i -= 1
        
    # --- Fase 4: Copiar 'output' de vuelta a 'arr' ---
    # Ahora 'arr' está ordenada según el dígito 'exp'.
    for i in range(n):
        arr[i] = output[i]

# --- Función Principal: RadixSort ---
def radix_sort(arr):
    
    # Si la lista está vacía, no hay nada que hacer.
    if not arr:
        return
        
    # 1. Encontrar el número máximo en la lista.
    # Esto nos dice cuántos dígitos tiene el número más grande, y por lo tanto, cuántas "pasadas" de CountingSort necesitamos.
    max_num = max(arr)
    
    # 2. Inicializar el exponente 'exp' en 1 (para ver las unidades).
    exp = 1
    
    # 3. Bucle principal de RadixSort
    # Este bucle 'while' se ejecutará mientras 'exp' sea lo suficientemente pequeño como para "sacar" un dígito del número máximo.
    # (ej. si max_num=175, se ejecuta para exp=1, exp=10, exp=100)
    while max_num // exp > 0:
        
        # Llamamos a CountingSort para ordenar la lista
        # basándonos en el dígito actual (definido por 'exp').
        counting_sort(arr, exp)
        
        # Multiplicamos 'exp' por 10 para pasar al siguiente dígito
        # (unidades -> decenas -> centenas...)
        exp *= 10


# Creamos una lista desordenada
lista_ejemplo = [170, 45, 75, 90, 802, 24, 2, 66]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función principal para que ordene la lista
radix_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")