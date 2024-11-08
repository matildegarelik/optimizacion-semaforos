# optimizacion-semaforos
Optimizar tiempos de semáforos en función del tráfico

Pasos: 
1. Ejecutar rutas_optimas/rutas.py para encontrar parámetros y entrenar las rutas óptimas que simulen el flujo objetivo definido en ese archivo también
2. Ejecutar sumo/cargar_rutas_optimas.py para actualizar la red con el flujo a simular. Se lee para esto el archivo rutas_optimas/resultados.txt
3. Ejecutar semaforos/main.py para entrenar algoritmo y obtener mejores tiempos semáforos para mejorar fluidez tránsito.

pendientes: 
- arreglar hardcodeado sacar rutas invalidas en cargar rutas optimas
