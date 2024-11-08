from utils import entrenar
from editar_sumo import ejecutar_simulacion, actualizar_fases_semaforos
from itertools import product

tiempos_posibles = [15, 35, 55]

def funcion_aptitud(vt):
    # pasar tiempos semáforo a SUMO
    actualizar_fases_semaforos(vt)
    # obtener datos de SUMO
    waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()

    f= + avg_speed - waiting_time_per_vehicle # es lo que se busca maximizar
    return f


def busqueda():
    mejor_vt = None
    mejor_aptitud = float('-inf')
    total_combinations = 4 ** 24  # Total de combinaciones posibles
    print_interval = 100000  # Imprime el progreso cada 100,000 combinaciones
    counter = 0

    # Generar todas las combinaciones posibles para las 12 tuplas
    for combinacion in product(product(tiempos_posibles, repeat=2), repeat=12):
        vt = list(combinacion)  # Cada combinacion es una lista de 12 tuplas
        aptitud = funcion_aptitud(vt)
        
        # Verificar si es la mejor combinación hasta ahora
        if aptitud > mejor_aptitud:
            mejor_aptitud = aptitud
            mejor_vt = vt

        # Contador y mensaje de progreso
        counter += 1
        if counter % print_interval == 0:
            progress = (counter / total_combinations) * 100
            print(f"Progreso: {progress:.6f}% completado, mejor aptitud hasta ahora: {mejor_aptitud} y vt={vt}")

    return mejor_vt, mejor_aptitud

# Ejecutar la búsqueda con seguimiento de progreso
mejor_combinacion, mejor_aptitud = busqueda()
print("Mejor combinación:", mejor_combinacion)
print("Mejor aptitud:", mejor_aptitud)