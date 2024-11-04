import numpy as np
import random
from entrenamiento_rutas import algoritmo_genetico
from entrenamiento_parametros import algoritmo_genetico_parametros

# Dimensiones y configuración
N = 4  # Tamaño del mapa (4x4)

# Inicializar matriz de vecindad
matriz_vecindad = np.array([
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#0
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#1
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#2
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],#3
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#4
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#5
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#6
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],#7
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],#9
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],#10
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],#11
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],#12
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],#13
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],#14
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]#15
])


# Flujo objetivo
flujo_objetivo = np.random.randint(50, 100, size=(N, N))

import matplotlib.pyplot as plt
mejor_rutas = []
mejor_autos_por_ruta = []

# Leer el archivo y extraer datos
with open("resultados.txt", "r") as archivo:
    for linea in archivo:
        if "Ruta" in linea:
            # Extraer la ruta y el número de autos
            partes = linea.split(":")
            ruta_str = partes[1].split("con")[0].strip()  # Extraer solo la parte de la ruta
            ruta = list(map(int, ruta_str.strip("[]").split(", ")))  # Convertir a lista de enteros
            autos = int(partes[1].split("con")[1].strip().split()[0])  # Extraer número de autos
            mejor_rutas.append(ruta)
            mejor_autos_por_ruta.append(autos)
        elif "NUM_RUTAS" in linea:
            NUM_RUTAS = int(linea.split(":")[1].strip())
        elif "LONG_MAX_RUTAS" in linea:
            LONG_MAX_RUTAS = int(linea.split(":")[1].strip())
        elif "AUTOS_POR_RUTA_MIN" in linea:
            AUTOS_POR_RUTA_MIN = int(linea.split(":")[1].strip())
        elif "AUTOS_POR_RUTA_MAX" in linea:
            AUTOS_POR_RUTA_MAX = int(linea.split(":")[1].strip())
# Crear matriz de flujo real
flujo_real = np.zeros((N, N))
# Calcular flujo real basado en las mejores rutas y autos por ruta
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
