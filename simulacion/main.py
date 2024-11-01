import random
import pygame
from config import WIDTH, HEIGHT, FPS, WHITE, rows, cols, row_directions, column_directions, flujo_objetivo
from map import create_cars, create_traffic_lights, draw_map, generate_cars, draw_flow_indicators
from car import Car
from traffic_light import TrafficLight

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Mapa de Calles")
clock = pygame.time.Clock()

periodo_medicion = 100  # Cambia según la estabilidad que necesites
contador_ciclos = 0
flujos_acumulados = [[0 for _ in range(cols)] for _ in range(rows)]
flujos = [[0 for _ in range(cols)] for _ in range(rows)]
tasa_generacion = {'izquierda': 1, 'derecha': 1, 'superior': 1, 'inferior': 1}


#cars = create_cars(column_directions, row_directions)
cars=generate_cars([], tasa_generacion, column_directions, row_directions)
traffic_lights = create_traffic_lights(column_directions, row_directions)

running = True
while running:
    screen.fill(WHITE)

    draw_map(screen, cols, rows)
    cars=generate_cars(cars, tasa_generacion, column_directions, row_directions)


    for car in cars:
        flujos_acumulados = car.move(traffic_lights, column_directions, row_directions, flujos_acumulados)
        car.draw(screen)

    for traffic_light in traffic_lights:
        traffic_light.update()
        traffic_light.draw(screen)
    
    draw_flow_indicators(screen, flujos_acumulados, flujo_objetivo)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    contador_ciclos += 1

    # Ajustar el flujo cada "periodo_medicion" ciclos
    if contador_ciclos >= periodo_medicion:
        for row in range(rows):
            for col in range(cols):
                flujo_promedio = flujos_acumulados[row][col] / periodo_medicion
                desviacion = flujo_objetivo[row][col] - flujo_promedio

                # Ajuste de la tasa de generación en el borde correspondiente
                if col == 0:  # Borde izquierdo
                    tasa_generacion['izquierda'] += desviacion * 0.01
                elif col == cols - 1:  # Borde derecho
                    tasa_generacion['derecha'] += desviacion * 0.01
                if row == 0:  # Borde superior
                    tasa_generacion['superior'] += desviacion * 0.01
                elif row == rows - 1:  # Borde inferior
                    tasa_generacion['inferior'] += desviacion * 0.01

        # Reiniciar el acumulador y el contador
        flujos_acumulados = [[0 for _ in range(cols)] for _ in range(rows)]
        contador_ciclos = 0

        print('reinicio')


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
