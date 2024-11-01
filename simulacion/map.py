# map.py

import pygame
import random
from config import BLOCK_SIZE, STREET_WIDTH, TRAFFIC_LIGHT_POSITIONS,  WIDTH, rows, cols, HEIGHT, FPS, CAR_SIZE
from car import Car
from traffic_light import TrafficLight

def create_cars(column_directions, row_directions):
    cars = []
    for row in range(3):
        for col in range(3):
            dir_x = column_directions[col] if random.choice([True, False]) else 0
            dir_y = row_directions[row] if dir_x == 0 else 0

            car_x = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2 + random.randint(0, STREET_WIDTH - 5)
            car_y = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2 + random.randint(0, STREET_WIDTH - 5)

            cars.append(Car(car_x, car_y, dir_x, dir_y))
    return cars

def create_traffic_lights(column_directions, row_directions):
    traffic_lights = []
    for pos in TRAFFIC_LIGHT_POSITIONS:
        col, row = pos
        x = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
        y = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2

        if row_directions[row] == 1:
            traffic_lights.append(TrafficLight(x - STREET_WIDTH, y, 'green'))
        else:
            traffic_lights.append(TrafficLight(x + STREET_WIDTH, y, 'green'))

        if column_directions[col] == 1:
            traffic_lights.append(TrafficLight(x, y - STREET_WIDTH, 'red'))
        else:
            traffic_lights.append(TrafficLight(x, y + STREET_WIDTH, 'red'))

    return traffic_lights

def draw_map(screen, cols, rows):
    for row in range(rows):
        for col in range(cols):
            x = col * BLOCK_SIZE
            y = row * BLOCK_SIZE

            pygame.draw.rect(screen, (200, 200, 200), (x, y + (BLOCK_SIZE - STREET_WIDTH) // 2, BLOCK_SIZE, STREET_WIDTH))
            pygame.draw.rect(screen, (200, 200, 200), (x + (BLOCK_SIZE - STREET_WIDTH) // 2, y, STREET_WIDTH, BLOCK_SIZE))


def generate_cars(cars, tasa_generacion, column_directions, row_directions):
    for borde, tasa in tasa_generacion.items():
        if random.random() < tasa / FPS:
            # Generar desde el borde izquierdo
            if borde == 'izquierda':

                row = random.randint(0, rows-1)
                while row_directions[row] != 1:
                    row = random.randint(0, rows-1)  # Solo generar en filas con dirección hacia la derecha

                y = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
                cars.append(Car(0, y, 1, 0))  # Dirección hacia la derecha
                        

            # Generar desde el borde derecho
            elif borde == 'derecha':
                row = random.randint(0, rows-1)
                while row_directions[row] != -1:
                    row = random.randint(0, rows-1)  # Solo generar en filas con dirección hacia la izquierda
                y = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
                cars.append(Car(WIDTH - CAR_SIZE, y, -1, 0))  # Dirección hacia la izquierda

            # Generar desde el borde superior
            elif borde == 'superior':
                col = random.randint(0, cols-1)
                while column_directions[col] != 1:
                    col = random.randint(0, cols-1)  # Solo generar en columnas con dirección hacia abajo
                x = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
                cars.append(Car(x, 0, 0, 1))  # Dirección hacia abajo
                

            # Generar desde el borde inferior
            elif borde == 'inferior':
                col = random.randint(0, cols-1)
                while column_directions[col] != -1:
                    col = random.randint(0, cols-1) # Solo generar en columnas con dirección hacia arriba
                x = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
                cars.append(Car(x, HEIGHT - CAR_SIZE, 0, -1))  # Dirección hacia arriba
                        
    return cars

def draw_flow_indicators(screen, flujos_acumulados, flujo_objetivo):
    for row in range(rows):
        for col in range(cols):
            # Posición del indicador en la esquina superior izquierda de la manzana
            x = col * BLOCK_SIZE + 10  # Margen desde la izquierda
            y = row * BLOCK_SIZE + 10  # Margen desde arriba

            flujo_actual = flujos_acumulados[row][col]
            objetivo = flujo_objetivo[row][col]

            # Dibuja el rectángulo de fondo
            #pygame.draw.rect(screen, (100, 100, 100), (x, y, 40, 40))
            font = pygame.font.Font(None, 8)

            # Dibuja el texto del flujo actual y objetivo
            current_text = f"Actual: {flujo_actual}"
            target_text = f"Objetivo: {objetivo}"
            current_surface = font.render(current_text, True, (0, 0, 0))
            target_surface = font.render(target_text, True, (0, 0, 0))

            screen.blit(current_surface, (x + 5, y + 5))  # Dibuja el flujo actual
            screen.blit(target_surface, (x + 5, y + 25))  # Dibuja el objetivo
