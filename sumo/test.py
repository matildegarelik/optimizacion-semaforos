import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


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

# contains TraCI control loop
def run():
    step = 0

    net_file = 'test.net.xml'
    
    edges_per_node = extraer_nodos_edges(net_file)

    flujo_por_nodo = {node: 0 for node in edges_per_node}

    intervalo = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        for node, edge_ids in edges_per_node.items():
            for edge_id in edge_ids:
                flujo_por_nodo[node] += traci.edge.getLastStepVehicleNumber(edge_id)

        if intervalo == 900: # a los 15 minutos (900 seg = 15 min)
            for node, total_flujo in flujo_por_nodo.items():
                flow_rate = total_flujo / intervalo
                print(f"Intersección: {node}, Flujo: {flow_rate}")
            print("--------------------------------------------------")
            flujo_por_nodo = {n: 0 for n in flujo_por_nodo}
            intervalo = 0

        intervalo += 1
        step += 1

    traci.close()
    sys.stdout.flush()



# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "test.sumocfg"])
    # traci.start([sumoBinary, "-c", "test.sumocfg", "--tripinfo-output", "tripinfo.xml"])
    run()