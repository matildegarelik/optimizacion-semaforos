import numpy as np
import random
from entrenamiento_rutas import algoritmo_genetico
from entrenamiento_parametros import algoritmo_genetico_parametros

# Dimensiones y configuración
N = 5  # Tamaño del mapa (5x5)

# Inicializar matriz de vecindad
matriz_vecindad = np.zeros((N * N, N * N), dtype=int)
for fila in range(N):
    for columna in range(N):
        indice_actual = fila * N + columna
        # Vecinos
        if fila > 0: matriz_vecindad[indice_actual][(fila - 1) * N + columna] = 1
        if fila < N - 1: matriz_vecindad[indice_actual][(fila + 1) * N + columna] = 1
        if columna > 0: matriz_vecindad[indice_actual][fila * N + (columna - 1)] = 1
        if columna < N - 1: matriz_vecindad[indice_actual][fila * N + (columna + 1)] = 1

# Flujo objetivo
flujo_objetivo = np.random.randint(50, 100, size=(N, N))

# Algoritmo Genético
POPULATION_SIZE = 500
GENERATIONS = 1000
MUTATION_RATE = 0.1

# Ejecutar el algoritmo genético para ajustar parámetros
mejores_parametros = algoritmo_genetico_parametros(N, matriz_vecindad, flujo_objetivo)
print(f"\nMejores parámetros ajustados: {mejores_parametros}")

NUM_RUTAS = mejores_parametros[0]
LONG_MAX_RUTAS = mejores_parametros[1]
AUTOS_POR_RUTA_MIN = mejores_parametros[2]
AUTOS_POR_RUTA_MAX = mejores_parametros[3]

# Ejecutar el algoritmo genético
mejor_rutas, mejor_autos_por_ruta = algoritmo_genetico(N, NUM_RUTAS, LONG_MAX_RUTAS, AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX, matriz_vecindad, flujo_objetivo,
                       POPULATION_SIZE = 500, GENERATIONS = 1000, MUTATION_RATE = 0.1)

# Resultados
print("\nMejor conjunto de rutas:")
for i, ruta in enumerate(mejor_rutas):
    print(f"Ruta {i+1}: {ruta} con {mejor_autos_por_ruta[i]} autos/hora")


import matplotlib.pyplot as plt

# Calcular flujo real basado en las mejores rutas y autos por ruta
flujo_real = np.zeros((N, N))
for i, ruta in enumerate(mejor_rutas):
    autos = mejor_autos_por_ruta[i]
    for nodo in ruta:
        fila, columna = divmod(nodo, N)
        flujo_real[fila, columna] += autos

# Crear el gráfico
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-1, N)
ax.set_ylim(-1, N)

# Graficar los nodos e incluir los números de nodo
for fila in range(N):
    for columna in range(N):
        nodo = fila * N + columna
        x, y = columna, N - fila - 1  # Para visualizar como matriz
        ax.text(x, y, str(nodo), fontsize=6, ha='center', va='center', color='grey')  # Número de nodo en gris
        ax.text(x, y - 0.3, f"Obj: {flujo_objetivo[fila, columna]}", fontsize=8, ha='center', color='blue')  # Flujo objetivo
        ax.text(x, y - 0.6, f"Real: {int(flujo_real[fila, columna])}", fontsize=8, ha='center', color='red')  # Flujo real

# Configuración visual
ax.grid(True)
ax.set_xticks(range(N))
ax.set_yticks(range(N))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_title("Mapa de nodos con Flujo Objetivo y Flujo Real")

plt.show()