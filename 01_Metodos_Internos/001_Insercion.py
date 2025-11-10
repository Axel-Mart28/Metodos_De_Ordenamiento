#Algoritmo del metodo de ordenamiento de Insercion

# Definimos la función que recibirá la lista de números a ordenar
def insertion_sort(arr):
    
    # Iniciamos un bucle 'for' que recorrerá la lista DESDE el segundo elemento (indice 1) hasta el final. Omitimos el primer elemento (índice 0) porque una lista de un solo elemento ya se considera "ordenada".
    for i in range(1, len(arr)):
        
        # elemento_actual es el valor que vamos a tomar para "insertar" en la parte ordenada de la lista.
        elemento_actual = arr[i]
        
        # j es un índice que usaremos para movernos hacia la izquierda a través de la sub-lista ya ordenada.
        # Comienza en la posición justo a la izquierda del elemento actual.
        j = i - 1
        
        # Inicio del bucle while
        # Este bucle moverá los elementos de la parte ordenada que son mas grandes que el elemento_actual una posición a la derecha.
        # Se ejecutará mientras se cumplan DOS condiciones:
        # 1. 'j >= 0': No nos hemos salido del inicio de la lista.
        # 2. 'elemento_actual < arr[j]': El elemento que queremos insertar es MÁS PEQUEÑO que el elemento que estamos mirando en la parte ordenada.
        while j >= 0 and elemento_actual < arr[j]:
            
            # Como arr[j] es MÁS GRANDE que nuestro elemento_actual, lo movemos una posición a la derecha (a la posición j + 1). Esto abre un hueco para insertar nuestro elemento.
            arr[j + 1] = arr[j]
            
            # Movemos el índice 'j' una posición más a la izquierda para comparar con el siguiente elemento de la parte ordenada.
            j = j - 1
            
        
        # En este punto, el bucle 'while' se detuvo. Esto significa que:
        # Hemos llegado al inicio de la lista (j = -1) O hemos encontrado un elemento que es MÁS PEQUEÑO o IGUAL (arr[j]) que nuestro elemento_actual.
        
        # El lugar correcto para insertar es 'j + 1' (a la derecha de ese elemento más pequeño).
        arr[j + 1] = elemento_actual


# Creamos una lista desordenada
lista_ejemplo = [12, 11, 13, 5, 6]

print(f"Lista original: {lista_ejemplo}")

# Llamamos a la función para que ordene la lista
insertion_sort(lista_ejemplo)

print(f"Lista ordenada: {lista_ejemplo}")