"""A* grid path planner using Manhattan distance and four-way movement."""
from __future__ import annotations
import heapq
from typing import Iterable

Point = tuple[int, int]


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(point: Point, width: int, height: int) -> Iterable[Point]:
    x, y = point
    for candidate in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= candidate[0] < width and 0 <= candidate[1] < height:
            yield candidate


def astar(width: int, height: int, obstacles: set[Point], start: Point, goal: Point) -> list[Point]:
    """Return start-to-goal path (inclusive), or [] when no route exists."""
    if width < 1 or height < 1:
        raise ValueError("Grid width and height must be positive")
    for label, point in (("start", start), ("goal", goal)):
        if not (0 <= point[0] < width and 0 <= point[1] < height):
            raise ValueError(f"{label} is outside the grid: {point}")
    if start in obstacles or goal in obstacles:
        return []
    frontier: list[tuple[int, int, Point]] = [(manhattan(start, goal), 0, start)]
    came_from: dict[Point, Point | None] = {start: None}
    cost: dict[Point, int] = {start: 0}
    counter = 0
    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]  # type: ignore[assignment]
            return list(reversed(path))
        for nxt in neighbors(current, width, height):
            if nxt in obstacles:
                continue
            new_cost = cost[current] + 1
            if new_cost < cost.get(nxt, float("inf")):
                cost[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (new_cost + manhattan(nxt, goal), counter, nxt))
    return []
