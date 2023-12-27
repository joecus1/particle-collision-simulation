from config import *
import model

class Renderer:
    def __init__(self, surface: pg.Surface):
        self.surface = surface
    
    def draw(self, particles: list[model.Particle]):
        self.surface.fill(BLACK)
        for particle in particles:
            center = (particle.x, particle.y)
            pg.draw.circle(self.surface, GREEN, center, PARTICLE_SIZE)

        pg.display.update()

        