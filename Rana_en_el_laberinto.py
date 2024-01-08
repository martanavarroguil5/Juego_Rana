'''
Primero se define la función que determina la probabilidad de escape teniendo en cuenta n 
que son el número de columnas, m el numero de filas, k el numero de túneles, los túneles y el laberinto entero.'''
def escape_probability(n, m, k, laberinto, tuneles):

    '''
    Dentro definimos una funcion que evalúe la validez un movimiento a la posición (x, y), 
    garantizndo que se encuentre entre los perímetros que limitan al laberinto y que no sea un obstáculo.'''
    def is_valid_move(x, y):
        return 0 <= x < n and 0 <= y < m and laberinto[x][y] not in ['#','*']
    
    
    '''
    Ahora se define una función que calcula la probabilidad de escape. Cuenta con el posible movimiento
    (x, y) que se ha evaluado anteriormente, y con una lista "visited" que guarda las posiciones de los
    puntos visitados'''
    def find_exit_probability(x, y, visited):
        if laberinto[x][y] == '%':
            return 1.0  # Si Alef ya está en la salida la probabilidad es de 1.

        if (x, y) in visited:
            return 0.0  # Si ya has visitado este lugar, te devuelve 0 para evitar las repeticiones. 
        
        '''
        La lista con las posiciones visitadas se va expandiendo con forme se evaluan las distintas 
        posiciones dentro del laberinto. En esta lista se añade la posición actual.'''
        visited.add((x, y))
        total_probability = 0.0 # Se inicia con una probabilidad de 0.
        # Para poder moverte hacia arriba, abajo, a la izquierda o derecha.
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        '''
        Para un proximo movimiento, primero de todo debe de estar dentro de los movimientos posibles con respecto
        a la posición actual y luego evaluar su validez de nuevo. Esto se hace con las funciones ya definidas 
        anteriormente. Se toman el "proximo movimiento" como si fuera el actual en las variables de las funciones.
        En el caso de que sea un movimiento válido la probabilidad de encontrar la salida desde esta posición nueva 
        se le suma a la probabilidad total.'''
        for next_x, next_y in possible_moves:
            if is_valid_move(next_x, next_y):
                total_probability += find_exit_probability(next_x, next_y, visited)

        visited.remove((x, y))  # Con esto se elimina la posición actual de la lista para poder explorar otras.
        '''
        Devuelve la probabilidad total de escape desde la posición actual, dividiendo la probabilidad total 
        acumulada por el número de posibles movimientos válidos (len(possible_moves)). Esta división garantiza que 
        la probabilidad se distribuya equitativamente entre todas las opciones de movimiento válidas. Se asume que 
        la probabilidad se divide por el número de movimientos posibles, ya que Alef tiene igual probabilidad de 
        elegir cualquiera de las direcciones válidas.'''
        return total_probability / len(possible_moves)

    '''
    Esta función verifica que el movimiento al túnel sea válida. Primero debe encontrarse en los límites marcados 
    por el laberinto ni que sea un obstáculo. Con el túnel se consigue llegar a la otra desembocación, por lo tanto 
    se crea una tupla (tunnel) con la posición de las dos bocas. Con esta función se verifica que la posición no sea
    la entrada/salida de un túnel'''
    def is_valid_move_with_tunnel(x, y, tunnel):
        return 0 <= x < n and 0 <= y < m and laberinto[x][y] not in ['#', '_', '*'] and (x, y) != (tunnel[0], tunnel[1])

    
    for i in range(n):
        for j in range(m):
            if laberinto[i][j] == 'A':
                initial_position = (i, j)

    # Calculate the probability of escape considering tunnels
    total_probability = 0.0
    for tunnel in tuneles:
        x, y = initial_position
        if is_valid_move_with_tunnel(x, y, tunnel):
            total_probability += find_exit_probability(tunnel[2], tunnel[3], set())

    return total_probability

# Le pide al usuario que proporciones los datos del laberinto que necesita.
print("Ingrese las dimensiones del laberinto y el número de túneles (n m k):")
n, m, k = map(int, input().split())

print("Ingrese el laberinto (utilice '#' para obstáculos, '_' para espacios vacíos, 'A' para Alef, '*' para minas, '%' para salidas, 'T' para túneles):")
laberinto = [list(input()) for _ in range(n)]

print(f"Ingrese las coordenadas de los túneles (x1 y1 x2 y2) para cada túnel (k veces):")
print ("Escriba en la misma fila los túneles asociados:")
'''
Se encarga de recibir las coordenadas de los túneles desde la entrada estándar y almacenarlas en una lista 
llamada tuneles'''
tuneles = [list(map(int, input().split())) for _ in range(k)]

# Calcular la probabilidad de escape y mostrar el resultado
result = escape_probability(n, m, k, laberinto, tuneles)
print(f"\nLa probabilidad de escape de Alef es: {result}")