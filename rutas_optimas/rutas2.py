import numpy as np

# Dimensiones y configuración
N = 4  # Tamaño del mapa (4x4)

# Flujo objetivo
flujo_objetivo_20s = np.array([
    [10, 15, 12, 8],
    [12, 14, 16, 13],
    [13, 16, 17, 12],
    [9, 7, 11, 14]
])
# Flujo objetivo x hora
flujo_objetivo = flujo_objetivo_20s * 3 * 60

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
