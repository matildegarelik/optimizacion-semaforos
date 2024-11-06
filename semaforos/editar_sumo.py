import xml.etree.ElementTree as ET
import subprocess

def actualizar_fases_semaforos( vector_tiempos, archivo_xml="../sumo/test.net.xml"):
    # Cargar el archivo XML
    tree = ET.parse(archivo_xml)
    root = tree.getroot()
    
    # Iterar sobre cada tlLogic en el archivo XML
    for idx, tlLogic in enumerate(root.findall("tlLogic")):
        if idx >= len(vector_tiempos):
            break  # Evitar exceder el tamaño del vector
        
        verde, rojo = vector_tiempos[idx]
        verde +=1
        rojo +=1
        fases = list(tlLogic.findall("phase"))
        
        # Asignar tiempos de verde y rojo en las fases según el tipo de semáforo
        if len(fases) == 3:
            # Semáforos con 1 dirección
            fases[0].set("duration", str(verde))  # Fase en verde
            fases[1].set("duration", "3")         # Fase en amarillo
            fases[2].set("duration", str(rojo))   # Fase en rojo
        elif len(fases) == 4:
            # Semáforos con 2 direcciones
            fases[0].set("duration", str(verde))  # Fase en verde para una dirección
            fases[1].set("duration", "3")         # Fase en amarillo para una dirección
            fases[2].set("duration", str(rojo))   # Fase en verde para la otra dirección
            fases[3].set("duration", "3")         # Fase en amarillo para la otra dirección

    # Guardar los cambios en el mismo archivo XML
    tree.write(archivo_xml, encoding="utf-8", xml_declaration=True)
    #print(f"Archivo '{archivo_xml}' actualizado exitosamente.")


def ejecutar_simulacion(sumo_config="../sumo/test.sumocfg", tripinfo_output="../sumo/tripinfo.xml"):
    # Ejecutar la simulación de SUMO
    subprocess.run(["sumo", "-c", sumo_config, "--tripinfo-output", tripinfo_output])
    
    # Parsear tripinfo.xml para obtener las métricas
    tree = ET.parse(tripinfo_output)
    root = tree.getroot()
    
    total_waiting_time = 0.0
    total_route_length = 0.0
    total_duration = 0.0
    vehicle_count = 0

    # Recorrer cada vehículo en el archivo tripinfo.xml
    for tripinfo in root.findall('tripinfo'):
        waiting_time = float(tripinfo.get('waitingTime', 0))
        route_length = float(tripinfo.get('routeLength', 0))
        duration = float(tripinfo.get('duration', 0))
        
        total_waiting_time += waiting_time
        total_route_length += route_length
        total_duration += duration
        vehicle_count += 1

    # Calcular velocidad media en la red
    average_speed = total_route_length / total_duration if total_duration > 0 else 0

    # Calcular tiempo de espera por vehículo
    waiting_time_per_vehicle = total_waiting_time / vehicle_count if vehicle_count > 0 else 0

    return total_waiting_time, average_speed, waiting_time_per_vehicle

# Llamada a la función y resultados
#waiting_time, avg_speed, waiting_time_per_vehicle = ejecutar_simulacion()
#print(f"Suma de tiempos de espera: {waiting_time}")
#print(f"Velocidad media en la red: {avg_speed}")
#print(f"Tiempo de espera por vehículo: {waiting_time_per_vehicle}")
