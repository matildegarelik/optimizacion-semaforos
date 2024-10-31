import random
import pygame
from config import WIDTH, HEIGHT, FPS, WHITE
from map import create_cars, create_traffic_lights, draw_map
from car import Car
from traffic_light import TrafficLight

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Mapa de Calles")
clock = pygame.time.Clock()

cols = WIDTH // 100
rows = HEIGHT // 100
column_directions = [random.choice([1, -1]) for _ in range(cols)]
row_directions = [random.choice([1, -1]) for _ in range(rows)]

cars = create_cars(column_directions, row_directions)
traffic_lights = create_traffic_lights(column_directions, row_directions)

running = True
while running:
    screen.fill(WHITE)

    draw_map(screen, cols, rows)

    for car in cars:
        car.move(traffic_lights, column_directions, row_directions)
        car.draw(screen)

    for traffic_light in traffic_lights:
        traffic_light.update()
        traffic_light.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
