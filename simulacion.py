import pygame
import random

# Configuración de la ventana y el entorno
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 100  # Tamaño de cada manzana (cuadrícula)
STREET_WIDTH = 10  # Ancho de cada calle
CAR_SIZE = 5      # Tamaño de cada auto
FPS = 30
TURN_PROBABILITY = 0.99  # Probabilidad de girar en una intersección

# Colores básicos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Mapa de Calles")
clock = pygame.time.Clock()

# Creamos el mapa de direcciones por fila y columna
cols = WIDTH // BLOCK_SIZE
rows = HEIGHT // BLOCK_SIZE
column_directions = [random.choice([1, -1]) for _ in range(cols)]
row_directions = [random.choice([1, -1]) for _ in range(rows)]

INTERSECTION_MARGIN = 2  # Un margen para considerar cercanía a la intersección
TRAFFIC_LIGHT_POSITIONS = [
    (1, 1),  # Semáforo en la intersección (1, 1)
    (2, 2),  # Semáforo en la intersección (2, 2)
    # Agrega más posiciones según sea necesario
]


# Clase para el auto
class Car:
    def __init__(self, x, y, dir_x, dir_y):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = 2
        self.is_currently_at_intersection= False

    def move(self):
        # Tomar decisión si estamos en una intersección
       
        if self.at_intersection():
            tli = self.find_traffic_light() * 2 # indice de semaforo
            if self.dir_y:
                tli+=1 # el segundo de la lista de semaforos es el q hay q ver, el primero es en x
            
            if tli>=0 and traffic_lights[tli].is_red():
                # no mover si semaforo en rojo
                print('esperar') # espera a q se ponga en verde.
            else:
                # Mover el auto en la dirección permitida por la calle
                self.x += self.dir_x * self.speed
                self.y += self.dir_y * self.speed


                self.make_decision()
        else: 
            # Mover el auto en la dirección permitida por la calle
            self.x += self.dir_x * self.speed
            self.y += self.dir_y * self.speed


    def make_decision(self):
        # Si estamos en una intersección, decidir si girar o seguir
        if random.random() < TURN_PROBABILITY:
            # Elegir una nueva dirección de giro
            if self.dir_x != 0:
                self.dir_x = 0
                col = int(self.x // BLOCK_SIZE)
                if col >= len(column_directions):
                    col=-1
                self.dir_y = column_directions[col]
            elif self.dir_y != 0:
                self.dir_y = 0
                row = int(self.y // BLOCK_SIZE) 
                if row >= len(row_directions):
                    row=-1
                self.dir_x = row_directions[row]
            self.restrain_in_street()


    def at_intersection(self):
        # Calcular la posición en términos de "manzanas"
        col = int(self.x // BLOCK_SIZE)
        row = int(self.y // BLOCK_SIZE)
        
        
        # Calcular el centro de la calle de la manzana actual
        street_center_y = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
        street_center_x = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2 

        # Verificar si el auto está dentro del margen de una intersección
        in_horizontal_street = (
            self.dir_x != 0 and 
            abs(self.x - street_center_x) <= INTERSECTION_MARGIN
        )
        in_vertical_street = (
            self.dir_y != 0 and 
            abs(self.y - street_center_y) <= INTERSECTION_MARGIN
        )

       
        if((in_horizontal_street or in_vertical_street) and self.is_currently_at_intersection):
            return False # sino marca como cuatro veces q esta en una interseccion y solo haria falta una vez
        elif (in_horizontal_street or in_vertical_street):
            self.is_currently_at_intersection=True
            return True
        else:
            self.is_currently_at_intersection=False
            return False

    def restrain_in_street(self):
        # Si el auto se mueve en la dirección horizontal (x)
        if self.dir_x != 0:
            # Calcula el centro vertical de la calle en la manzana actual
            street_center_y = (self.y // BLOCK_SIZE) * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
            # Centra el auto en la posición 'y' de la calle
            self.y = street_center_y + (STREET_WIDTH - CAR_SIZE) // 2

        # Si el auto se mueve en la dirección vertical (y)
        if self.dir_y != 0:
            # Calcula el centro horizontal de la calle en la manzana actual
            street_center_x = (self.x // BLOCK_SIZE) * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2
            # Centra el auto en la posición 'x' de la calle
            self.x = street_center_x + (STREET_WIDTH - CAR_SIZE) // 2

    def find_traffic_light(self):
        col = int(self.x // BLOCK_SIZE)
        row = int(self.y // BLOCK_SIZE) 
        position=(row,col)
        try:
            return TRAFFIC_LIGHT_POSITIONS.index(position)
        except ValueError:
            return -1
        
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, CAR_SIZE, CAR_SIZE))

# Lista de autos en circulación
cars = []

# Creación de autos al azar en el mapa
for row in range(3):
    for col in range(3):
        dir_x = column_directions[col] if random.choice([True, False]) else 0
        dir_y = row_directions[row] if dir_x == 0 else 0

        car_x = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2 + random.randint(0, STREET_WIDTH - CAR_SIZE)
        car_y = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2 + random.randint(0, STREET_WIDTH - CAR_SIZE)

        cars.append(Car(car_x, car_y, dir_x, dir_y))
        #cars =[Car(car_x, car_y, dir_x, dir_y)]

class TrafficLight:
    def __init__(self, x, y,state):
        self.x = x
        self.y = y
        self.state = state  # Estado inicial
        self.timer = 0
        self.green_time = 150  # Tiempo para el verde
        self.red_time = 150   # Tiempo para el rojo

    def update(self):
        self.timer += 1
        if self.state == 'green' and self.timer > self.green_time:
            self.state = 'red'
            self.timer = 0
        elif self.state == 'red' and self.timer > self.red_time:
            self.state = 'green'
            self.timer = 0
    
    def is_green(self):
        return self.state == 'green'

    def is_red(self):
        return self.state == 'red'

    def draw(self):
        color = (0, 255, 0) if self.state == 'green' else (255, 0, 0)
        pygame.draw.rect(screen, color, (self.x, self.y, STREET_WIDTH, STREET_WIDTH))



# Crear una lista para almacenar los semáforos
traffic_lights = []

# Crear semáforos en las posiciones especificadas
for pos in TRAFFIC_LIGHT_POSITIONS:
    col, row = pos
    x = col * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2  # Centrar en la intersección
    y = row * BLOCK_SIZE + (BLOCK_SIZE - STREET_WIDTH) // 2

    if row_directions[row] == 1:
        traffic_lights.append(TrafficLight(x-STREET_WIDTH, y,'green'))
    else:
        traffic_lights.append(TrafficLight(x+STREET_WIDTH, y,'green'))
    if column_directions[col] == 1:
        traffic_lights.append(TrafficLight(x, y-STREET_WIDTH,'red'))
    else:
        traffic_lights.append(TrafficLight(x, y+STREET_WIDTH,'red'))

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Dibuja el mapa de calles (cuadrícula con calles de ancho definido)
    for row in range(rows):
        for col in range(cols):
            x = col * BLOCK_SIZE
            y = row * BLOCK_SIZE

            pygame.draw.rect(screen, GRAY, (x, y + (BLOCK_SIZE - STREET_WIDTH) // 2, BLOCK_SIZE, STREET_WIDTH))
            pygame.draw.rect(screen, GRAY, (x + (BLOCK_SIZE - STREET_WIDTH) // 2, y, STREET_WIDTH, BLOCK_SIZE))

    # Actualizar y dibujar autos
    for car in cars:
        car.move()
        car.draw()
    
    # Actualizar y dibujar semáforos
    for traffic_light in traffic_lights:
        traffic_light.update()
        traffic_light.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
