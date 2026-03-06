from sre_parse import REPEAT
import numpy as np
import pygame
import random

BOID_SIZE = 10
CLOSE_RANGE = 30
DISTANCE_RANGE = 80
REPEL_RANGE = 30
PRED_SIZE = 10
PRED_COLOR = (200, 0, 0)
MAX_SPEED = 5
MAX_PRED_SPEED = 6
MAX_FORCE = 0.2

def limit_vec(vec, max_val):
    mag = np.linalg.norm(vec)
    if mag > max_val:
        vec = (vec / mag) * max_val

    return vec


class Mover:
    def __init__(self, pos, acc):
        self.position = pos
        self.acceleration = acc
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.max_speed = MAX_SPEED

    def update(self):
        acc_mag = np.linalg.norm(self.acceleration)
        if acc_mag > MAX_FORCE:
            self.acceleration = (self.acceleration / acc_mag) * MAX_FORCE
        self.velocity += self.acceleration
        self.velocity = limit_vec(self.velocity, self.max_speed)

        self.position += self.velocity
        self.acceleration *= 0


class Boid(Mover):
    def __init__(self, pos, acc):
        super().__init__(pos, acc)

    def flee(self, others):
        count = 0
        steering = np.zeros((2,))
        for other in others:
            if self == other:
                continue

            diff = self.position - other.position
            distance = np.linalg.norm(diff)
            if distance < CLOSE_RANGE:
                diff /= distance
                steering += diff
                count += 1
        if count > 0:
            steering /= count
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.max_speed
                steering -= self.velocity
                steering = limit_vec(steering, MAX_FORCE)
            self.acceleration += steering

    def align(self, others):
        total_velocity = np.zeros((2,))
        count = 0
        for other in others:
            diff = self.position - other.position
            distance = np.linalg.norm(diff)
            if self != other and distance < DISTANCE_RANGE:
                total_velocity += other.velocity
                count += 1

        if count == 0:
            return

        total_velocity /= count

        mag = np.linalg.norm(total_velocity)

        if mag > 0:
            desired = (total_velocity / mag) * self.max_speed
            steering = desired - self.velocity
            steering = limit_vec(steering, MAX_FORCE)

            self.acceleration += steering

    def cohesion(self, others):
        avg_position = np.zeros((2,))
        count = 0
        for other in others:
            if self == other:
                continue
            diff = self.position - other.position
            distance = np.linalg.norm(diff)
            if distance < DISTANCE_RANGE:
                avg_position += other.position
                count += 1
        if count > 0:
            avg_position /= count
            desired = avg_position - self.position

            desired_mag = np.linalg.norm(desired)
            if desired_mag > 0:
                desired = (desired / desired_mag) * self.max_speed

                steering = desired - self.velocity
                steering = limit_vec(steering, MAX_FORCE)

                self.acceleration += steering

    def avoid(self, pos):
        diff = self.position - pos
        dist = np.linalg.norm(diff)
        if 0 < dist < DISTANCE_RANGE * 1.5:
            desired = (diff / dist) * self.max_speed
            steering = desired - self.velocity
            steering = limit_vec(steering, MAX_FORCE * 1.5)

            self.acceleration += steering

    def draw(self, screen):
        points = self._get_rotated_points()
        pygame.draw.polygon(screen, self.color, points)

    def _get_rotated_points(self):
        base_points = np.array([
            [BOID_SIZE, 0], # nose
            [-BOID_SIZE, -BOID_SIZE // 2], # rear left
            [-BOID_SIZE, BOID_SIZE // 2] # rear right
        ])

        angle = np.arctan2(self.velocity[1], self.velocity[0])
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array([
            [cos_a, -sin_a],
            [sin_a, cos_a]
        ])

        transformed_points = (base_points @ rotation_matrix.T) + self.position
        return transformed_points.tolist()

class Predator(Mover):
    def __init__(self, pos, acc):
        super().__init__(pos, acc)
        self.max_speed = MAX_PRED_SPEED

    def repel(self, predators):
        steering = np.zeros((2,))
        count = 0

        for pred in predators:
            if pred == self:
                continue
            diff = self.position - pred.position
            dist = np.linalg.norm(diff)
            if 0 < dist < REPEL_RANGE:
                push = (diff / dist) / dist
                steering += push
                count += 1

        if count > 0:
            steering /= count
            mag = np.linalg.norm(steering)
            if mag > 0:
                steering = (steering / mag) * self.max_speed
                self.acceleration += steering
                self.acceleration = limit_vec(self.acceleration, self.max_speed)

    def draw(self, screen):
        pygame.draw.circle(screen, PRED_COLOR, self.position.tolist(), radius=10)

    def seek(self, boids):
        closest_dist = float("inf")
        closest_pos = None
        for boid in boids:
            diff = boid.position - self.position
            dist = np.linalg.norm(diff)
            if dist < closest_dist:
                closest_dist = dist
                closest_pos = boid.position

        if closest_dist < DISTANCE_RANGE * 2.5:
            desired = closest_pos - self.position
            desired = (desired / closest_dist) * self.max_speed
            desired = limit_vec(desired, self.max_speed)
            steer = desired - self.velocity
            self.acceleration += steer
            self.acceleration = limit_vec(self.acceleration, self.max_speed)
        else:
            wander = np.array([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)])
            self.acceleration += wander
