import pygame
import random
from config import BLOCK_SIZE, STREET_WIDTH, CAR_SIZE, TURN_PROBABILITY, TRAFFIC_LIGHT_POSITIONS, INTERSECTION_MARGIN, rows, cols

class Car:
    def __init__(self, x, y, dir_x, dir_y):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = 2
        self.is_currently_at_intersection = False
        self.is_stopped = False

    def move(self, traffic_lights, column_directions, row_directions, flujos_acumulados):

        if self.at_intersection(column_directions, row_directions, traffic_lights) or self.is_stopped:
            

            tli = self.find_traffic_light() * 2  # índice de semáforo
            if self.dir_y:
                tli += 1  # el segundo de la lista de semáforos es el que hay que ver, el primero es en x

            if (tli >= 0 and traffic_lights[tli].is_red()):
                # Si el semáforo está en rojo, detener el auto
                self.is_stopped = True  # Detener el auto
                return  flujos_acumulados# No mover el auto si el semáforo está en rojo
            else:
                self.is_stopped = False  # Si el semáforo está en verde, continuar el movimiento

                # actualizar flujo por interseccion
                col = int(self.x // BLOCK_SIZE)
                row = int(self.y // BLOCK_SIZE)
                if 0 <= row < rows and 0 <= col < cols:
                    flujos_acumulados[row][col] += 1

                self.x += self.dir_x * self.speed
                self.y += self.dir_y * self.speed
                self.make_decision(column_directions, row_directions)
        else:
            self.x += self.dir_x * self.speed
            self.y += self.dir_y * self.speed
        
        return flujos_acumulados

    def make_decision(self, column_directions, row_directions):
        if random.random() < TURN_PROBABILITY:
            if self.dir_x != 0:
                self.dir_x = 0
                col = int(self.x // BLOCK_SIZE)
                if col >= len(column_directions):
                    col = -1
                elif col<0:
                    col=0
                self.dir_y = column_directions[col]
            elif self.dir_y != 0:
                self.dir_y = 0
                row = int(self.y // BLOCK_SIZE)
                if row >= len(row_directions):
                    row = -1
                elif row<0:
                    row=0
                self.dir_x = row_directions[row]
            self.restrain_in_street()

    def at_intersection(self, column_directions, row_directions, traffic_lights):
        col = int(self.x // BLOCK_SIZE)
        row = int(self.y // BLOCK_SIZE)
        street_center_y = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
        street_center_x = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2

        in_horizontal_street = (self.dir_x != 0 and abs(self.x - street_center_x) <= INTERSECTION_MARGIN)
        in_vertical_street = (self.dir_y != 0 and abs(self.y - street_center_y) <= INTERSECTION_MARGIN)

        if (in_horizontal_street or in_vertical_street) and self.is_currently_at_intersection:
            return False
        elif (in_horizontal_street or in_vertical_street):
            self.is_currently_at_intersection = True
            return True
        else:
            self.is_currently_at_intersection = False
            return False

    def restrain_in_street(self):
        if self.dir_x != 0:
            street_center_y = (self.y // BLOCK_SIZE) * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
            self.y = street_center_y + (STREET_WIDTH - CAR_SIZE) // 2

        if self.dir_y != 0:
            street_center_x = (self.x // BLOCK_SIZE) * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
            self.x = street_center_x + (STREET_WIDTH - CAR_SIZE) // 2

    def find_traffic_light(self):
        col = int(self.x // BLOCK_SIZE)
        row = int(self.y // BLOCK_SIZE)
        position = (row, col)
        try:
            return TRAFFIC_LIGHT_POSITIONS.index(position)
        except ValueError:
            return -1

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, CAR_SIZE, CAR_SIZE))
