import xml.etree.ElementTree as ET
import subprocess

def editar_tiempos_semaforos(vector_tiempos,archivo_xml="../sumo/test.net.xml"):
    """
    Edita el archivo XML de SUMO para actualizar los tiempos y estados de los semáforos.
    Si faltan fases en algún semáforo, las agrega con valores por defecto.
    
    Args:
    archivo_xml (str): Ruta del archivo XML a modificar.
    vector_tiempos (list of tuple): Lista de tuplas, donde cada tupla contiene dos enteros.
                                    El primer entero es el tiempo de verde y el segundo es el tiempo de rojo.
    """
    # Cargar el archivo XML
    tree = ET.parse(archivo_xml)
    root = tree.getroot()

    # Iterar sobre el vector de tiempos y actualizar cada semáforo
    for idx, (verde, rojo) in enumerate(vector_tiempos):
        semaforo_id = f"S{idx+1}"
        tlLogic = root.find(f".//tlLogic[@id='{semaforo_id}']")
        
        if tlLogic is not None:
            # Obtener las fases existentes o agregar las que falten
            phases = tlLogic.findall("phase")
            while len(phases) < 4:
                # Agregar fase por defecto hasta que haya 4
                new_phase = ET.Element("phase", duration="0", state="rrrr")
                tlLogic.append(new_phase)
                phases = tlLogic.findall("phase")
                print(phases)

            # Actualizar la duración y el estado de cada fase
            phases[0].set("duration", str(verde))  # Verde
            phases[0].set("state", "GGrr")
            
            phases[1].set("duration", "3")         # Amarillo
            phases[1].set("state", "yyrr")
            
            phases[2].set("duration", str(rojo))   # Rojo
            phases[2].set("state", "rrGG")
            
            phases[3].set("duration", "3")         # Amarillo en sentido opuesto
            phases[3].set("state", "rryy")

    # Guardar los cambios en el archivo XML
    tree.write(archivo_xml, encoding="utf-8", xml_declaration=True)
    #print(f"Archivo {archivo_xml} actualizado con los nuevos tiempos y estados de semáforos.")

# Ejemplo de uso
#vector_tiempos = [(42, 30), (50, 40), (60, 45)]
#editar_tiempos_semaforos(vector_tiempos)



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
