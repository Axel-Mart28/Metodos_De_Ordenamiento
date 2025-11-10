#Algoritmo del metodo de intercambio

# Definimos la función que recibirá la lista (arreglo) a ordenar
def bubble_sort(arr):
    
    # 'n' almacenará el número total de elementos en la lista.
    n = len(arr)
    
    # Este bucle 'for' (con la variable 'i') controla cuántas "pasadas" completas hacemos sobre la lista.
    # Después de cada pasada 'i', el i-ésimo elemento más grande ya estará en su posición final correcta al final de la lista.
    # Por eso, 'i' va de 0 hasta n-1.
    for i in range(n):
        
        # Creamos una variable para rastrear si hicimos algún intercambio en esta pasada.
        hubo_intercambios = False
        
        # Este bucle 'for' (con la variable 'j') es el que hace las comparaciones y los intercambios adyacentes.
        #
        # Va desde el primer elemento (índice 0) hasta 'n - i - 1'.
        # 'n - i': Porque los últimos 'i' elementos ya están ordenados.
        # '- 1': Porque comparamos 'j' con 'j + 1', así que paramos un elemento antes del final para no salirnos del rango.
        for j in range(0, n - i - 1):
            
        
            # Comparamos el elemento actual (arr[j]) con el siguiente (arr[j + 1]).
            if arr[j] > arr[j + 1]:
                
                # El Intercambio (Swap): Si el elemento actual es mas grande que el siguiente, los intercambiamos de lugar.
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                
                # Marcamos que sí hicimos un intercambio en esta pasada.
                hubo_intercambios = True
                
    
        # Si después de una pasada completa por el bucle interno
        # NO hicimos ni un solo intercambio...
        if not hubo_intercambios:
            # ...significa que la lista YA ESTÁ ORDENADA.
            # Podemos detener el algoritmo aquí y no hacer las pasadas restantes.
            break


# Creamos una lista desordenada
lista_ejemplo = [34, 90, 15, 8, 27, 2]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función para que ordene la lista
bubble_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")