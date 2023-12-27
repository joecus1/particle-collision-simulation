from config import *
import math

class Particle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.vx = 1 - 2 * random.random()
        self.vy = 1 - 2 * random.random()
        self.prev_collision = None

        colors = [WHITE, BLUE, GREEN, RED]
        self.color = colors[random.randint(0,3)]

    def calculate_distance(self, p1_x, p1_y, p2_x, p2_y):
        return math.sqrt(math.pow((p1_x - p2_x), 2) + math.pow((p1_y - p2_y), 2))


    def detect_collision(self, other, other_index):
        curr_distance = self.calculate_distance(self.x, self.y, other.x, other.y)

        if curr_distance <= PARTICLE_SIZE and other_index != self.prev_collision:
            self.prev_collision = other_index
            velocity_diff = (self.vx - other.vx, self.vy - other.vy)
            position_diff = (self.x - other.x, self.y - other.y)
            v_p_dotprod = velocity_diff[0] * position_diff[0] + velocity_diff[1] * position_diff[1]
            position_diff_mag_squared = math.pow(position_diff[0], 2) + math.pow(position_diff[1], 2)
            dot_prod_over_mag = v_p_dotprod / position_diff_mag_squared
            self.vx = self.vx - (dot_prod_over_mag * position_diff[0])
            self.vy = self.vy - (dot_prod_over_mag * position_diff[1])

    def detect_wall(self):
        r = (PARTICLE_SIZE * 0.5)
        if self.x <= 0 + r:
            self.x = r + 1
            self.vx = -self.vx
        if self.x >= SCREEN_WIDTH - r:
            self.x = SCREEN_WIDTH - r - 1
            self.vx = -self.vx
        if self.y <= 1:
            self.y = r + 1
            self.vy = -self.vy
        if self.y >= SCREEN_HEIGHT - r:
            self.y = SCREEN_HEIGHT - r - 1
            self.vy = -self.vy


class World:
    def __init__(self):
        self.particles = [Particle() for _ in range(NUM_PARTICLES)]
        self.update_quadrants()

    def get_particles(self):
        return self.particles
    
    def update_world(self, frame_time):
        self.update_velocities()
        self.update_positions(frame_time)
        self.update_quadrants()

    def update_velocities(self):
        for i, particle in enumerate(self.particles):
            row = int(particle.y // 100)
            column = int(particle.x // 100)
            for j in self.quadrants[row][column]:
                if i != j:
                    other_particle = self.particles[j]
                    particle.detect_collision(other_particle, j)
            particle.detect_wall()
    
    def update_positions(self, frame_time):
        for particle in self.particles:
            particle.x += particle.vx * (frame_time / 16.6)
            particle.y += particle.vy * (frame_time / 16.6)

    def update_quadrants(self):
        self.quadrants = []
        for i in range((SCREEN_HEIGHT // 100) + 1):
            self.quadrants.append([])
            for _ in range((SCREEN_WIDTH // 100) + 1):
                self.quadrants[i].append([])

        for i, particle in enumerate(self.particles):
            row = int(particle.y // 100)
            column = int(particle.x // 100)
            self.quadrants[row][column].append(i)


    
