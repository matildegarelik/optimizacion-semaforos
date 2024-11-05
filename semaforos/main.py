from utils import entrenar
from editar_sumo import editar_tiempos_semaforos, ejecutar_simulacion

def codificar(vt): # recibe vector con tiempos semáforo entre 0 y 64 = 6 bits por semaforo => 12 bits por inters
    binario = ''.join(f'{x:06b}{y:06b}' for x, y in vt)
    return binario

# decodificar el binario a la lista original de tuplas
def decodificar(binario):
    tuplas = [(int(binario[i:i+6], 2), int(binario[i+6:i+12], 2)) for i in range(0, len(binario), 12)]
    return tuplas

def funcion_aptitud(individuo):
    vt = decodificar(individuo)
    # pasar tiempos semáforo a SUMO
    editar_tiempos_semaforos(vt)
    # obtener datos de SUMO
    waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()

    f= - avg_speed + waiting_time_per_vehicle # es lo que se busca minimizar
    return f


ind, it_ev, progreso, mejor_aptitud =  entrenar(
    funcion_aptitud,cantidad_poblacion=10,
    tipo_reemplazo='ELITISMO',
    aptitud_requerida=1400
)
sol = decodificar(ind)
print(f"Algoritmo Genético: x = {sol}, f(x) = {mejor_aptitud} Iteraciones: {it_ev}")
