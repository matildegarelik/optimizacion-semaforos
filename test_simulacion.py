import pygame
import random
import sys

# Configuración básica
pygame.init()
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Tráfico con Direcciones y Doblado Controlado")
FPS = 30
GRID_SIZE = 10
BLOCK_SIZE = WIDTH // (GRID_SIZE + 1)
STREET_WIDTH = BLOCK_SIZE // 4
CAR_SPAWN_RATE = 0.1  # Probabilidad de generación de autos

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CAR_COLOR = (0, 0, 255)

CAR_SPEED = 2

# Tasa de tráfico para cada calle
TRAFFIC_RATE = [[random.uniform(1, 10) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Direcciones de las calles en el grid
HORIZONTAL_DIRECTION = [1 if i % 2 == 0 else -1 for i in range(GRID_SIZE)]
VERTICAL_DIRECTION = [1 if j % 2 == 0 else -1 for j in range(GRID_SIZE)]

class Car:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        # Avanza en la dirección actual
        if self.direction == "right":
            self.x += CAR_SPEED
        elif self.direction == "left":
            self.x -= CAR_SPEED
        elif self.direction == "up":
            self.y -= CAR_SPEED
        elif self.direction == "down":
            self.y += CAR_SPEED

        # Alcanza una intersección, evalúa si dobla o sigue recto
        if self.is_at_intersection():
            self.decide_turn()

    def is_at_intersection(self):
        # Verifica si el auto está en el centro de una intersección
        return self.x % (BLOCK_SIZE + STREET_WIDTH) < CAR_SPEED and self.y % (BLOCK_SIZE + STREET_WIDTH) < CAR_SPEED

    def decide_turn(self):
        x_index = self.x // (BLOCK_SIZE + STREET_WIDTH)
        y_index = self.y // (BLOCK_SIZE + STREET_WIDTH)
        
        # Probabilidad de doblar basada en la tasa de tráfico de la calle actual
        forward_traffic_rate = TRAFFIC_RATE[x_index][y_index]
        turn_traffic_rate = TRAFFIC_RATE[(x_index + VERTICAL_DIRECTION[y_index]) % GRID_SIZE][(y_index + HORIZONTAL_DIRECTION[x_index]) % GRID_SIZE]
        
        if random.random() < turn_traffic_rate:  # Si decide doblar
            # Decide doblar en función de la dirección actual
            if self.direction in ["right", "left"]:  # Está en una calle horizontal
                if VERTICAL_DIRECTION[y_index] == 1:  # Calle vertical va hacia abajo
                    self.direction = "down"
                else:  # Calle vertical va hacia arriba
                    self.direction = "up"
            else:  # Está en una calle vertical
                if HORIZONTAL_DIRECTION[x_index] == 1:  # Calle horizontal va hacia la derecha
                    self.direction = "right"
                else:  # Calle horizontal va hacia la izquierda
                    self.direction = "left"
        # Si no dobla, sigue en la misma dirección

    def draw(self, screen):
        pygame.draw.rect(screen, CAR_COLOR, (self.x, self.y, BLOCK_SIZE // 5, BLOCK_SIZE // 5))

class TrafficLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "red"
        self.cycle = 0
        self.change_interval = random.randint(90, 180)

    def update(self):
        self.cycle += 1
        if self.cycle >= self.change_interval:
            self.state = "green" if self.state == "red" else "red"
            self.cycle = 0
            self.change_interval = random.randint(90, 180)

    def draw(self, screen):
        color = GREEN if self.state == "green" else RED
        pygame.draw.circle(screen, color, (self.x, self.y), STREET_WIDTH // 2)

def draw_grid():
    # Dibuja las manzanas y calles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Dibuja cada manzana como un bloque
            pygame.draw.rect(SCREEN, BLACK, 
                             (col * (BLOCK_SIZE + STREET_WIDTH) + STREET_WIDTH,
                              row * (BLOCK_SIZE + STREET_WIDTH) + STREET_WIDTH,
                              BLOCK_SIZE, BLOCK_SIZE))

def spawn_car():
    # Selecciona una calle aleatoria para generar un auto
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)
    rate = TRAFFIC_RATE[x][y]
    
    if random.random() < rate * CAR_SPAWN_RATE:
        # Direccion inicial basada en la orientacion de la calle
        if random.choice([True, False]):  # Elige si el auto empieza en una calle horizontal o vertical
            if HORIZONTAL_DIRECTION[x] == 1:
                direction = "right"
                start_x, start_y = x * (BLOCK_SIZE + STREET_WIDTH), y * (BLOCK_SIZE + STREET_WIDTH) + STREET_WIDTH // 2
            else:
                direction = "left"
                start_x, start_y = (x + 1) * (BLOCK_SIZE + STREET_WIDTH), y * (BLOCK_SIZE + STREET_WIDTH) + STREET_WIDTH // 2
        else:
            if VERTICAL_DIRECTION[y] == 1:
                direction = "down"
                start_x, start_y = x * (BLOCK_SIZE + STREET_WIDTH) + STREET_WIDTH // 2, y * (BLOCK_SIZE + STREET_WIDTH)
            else:
                direction = "up"
                start_x, start_y = x * (BLOCK_SIZE + STREET_WIDTH) + STREET_WIDTH // 2, (y + 1) * (BLOCK_SIZE + STREET_WIDTH)

        return Car(start_x, start_y, direction)
    return None

def main():
    clock = pygame.time.Clock()
    cars = []
    traffic_lights = [TrafficLight((x + 1) * (BLOCK_SIZE + STREET_WIDTH) - STREET_WIDTH // 2,
                                   (y + 1) * (BLOCK_SIZE + STREET_WIDTH) - STREET_WIDTH // 2)
                      for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

    running = True
    while running:
        SCREEN.fill(WHITE)
        draw_grid()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar semáforos
        for light in traffic_lights:
            light.update()
            light.draw(SCREEN)

        # Generar autos nuevos
        if random.random() < CAR_SPAWN_RATE:  # Generación de autos
            car = spawn_car()
            if car:
                cars.append(car)

        # Mover y dibujar autos
        for car in cars:
            car.move()
            car.draw(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
