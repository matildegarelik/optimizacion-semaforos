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

    f= - waiting_time_per_vehicle # es lo que se busca maximizar
    return f

def params_aptitud(individuo):
    vt = decodificar(individuo)
    # pasar tiempos semáforo a SUMO
    actualizar_fases_semaforos(vt)
    # obtener datos de SUMO
    waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()
    return avg_speed, waiting_time_per_vehicle


ind, it_ev, progreso, mejor_aptitud, tiempo =  entrenar(
    funcion_aptitud,max_it=500,params_aptitud= params_aptitud,longitud=144,
    aptitud_requerida=-5, # justificación: porcentaje de reducción de 85%
    cantidad_poblacion=50,
    tasa_supervivencia=0.2, # porcentaje de padres que sobreviven en la próxima generación.
    tasa_mutacion=0.1
)
sol = decodificar(ind)
print(f"Algoritmo Genético: x = {sol}, f(x) = {mejor_aptitud}, Tiempo: {tiempo} seg")

"""
#ejemplo_inicial = [(29, 21), (56, 4), (28, 4), (40, 10), (30, 37), (44, 6), (32, 7), (8, 20), (48, 61), (62, 50), (61, 0), (40, 33)]
ejemplo_inicial = [(45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45), (45, 45)]
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