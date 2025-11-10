#Algoritmo del metodo MergeSort

# Definimos la función principal que recibirá la lista
def merge_sort(arr):
    
    # Si la lista tiene 1 elemento o menos, ya se considera ordenada.
    # Esto detiene la recursión (el "dividir").
    if len(arr) > 1:
        
        
        # 1. Encontrar el punto medio de la lista
        # (Usamos '//' para obtener una división entera)
        mid = len(arr) // 2
        
        # 2. Crear las dos sub-listas (mitades)
        # 'L' (Left) contendrá la primera mitad
        L = arr[:mid]
        
        # 'R' (Right) contendrá la segunda mitad
        R = arr[mid:]
        
        # 3. Llamadas Recursivas
        # Llamamos a merge_sort sobre la mitad izquierda.
        # Esto seguirá dividiendo 'L' hasta que solo queden elementos individuales.
        merge_sort(L)
        
        # Llamamos a merge_sort sobre la mitad derecha.
        # Esto seguirá dividiendo 'R' hasta que solo queden elementos individuales.
        merge_sort(R)
        
        # --- Fase de Conquista ---
        # En este punto, 'L' y 'R' son dos sub-listas que ya estan ordenadas
        # Ahora, necesitamos mezclarlas ordenadamente de vuelta en 'arr'.
        
        # 'i' será el puntero para la sub-lista Izquierda (L)
        i = 0
        # 'j' será el puntero para la sub-lista Derecha (R)
        j = 0
        # 'k' será el puntero para la lista principal (arr), donde
        # colocaremos los elementos mezclados.
        k = 0
        
        # Este bucle se ejecuta mientras HAYA elementos en AMBAS listas (L y R)
        while i < len(L) and j < len(R):
            
            # Comparamos el elemento actual de L con el de R
            if L[i] <= R[j]:
                # Si el de L es más pequeño (o igual), lo colocamos en arr[k]
                arr[k] = L[i]
                # Avanzamos el puntero de la lista L
                i += 1
            else:
                # Si el de R es más pequeño, lo colocamos en arr[k]
                arr[k] = R[j]
                # Avanzamos el puntero de la lista R
                j += 1
                
            # En cualquier caso, avanzamos el puntero de la lista principal
            k += 1
            
       
        # Al final del bucle anterior, es posible que una de las sub-listas (L o R) se haya "acabado" primero.
        # Necesitamos copiar los elementos restantes de la otra lista.
        
        # Bucle para copiar los elementos sobrantes de L (si los hay)
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        # Bucle para copiar los elementos sobrantes de R (si los hay)
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1



# Creamos una lista desordenada
lista_ejemplo = [38, 27, 43, 3, 9, 82, 10]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función principal para que ordene la lista
merge_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")