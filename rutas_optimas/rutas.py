import numpy as np
import random
from entrenamiento_rutas import algoritmo_genetico
from entrenamiento_parametros import algoritmo_genetico_parametros

# Dimensiones y configuración
N = 4  # Tamaño del mapa (4x4)

# Inicializar matriz de vecindad
matriz_vecindad = np.array([
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#0  
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#1  bien
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#2  bien
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],#3  bien
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#4  bien
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#5  bien
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#6  bien
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],#7  bien
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#8  bien
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],#9  bien
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],#10 bien
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#11 
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],#12 bien
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],#13 bien
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],#14 bien 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0] #15 bien
])  #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15

# Flujo objetivo
# Flujo objetivo
flujo_objetivo_20s = np.array([
    [10, 15, 12, 8],
    [12, 14, 16, 13],
    [13, 16, 17, 12],
    [9, 7, 11, 14]
])
# Flujo objetivo x hora
flujo_objetivo = flujo_objetivo_20s * 30

# Ejecutar el algoritmo genético para ajustar parámetros
mejores_parametros = algoritmo_genetico_parametros(N, matriz_vecindad, flujo_objetivo)
print(f"\nMejores parámetros ajustados: {mejores_parametros}")

NUM_RUTAS = mejores_parametros[0]
LONG_MAX_RUTAS = mejores_parametros[1]
AUTOS_POR_RUTA_MIN = mejores_parametros[2]
AUTOS_POR_RUTA_MAX = mejores_parametros[3]
"""
NUM_RUTAS= 12
LONG_MAX_RUTAS= 8
AUTOS_POR_RUTA_MIN= 20
AUTOS_POR_RUTA_MAX= 100
"""
# Ejecutar el algoritmo genético
mejor_rutas, mejor_autos_por_ruta = algoritmo_genetico(N, NUM_RUTAS, LONG_MAX_RUTAS, AUTOS_POR_RUTA_MIN, AUTOS_POR_RUTA_MAX, matriz_vecindad, flujo_objetivo,
                       POPULATION_SIZE = 500, GENERATIONS = 500, MUTATION_RATE = 0.1)

# Resultados
print("\nMejor conjunto de rutas:")
for i, ruta in enumerate(mejor_rutas):
    print(f"Ruta {i+1}: {ruta} con {mejor_autos_por_ruta[i]} autos/hora")

# Guardar los mejores parámetros y rutas en un archivo de texto
with open("resultados.txt", "w") as archivo:
    archivo.write("Mejor conjunto de rutas:\n")
    for i, ruta in enumerate(mejor_rutas):
        archivo.write(f"Ruta {i+1}: {ruta} con {mejor_autos_por_ruta[i]} autos/hora\n")
    
    archivo.write("\nMejores parámetros ajustados:\n")
    archivo.write(f"NUM_RUTAS: {NUM_RUTAS}\n")
    archivo.write(f"LONG_MAX_RUTAS: {LONG_MAX_RUTAS}\n")
    archivo.write(f"AUTOS_POR_RUTA_MIN: {AUTOS_POR_RUTA_MIN}\n")
    archivo.write(f"AUTOS_POR_RUTA_MAX: {AUTOS_POR_RUTA_MAX}\n")

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