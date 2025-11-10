#Algoritmo del metodo de ordenamiento de arbol
# Función Auxiliar: heapify 
# Esta función es la MÁS IMPORTANTE.
# Su trabajo es tomar un sub-árbol (cuya raíz está en el índice 'i') y asegurarse de que cumpla la propiedad de Max-Heap (que el padre sea el mas grande). "n" es el tamaño total del heap (lista).

def heapify(arr, n, i):
    
    # Asumimos que el elemento mas grande ('largest') es la raíz actual ('i').
    largest = i
    
    # Calculamos el índice del hijo izquierdo
    # En un heap-array, el hijo izquierdo de 'i' es '2*i + 1'
    left = 2 * i + 1
    
    # Calculamos el índice del hijo derecho
    # En un heap-array, el hijo derecho de 'i' es '2*i + 2'
    right = 2 * i + 2
    
    
    # 1. Verificamos que el hijo izquierdo exista (que esté dentro del tamaño 'n' del heap)
    # 2. Verificamos si el hijo izquierdo (arr[left]) es mas grande que la raíz (arr[largest])
    if left < n and arr[left] > arr[largest]:
        
        # Si es más grande, actualizamos 'largest' para que apunte al hijo izquierdo
        largest = left
        
    
    # 1. Verificamos que el hijo derecho exista (que esté dentro del tamaño 'n' del heap)
    # 2. Verificamos si el hijo derecho (arr[right]) es MÁS GRANDE que el 'largest' que tenemos hasta ahora.
    if right < n and arr[right] > arr[largest]:
        
        # Si es más grande, actualizamos 'largest' para que apunte al hijo derecho
        largest = right
        
    
    # Si 'largest' NO es la raíz original ('i') significa que uno de los hijos era más grande.
    if largest != i:
        
        # Intercambiamos la raíz ('i') con el hijo más grande ('largest')
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # Al intercambiar, es posible que hayamos "roto" la propiedad de Max-Heap en el sub-árbol de abajo.
        # Así que llamamos recursivamente a 'heapify' sobre ese sub-árbol (cuya nueva raíz es 'largest') para repararlo "hacia abajo".
        heapify(arr, n, largest)

# --- Función Principal: HeapSort ---
def heap_sort(arr):
    
    # 'n' es el número de elementos en la lista.
    n = len(arr)
    
    # --- FASE 1: Construir el Max-Heap ---
    # Empezamos desde el ultimo nodo padre. Su índice es (n // 2) - 1.
    # Vamos "hacia atrás" (hasta el índice 0) aplicando 'heapify' a cada sub-árbol para construir el Max-Heap completo.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        
    # En este punto, 'arr' ya es un Max-Heap.
    # El elemento más grande está en 'arr[0]'.
    
    # --- FASE 2: Extraer elementos uno por uno ---
    #
    # Recorremos la lista desde el final ('n - 1') hasta el principio.
    for i in range(n - 1, 0, -1):
        
        # Movemos la raíz actual (el elemento más grande, 'arr[0]')
        # al final de la parte "no ordenada" de la lista (posición 'i').
        # Esto pone al elemento más grande en su lugar ordenado final.
        arr[i], arr[0] = arr[0], arr[i]
        
        # --- Reparar el Heap ---
        # El intercambio rompió el Max-Heap en la raíz.
        # Llamamos a 'heapify' sobre la raíz (índice 0) para repararlo.
        #
        # El tamaño del heap ahora es 'i' (no 'n'), porque estamos ignorando los elementos que ya movimos al final (que ya están ordenados).
        heapify(arr, i, 0)
        


# Creamos una lista desordenada
lista_ejemplo = [12, 11, 13, 5, 6, 7]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función para que ordene la lista
heap_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")