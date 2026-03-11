import numpy as np
import pygame
from constants import WIDTH


class Target:
    def __init__(self, x, y=0, width=20, height=20, velocity=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = (255, 0, 0)

    def update(self):
        self.y += self.velocity

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())


class Brain:
    def __init__(self, n_in=4, n_hidden=6, n_out=3):
        self.w1 = np.random.randn(4, 6) * 0.5
        self.w2 = np.random.randn(6, 3) * 0.5

    def __call__(self, state):
        x = state @ self.w1
        x = np.tanh(x)
        return x @ self.w2


class Catcher:
    def __init__(self, x, y, width=40, height=20, velocity=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = 0
        self.color = (0, 0, 200, 20)
        self.alpha = 255
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        self.score = 0
        self.fitness = 0
        self.total_movement = 0
        self.brain = Brain()

    def move(self, state):
        output = self.brain(state)
        self.direction = output.argmax() - 1

    def update(self):
        old_x = self.x
        self.x += self.direction * self.velocity
        self.x = max(0, min(self.x, WIDTH - self.width))
        self.total_movement += abs(old_x - self.x)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
