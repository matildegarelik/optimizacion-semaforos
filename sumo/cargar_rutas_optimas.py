import os
import sys
import optparse
import xml.etree.ElementTree as ET


mejor_rutas = []
mejor_autos_por_ruta = []

# Leer el archivo y extraer datos
with open("../rutas_optimas/resultados.txt", "r") as archivo:
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


SUMO_HOME= "C:\Program Files (x86)\Eclipse\Sumo\\"
tools = os.path.join(SUMO_HOME, 'tools')
sys.path.append(tools)


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


import xml.etree.ElementTree as ET

def extraer_nodos_edges(net_file):
    tree = ET.parse(net_file)
    root = tree.getroot()
    
    node_edges = {}
    
    for edge in root.findall('edge'):
        edge_id = edge.get('id')
        from_node = edge.get('from')
        to_node = edge.get('to')
        
        if from_node and from_node.startswith('J'):
            if from_node not in node_edges:
                node_edges[from_node] = []
            node_edges[from_node].append(edge_id)
        
        if to_node and to_node.startswith('J'):
            if to_node not in node_edges:
                node_edges[to_node] = []
            node_edges[to_node].append(edge_id)
    
    node_edges = {key: node_edges[key] for key in sorted(node_edges.keys(), key=lambda x: int(x[1:]))}

    return node_edges

edges_per_junction = extraer_nodos_edges('test.net.xml')


def obtener_edges_por_ruta(nodos_rutas, edges_per_junction):
    rutas_edges = []
    
    for i, ruta in enumerate(nodos_rutas):
        edges = []
        ruta_valida = True  # Marcador para validar la ruta
        
        for j in range(len(ruta) - 1):
            nodo_actual = f"J{ruta[j]}"
            nodo_siguiente = f"J{ruta[j + 1]}"
            
            # Buscar un edge que conecte el nodo actual con el siguiente
            edges_conectados = edges_per_junction.get(nodo_actual, [])
            edge_encontrado = None
            
            for edge in edges_conectados:
                # Verificamos si el edge conecta al nodo siguiente
                if edge in edges_per_junction.get(nodo_siguiente, []):
                    edge_encontrado = edge
                    break
            
            if edge_encontrado:
                edges.append(edge_encontrado)
            else:
                print(f"Advertencia: No se encontró conexión entre {nodo_actual} y {nodo_siguiente} en la ruta {i}. Ruta omitida.")
                ruta_valida = False
                break
        
        # Solo agregar la ruta si es válida
        if ruta_valida:
            rutas_edges.append(edges)
    
    return rutas_edges

rutas_edges= obtener_edges_por_ruta(mejor_rutas, edges_per_junction)

#@TODO: ELIMINAR RUTAS INVALIDAS AUTOMATICAMENTE
del rutas_edges[8]
del rutas_edges[1]

def prettify(element, level=0):
    """Agrega indentación a un elemento y sus hijos para mejorar la legibilidad."""
    indent = "\n" + "  " * level
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + "  "
        for child in element:
            prettify(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    if level and (not element.tail or not element.tail.strip()):
        element.tail = indent
    return element

def agregar_rutas_y_flows(xml_file, rutas_edges, autos_por_ruta):
    # Cargar el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Eliminar todas las rutas y flujos existentes
    for elemento in root.findall("route") + root.findall("flow"):
        root.remove(elemento)
    
    # Agregar nuevas rutas y flujos
    for i, (edges, autos) in enumerate(zip(rutas_edges, autos_por_ruta)):
        # Crear la nueva ruta
        nueva_ruta = ET.Element("route")
        nueva_ruta.set("id", f"r_{i}")
        nueva_ruta.set("edges", " ".join(edges))
        
        # Crear el nuevo flujo asociado
        nuevo_flow = ET.Element("flow")
        nuevo_flow.set("id", f"f_{i}")
        nuevo_flow.set("begin", "0.00")
        nuevo_flow.set("end", "3600.00")
        nuevo_flow.set("route", nueva_ruta.get("id"))
        nuevo_flow.set("number", str(autos))
        
        # Agregar ruta y flujo al root del XML
        root.append(nueva_ruta)
        root.append(nuevo_flow)

    # Guardar los cambios en el archivo XML
    prettify(root)
    tree.write(xml_file, encoding="UTF-8", xml_declaration=True)
    print(f"Se han reemplazado todas las rutas y flujos en {xml_file}")

agregar_rutas_y_flows('test.rou.xml',rutas_edges,mejor_autos_por_ruta)