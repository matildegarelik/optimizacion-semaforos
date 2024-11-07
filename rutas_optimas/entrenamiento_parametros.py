import numpy as np
import random
from entrenamiento_rutas import algoritmo_genetico, calcular_fitness

POPULATION_SIZE = 50
GENERATIONS = 10
MUTATION_RATE = 0.15

# Parámetros a ajustar
NUM_RUTAS_MIN, NUM_RUTAS_MAX = 5, 20
LONG_MAX_RUTAS_MIN, LONG_MAX_RUTAS_MAX = 4, 15
AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX = 10, 500

# Nueva función de fitness que evalúa los parámetros
def fitness_parametros(params, N, matriz_vecindad, flujo_objetivo):
    # Actualizar los parámetros
    global NUM_RUTAS, LONG_MAX_RUTAS, AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX
    
    NUM_RUTAS = params[0]
    LONG_MAX_RUTAS = params[1]
    AUTOS_POR_RUTA_MIN = params[2]
    AUTOS_POR_RUTA_MAX = params[3]

    # Verificar que los parámetros son válidos
    if AUTOS_POR_RUTA_MIN >= AUTOS_POR_RUTA_MAX:
        return float('inf')  # Penaliza con un valor muy alto si los parámetros no son válidos

    
    # Ejecutar el algoritmo genético original para obtener el fitness
    mejor_rutas, mejor_autos_por_ruta = algoritmo_genetico(N, NUM_RUTAS, LONG_MAX_RUTAS, AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX, matriz_vecindad, flujo_objetivo, imprimir=False)
    fitness = calcular_fitness(mejor_rutas, mejor_autos_por_ruta, N, matriz_vecindad, flujo_objetivo)
    
    return fitness

# Algoritmo Genético para optimizar parámetros
def algoritmo_genetico_parametros(N, matriz_vecindad, flujo_objetivo):
    # Población inicial: [NUM_RUTAS, LONG_MAX_RUTAS, AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX]
    poblacion = [
        [
            random.randint(NUM_RUTAS_MIN, NUM_RUTAS_MAX), 
            random.randint(LONG_MAX_RUTAS_MIN, LONG_MAX_RUTAS_MAX), 
            random.randint(AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX),
            random.randint(AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX)
        ]
        for _ in range(POPULATION_SIZE)  # Tamaño de la población
    ]
    
    mejor_fitness = float('inf')
    mejor_parametros = None

    for generacion in range(GENERATIONS):  # Número de generaciones
        nueva_poblacion = []
        
        for _ in range(POPULATION_SIZE):  # Tamaño de la nueva población
            padre1 = seleccion(poblacion,N, matriz_vecindad, flujo_objetivo)
            padre2 = seleccion(poblacion,N, matriz_vecindad, flujo_objetivo)
            hijo = cruce(padre1, padre2)
            
            # Asegurar que el hijo tenga parámetros válidos
            hijo[0] = np.clip(hijo[0], NUM_RUTAS_MIN, NUM_RUTAS_MAX)
            hijo[1] = np.clip(hijo[1], LONG_MAX_RUTAS_MIN, LONG_MAX_RUTAS_MAX)
            hijo[2] = np.clip(hijo[2], AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX)
            hijo[3] = np.clip(hijo[3], AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX)

            hijo = mutacion(hijo)

            nueva_poblacion.append(hijo)

        # Evaluar el fitness de la nueva población
        poblacion = nueva_poblacion
        for params in poblacion:
            fitness = fitness_parametros(params,N, matriz_vecindad, flujo_objetivo)
            if fitness < mejor_fitness:
                mejor_fitness = fitness
                mejor_parametros = params
        
        # Imprimir progreso
        print(f"Generación {generacion + 1}, Mejor Fitness: {mejor_fitness}, Parámetros: {mejor_parametros}")

    return mejor_parametros

# Función de selección por torneo
def seleccion(poblacion,N, matriz_vecindad, flujo_objetivo):
    torneo = random.sample(poblacion, k=3)
    torneo.sort(key=lambda params: fitness_parametros(params,N, matriz_vecindad, flujo_objetivo))
    return torneo[0]

# Cruce de dos individuos
def cruce(padre1, padre2):
    punto_cruce = random.randint(1, 3)  # Cruce entre parámetros
    hijo = padre1[:punto_cruce] + padre2[punto_cruce:]
    return hijo

def mutacion(individuo):
    for i in range(len(individuo)):
        if random.random() < MUTATION_RATE:
            if i == 0:  # MUTAR NUM_RUTAS
                individuo[i] = random.randint(NUM_RUTAS_MIN, NUM_RUTAS_MAX)
            elif i == 1:  # MUTAR LONG_MAX_RUTAS
                individuo[i] = random.randint(LONG_MAX_RUTAS_MIN, LONG_MAX_RUTAS_MAX)
            elif i == 2 or i == 3:  # MUTAR AUTOS_POR_RUTA_MIN o AUTOS_POR_RUTA_MAX
                individuo[i] = random.randint(AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX)
    return individuo


