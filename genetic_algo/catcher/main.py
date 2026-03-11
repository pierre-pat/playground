import random

import numpy as np
import pygame
from constants import BACKGROUND, HEIGHT, MAX_MISS_TARGETS, POP_SIZE, TICK, WIDTH
from movers import Catcher, Target


def get_target():
    return Target(random.randint(100, WIDTH - 100))


def get_catcher():
    return Catcher(WIDTH / 2, y=HEIGHT - 20, width=40, height=20)


def calculate_fitness(catchers, target):
    for catcher in catchers:
        distance_bonus = 1 / (abs(catcher.x - target.x) + 1)
        catcher.fitness += (
            catcher.score + distance_bonus + 0.01 * catcher.total_movement
        )


def breed(parent1, parent2):
    child = get_catcher()
    mask1 = np.random.rand(*parent1.brain.w1.shape) > 0.5
    child.brain.w1 = np.where(mask1, parent1.brain.w1, parent2.brain.w1)

    mask2 = np.random.rand(*parent1.brain.w2.shape) > 0.5
    child.brain.w2 = np.where(mask2, parent1.brain.w2, parent2.brain.w2)
    return child


def create_new_population(catchers):
    weights = [max(0.0001, catcher.fitness) for catcher in catchers]

    elites = sorted(catchers, reverse=True, key=lambda c: c.fitness)[:2]
    print(f"Top 2: {elites[0].fitness} & {elites[1].fitness}")

    new_population = []
    for elite in elites:
        old_brain = elite.brain
        elite = get_catcher()
        elite.brain = old_brain
        new_population.append(elite)

    while len(new_population) < POP_SIZE:
        parent1, parent2 = random.choices(catchers, weights=weights, k=2)

        child = breed(parent1, parent2)

        if random.random() < 0.1:
            child.brain.w1 += np.random.randn(4, 6) * 0.1
            child.brain.w2 += np.random.randn(6, 3) * 0.1

        new_population.append(child)

    return new_population


def run_generation(catchers):
    missed_targets = 0
    targets = [get_target()]

    hit = set()

    while missed_targets < MAX_MISS_TARGETS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                missed_targets = MAX_MISS_TARGETS + 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    catchers[0].direction = -1
                elif event.key == pygame.K_RIGHT:
                    catchers[0].direction = 1
                elif event.key == pygame.K_DOWN:
                    catchers[0].direction = 0

        screen.fill(BACKGROUND)

        for target in targets[:]:
            target.update()
            target.draw(screen)

        if targets[-1].y >= HEIGHT // 3:
            targets.append(get_target())

        for catcher in catchers:
            if catcher.get_rect().colliderect(targets[0].get_rect()):
                if catcher not in hit:
                    hit.add(catcher)
                    catcher.score += 1

            state = np.array(
                [
                    catcher.x / WIDTH,
                    (catcher.x - targets[0].x) / WIDTH,
                    targets[0].y / HEIGHT,
                    1,
                ]
            )

            catcher.move(state)
            catcher.update()
            catcher.draw(screen)

        if targets[0].y > HEIGHT:
            for catcher in catchers:
                dist = abs(catcher.x - targets[0].x)
                catcher.fitness += 1 / (dist + 1)
            hit.clear()
            targets.pop(0)
            missed_targets += 1

        pygame.display.flip()
        clock.tick(TICK)

    calculate_fitness(catchers, targets[0])
    catchers = create_new_population(catchers)
    return catchers


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Genetic Catcher")

running = True
clock = pygame.time.Clock()

catchers = [get_catcher() for _ in range(POP_SIZE)]

eps = 1
while running:
    print("Generation ", eps)
    catchers = run_generation(catchers)
    eps += 1

pygame.quit()
