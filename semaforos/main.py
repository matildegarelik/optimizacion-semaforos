from utils import entrenar
from editar_sumo import ejecutar_simulacion, actualizar_fases_semaforos

def codificar(vt): # recibe vector con tiempos semáforo entre 0 y 64 = 6 bits por tiempo semaforo => 12 bits por semaforo
    binario = ''.join(f'{x:06b}{y:06b}' for x, y in vt)
    return binario

# decodificar el binario a la lista original de tuplas
def decodificar(binario):
    tuplas = [(int(binario[i:i+6], 2), int(binario[i+6:i+12], 2)) for i in range(0, len(binario), 12)]
    return tuplas

def funcion_aptitud(individuo):
    vt = decodificar(individuo)
    # pasar tiempos semáforo a SUMO
    actualizar_fases_semaforos(vt)
    # obtener datos de SUMO
    waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()

    f= + avg_speed - waiting_time_per_vehicle # es lo que se busca maximizar
    return f

def params_aptitud(individuo):
    vt = decodificar(individuo)
    # pasar tiempos semáforo a SUMO
    actualizar_fases_semaforos(vt)
    # obtener datos de SUMO
    waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()
    return avg_speed, waiting_time_per_vehicle


ind, it_ev, progreso, mejor_aptitud =  entrenar(
    funcion_aptitud,cantidad_poblacion=10,
    tipo_reemplazo='ELITISMO',
    aptitud_requerida=100,
    longitud=144,
    max_it=1, params_aptitud= params_aptitud
)
sol = decodificar(ind)
print(f"Algoritmo Genético: x = {sol}, f(x) = {mejor_aptitud} Iteraciones: {it_ev}")

"""
ejemplo_inicial = [(37, 52), (57, 34), (22, 8), (38, 40), (42, 24), (51, 58), (16, 34), (4, 55), (7, 24), (22, 61), (5, 1), (45, 35)]
actualizar_fases_semaforos(ejemplo_inicial)
waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()
print('---------------- SIN OPTIMIZACIÓN---------------------')
print(f"Tiempo espera total: {waiting_time}")
print(f"Tiempo espera x vehículo: {waiting_time_per_vehicle}")
print(f"Velocidad media vehículos: {avg_speed}")

sol = [(61, 18), (23, 3), (10, 3), (61, 4), (4, 15), (3, 13), (16, 4), (15, 51), (9, 2), (47, 15), (1, 6), (0, 2)]
actualizar_fases_semaforos(sol)
waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()
print('---------------- CON OPTIMIZACIÓN---------------------')
print(f"Tiempo espera total: {waiting_time}")
print(f"Tiempo espera x vehículo: {waiting_time_per_vehicle}")
print(f"Velocidad media vehículos: {avg_speed}")
"""
