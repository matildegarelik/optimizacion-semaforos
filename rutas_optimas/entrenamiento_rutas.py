import numpy as np
import random


# Generación de una ruta aleatoria que respeta la vecindad
def generar_ruta_aleatoria(LONG_MAX_RUTAS,matriz_vecindad,N):
    ruta = []
    nodo_actual = np.random.randint(0, N * N)
    ruta.append(nodo_actual)
    for _ in range(LONG_MAX_RUTAS - 1):
        vecinos = np.where(matriz_vecindad[nodo_actual] == 1)[0]
        if len(vecinos) == 0:
            break
        nodo_actual = random.choice(vecinos)
        ruta.append(nodo_actual)
    return ruta

# Generación de una población inicial
def generar_poblacion(LONG_MAX_RUTAS,matriz_vecindad,N, NUM_RUTAS,POPULATION_SIZE):
    return [[generar_ruta_aleatoria(LONG_MAX_RUTAS,matriz_vecindad,N) for _ in range(NUM_RUTAS)] for _ in range(POPULATION_SIZE)]

# Función de fitness que calcula el error con respecto al flujo objetivo
def calcular_fitness(individuo, autos_por_ruta,N,matriz_vecindad,flujo_objetivo):
    flujo_predicho = np.zeros((N, N))

    # Calcular el flujo en cada intersección basado en las rutas
    for i, ruta in enumerate(individuo):
        autos = autos_por_ruta[i]
        for nodo in ruta:
            fila, columna = divmod(nodo, N)
            flujo_predicho[fila, columna] += autos

    # Error cuadrático medio con respecto al flujo objetivo
    flujo_error = np.mean((flujo_objetivo - flujo_predicho) ** 2)

    # Penalización por rutas que no respetan la vecindad
    penalidad_vecindad = 0
    
    for ruta in individuo:
        for j in range(len(ruta) - 1):
            if matriz_vecindad[ruta[j], ruta[j + 1]] == 0:
                penalidad_vecindad += 1

    return flujo_error + penalidad_vecindad

# Selección por torneo
def seleccion(poblacion, autos_por_ruta,N,matriz_vecindad,flujo_objetivo):
    torneo = random.sample(poblacion, k=3)
    torneo.sort(key=lambda ind: calcular_fitness(ind, autos_por_ruta,N,matriz_vecindad,flujo_objetivo))
    return torneo[0]

# Cruce de dos individuos
def cruce(individuo1, individuo2,NUM_RUTAS):
    punto_cruce = random.randint(1, NUM_RUTAS - 1)
    hijo = individuo1[:punto_cruce] + individuo2[punto_cruce:]
    return hijo

# Mutación de un individuo
def mutacion(individuo,LONG_MAX_RUTAS,matriz_vecindad,N,NUM_RUTAS,MUTATION_RATE):
    for i in range(NUM_RUTAS):
        if random.random() < MUTATION_RATE:
            individuo[i] = generar_ruta_aleatoria(LONG_MAX_RUTAS,matriz_vecindad,N)
    return individuo

# Algoritmo Genético
def algoritmo_genetico(N, NUM_RUTAS, LONG_MAX_RUTAS, AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX, matriz_vecindad, flujo_objetivo,
                       POPULATION_SIZE = 500, GENERATIONS = 1000, MUTATION_RATE = 0.1, imprimir=True):
    poblacion = generar_poblacion(LONG_MAX_RUTAS,matriz_vecindad,N, NUM_RUTAS,POPULATION_SIZE)
    mejor_fitness = float('inf')
    mejor_individuo = None

    for generacion in range(GENERATIONS):
        autos_por_ruta = np.random.randint(AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX, NUM_RUTAS)
        nueva_poblacion = []
        
        for _ in range(POPULATION_SIZE):
            padre1 = seleccion(poblacion, autos_por_ruta,N,matriz_vecindad,flujo_objetivo)
            padre2 = seleccion(poblacion, autos_por_ruta,N,matriz_vecindad,flujo_objetivo)
            hijo = cruce(padre1, padre2,NUM_RUTAS)
            hijo = mutacion(hijo,LONG_MAX_RUTAS,matriz_vecindad,N,NUM_RUTAS,MUTATION_RATE)
            nueva_poblacion.append(hijo)

        # Evaluar el fitness de la nueva población
        poblacion = nueva_poblacion
        for individuo in poblacion:
            fitness = calcular_fitness(individuo, autos_por_ruta,N,matriz_vecindad,flujo_objetivo)
            if fitness < mejor_fitness:
                mejor_fitness = fitness
                mejor_individuo = individuo
        
        # Imprimir progreso
        if imprimir:
            print(f"Generación {generacion+1}, Mejor Fitness: {mejor_fitness}")

    return mejor_individuo, autos_por_ruta
