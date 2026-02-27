import pygame

from argparse import ArgumentParser

WIDTH = 600
HEIGHT = 600
N = 15
CELL_WIDTH = WIDTH // N
CELL_HEIGHT = HEIGHT // N
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND = (150, 150, 150)
TICK = 40

def is_valid_move(solution, i):
    if i in solution:
        return False
    for row, col in enumerate(solution):
        if abs(row - len(solution)) == abs(col - i):
            return False

    return True


def n_queens(solution, n):
    if len(solution) == n:
        yield solution
        return

    for i in range(n):
        if is_valid_move(solution, i):
            solution.append(i)
            yield solution
            yield from n_queens(solution, n)
            solution.pop()
            yield solution


def draw_board(screen):
    screen.fill(BACKGROUND)
    for i in range(N):
        pygame.draw.line(screen, BLACK, (i * CELL_WIDTH, 0), (i * CELL_WIDTH, HEIGHT), width=2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_HEIGHT), (WIDTH, i * CELL_HEIGHT), width=2)


def draw_solution(screen, solution):
    for row, col in enumerate(solution):

        center = (row * CELL_HEIGHT + CELL_HEIGHT // 2, col * CELL_WIDTH + CELL_WIDTH // 2)
        radius = CELL_WIDTH // 2 * 0.75
        pygame.draw.circle(screen, GREEN, center, radius, width=0)


pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("N Queens")

running = True
solver = n_queens([], N)
solution_found = False
solution = None
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while not solution_found:
        try:
            draw_board(screen)
            solution = next(solver)
            draw_solution(screen, solution)
            pygame.display.flip()
            if len(solution) == N:
                solution_found = True
        except StopIteration:
            print("Done.")

    draw_board(screen)
    draw_solution(screen, solution)
    pygame.display.flip()
    clock.tick(TICK)

pygame.quit()
