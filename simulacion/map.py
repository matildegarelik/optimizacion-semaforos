# map.py

import pygame
import random
from config import BLOCK_SIZE, STREET_WIDTH, TRAFFIC_LIGHT_POSITIONS
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
