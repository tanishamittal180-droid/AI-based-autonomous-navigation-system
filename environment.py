"""Repeatable grid-world generation and map helpers."""
import random
from .config import GRID_HEIGHT, GRID_WIDTH, OBSTACLE_DENSITY, RANDOM_SEED, START, GOAL
from .planner import Point


def make_obstacles(width=GRID_WIDTH, height=GRID_HEIGHT, density=OBSTACLE_DENSITY, seed=RANDOM_SEED) -> set[Point]:
    rng = random.Random(seed)
    obstacles: set[Point] = set()
    for y in range(height):
        for x in range(width):
            point = (x, y)
            if point not in (START, GOAL) and rng.random() < density:
                obstacles.add(point)
    # Keep a clear corridor so the default demo is reliably solvable.
    for x in range(min(START[0], GOAL[0]), max(START[0], GOAL[0]) + 1):
        obstacles.discard((x, START[1]))
    for y in range(min(START[1], GOAL[1]), max(START[1], GOAL[1]) + 1):
        obstacles.discard((GOAL[0], y))
    return obstacles
