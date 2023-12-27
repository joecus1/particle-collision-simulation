from config import *
from renderer import Renderer
import model

pg.init()
surface = pg.display.set_mode(SCREEN_SIZE)
renderer = Renderer(surface)

running = True
world = model.World()

last_time = pg.time.get_ticks()
current_time = pg.time.get_ticks()
num_frames = 0
frame_time = 0

while running:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            running = False

    world.update_world(frame_time)
    renderer.draw(world.get_particles())

    current_time = pg.time.get_ticks()
    delta = current_time - last_time
    if (delta >= 1000):
        framerate = int(1000 * num_frames/delta)
        pg.display.set_caption(f"FPS: {framerate}")
        last_time = current_time
        num_frames = -1
        frame_time = float(1000.0 / max(1, framerate))

    num_frames += 1