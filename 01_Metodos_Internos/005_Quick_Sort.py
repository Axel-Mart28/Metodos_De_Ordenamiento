#Algoritmo de  QuickSort
# Esta función es la  que inicia el proceso.
# Recibe el arreglo y llama a la función recursiva 'quick_sort_recursivo'.
def quick_sort(arr):
    
    # Llamamos a la función auxiliar que hace el trabajo pesado.
    # Le pasamos el arreglo completo, el índice de inicio (0) y el índice del final (longitud - 1).
    quick_sort_recursivo(arr, 0, len(arr) - 1)

# Esta función ordena el pedazo del arreglo entre 'low' (bajo) y 'high' (alto).
def quick_sort_recursivo(arr, low, high):
    

    # Si 'low' es mayor o igual a 'high', significa que el pedazo del arreglo tiene 0 o 1 elementos, por lo tanto, ya esta ordenado.
    # Esto detiene la recursión.
    if low < high:
        
        
        # Llama a la función 'partition' para encontrar un pivote y reordenar el arreglo alrededor de él.
        # 'pi' (partition index) es la posicion final donde quedó el pivote.
        pi = partition(arr, low, high)
        
        
        # Ahora que el pivote en 'pi' está en su lugar, aplicamos QuickSort a las dos sub-listas que se formaron:
        
        # 1. La sub-lista a la IZQUIERDA del pivote (sin incluir el pivote)
        quick_sort_recursivo(arr, low, pi - 1)
        
        # 2. La sub-lista a la DERECHA del pivote (sin incluir el pivote)
        quick_sort_recursivo(arr, pi + 1, high)


# Esta es una de las formas más comunes de implementar la partición.
# Reordena el arreglo (entre 'low' y 'high') usando el ÚLTIMO elemento ('high') como pivote.
def partition(arr, low, high):
    
    # Seleccionamos el último elemento del segmento (arr[high]) como pivote.
    pivot = arr[high]
    
    # 'i' es un puntero que rastrea la "frontera" del último elemento
    # que es MÁS PEQUEÑO que el pivote.
    # Lo inicializamos en 'low - 1' (justo antes del inicio del segmento).
    i = low - 1
    
   
    # Recorremos el segmento desde 'low' hasta 'high - 1' (sin incluir el pivote).
    for j in range(low, high):
        
        # Comparamos el elemento actual (arr[j]) con el pivote.
        if arr[j] <= pivot:
            
            # Si el elemento es MENOR O IGUAL que el pivote avanzamos nuestro puntero de "menores" ('i').
            i = i + 1
            
            #intercambiamos arr[i] con arr[j].
            # Esto mueve el elemento 'arr[j]' (que es pequeño) a la "zona de los menores" (que está a la izquierda de 'i').
            arr[i], arr[j] = arr[j], arr[i]
            
    # Al final del bucle 'for', todos los elementos menores que el pivote estan de 'low' hasta 'i'. Todos los mayores están de 'i + 1' hasta 'high - 1'.
    
    # El pivote (que estaba en arr[high]) debe ir en la posición 'i + 1'.
    # Intercambiamos el pivote (arr[high]) con el elemento en arr[i + 1].
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Ahora el pivote está en su posición final y correcta.
    
    # Devolvemos la posición donde quedó el pivote ('i + 1').
    return i + 1


# Creamos una lista desordenada
lista_ejemplo = [10, 7, 8, 9, 1, 5]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función principal para que ordene la lista
quick_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")