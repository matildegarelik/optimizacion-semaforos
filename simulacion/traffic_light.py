import pygame

class TrafficLight:
    def __init__(self, x, y, state):
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

    def draw(self, screen):
        color = (0, 255, 0) if self.state == 'green' else (255, 0, 0)
        pygame.draw.rect(screen, color, (self.x, self.y, 10, 10))  # Ajusta el tamaño según sea necesario
