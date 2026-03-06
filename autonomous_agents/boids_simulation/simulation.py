import numpy as np
from numpy.random import rand
import pygame
import random

from boid import Boid, Predator

WIDTH = 800
HEIGHT = 800
N_BOIDS = 100
N_PREDATORS = 3
BACKGROUND = (255, 255, 255)
TICK = 50

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Boids Simulation")

running = True
clock = pygame.time.Clock()

def get_boid():
    pos = np.random.randint(0, WIDTH, size=2).astype(np.float32)
    return Boid(pos, np.random.randn(2))

def get_predator():
    pos = np.random.randint(0, WIDTH, size=2).astype(np.float32)
    return Predator(pos, np.random.randn(2))

boids = [get_boid() for _ in range(N_BOIDS)]
predators = [get_predator() for _ in range(N_PREDATORS)]

time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND)

    pred_positions = set()
    eaten_boids = set()

    for pred in predators:
        pred.seek(boids)
        pred.repel(predators)
        pred.update()

        if pred.position[0] > WIDTH: pred.position[0] = 0
        if pred.position[0] < 0: pred.position[0] = WIDTH
        if pred.position[1] > HEIGHT: pred.position[1] = 0
        if pred.position[1] < 0: pred.position[1] = HEIGHT

        pred_positions.add((pred.position[0], pred.position[1]))
        pred.draw(screen)

    for i, boid in enumerate(boids):
        boid.flee(boids)
        boid.align(boids)
        boid.cohesion(boids)

        for pred in predators:
            boid.avoid(pred.position)
            diff = boid.position - pred.position
            dist = np.linalg.norm(diff)
            if dist < 10:
                eaten_boids.add(i)

        boid.update()

        if boid.position[0] > WIDTH: boid.position[0] = 0
        if boid.position[0] < 0: boid.position[0] = WIDTH
        if boid.position[1] > HEIGHT: boid.position[1] = 0
        if boid.position[1] < 0: boid.position[1] = HEIGHT

        boid.draw(screen)

    for i in eaten_boids:
        boids[i] = get_boid()

    time += 1
    if time == 100:
        boids[random.randint(0, len(boids))] = get_boid()
        time = 0

    pygame.display.flip()
    clock.tick(TICK)
