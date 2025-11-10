#Algoritmo de metodo de Seleccion

# Definimos la función que recibirá la lista (arreglo) a ordenar
def selection_sort(arr):
    
    # 'n' almacenará el número total de elementos en la lista.
    n = len(arr)
    
    # Este bucle 'for' recorre toda la lista. La variable 'i' representa el inicio de la "parte desordenada" de la lista.
    # Todo lo que esté a la izquierda de 'i' ya se considera ordenado.
    for i in range(n):
        
        # Suponemos inicialmente que el elemento más pequeño ('min_idx') es el primero de la parte desordenada (el elemento en 'i').
        min_idx = i
        
        
        # Este bucle 'for' (con la variable 'j') se usa para buscar  el verdadero elemento más pequeño en el resto de la lista desordenada.
        # Comienza en 'i + 1' (el elemento a la derecha de 'i') y va hasta el final.
        for j in range(i + 1, n):
            
            # Comparamos el valor en la posición 'j' con el valor de nuestro mínimo actual ('min_idx').
            if arr[j] < arr[min_idx]:
                
                # Si encontramos un elemento más pequeño, actualizamos 'min_idx' para que apunte a la posición 'j'.
                min_idx = j
                
        
        # En este punto, 'min_idx' contiene el índice (la posición) del elemento MÁS PEQUEÑO de toda la parte desordenada (de 'i' hasta el final).
        
        # --- Fase de Intercambio (Swap) ---
        # Ahora intercambiamos el elemento más pequeño que encontramos (en 'min_idx') con el elemento al inicio de la parte desordenada (en 'i').
        
        # Esta es la forma compacta de Python para hacer un intercambio:
        # (arr[i] toma el valor de arr[min_idx]) (arr[min_idx] toma el valor de arr[i])
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
        # Después de este intercambio, el elemento en la posición 'i' está en su lugar final y correcto.
        # La "parte ordenada" ha crecido en un elemento.
        
    # Una vez que 'i' ha recorrido toda la lista, todos los elementos han sido colocados en su posición correcta.


# Creamos una lista desordenada
lista_ejemplo = [64, 25, 12, 22, 11]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función para que ordene la lista
selection_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")