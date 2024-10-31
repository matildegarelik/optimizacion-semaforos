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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

INTERSECTION_MARGIN = 2  # Un margen para considerar cercanía a la intersección
TRAFFIC_LIGHT_POSITIONS = [
    (1, 1),  # Semáforo en la intersección (1, 1)
    (2, 2),  # Semáforo en la intersección (2, 2)
    # Agrega más posiciones según sea necesario
]
