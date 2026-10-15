"""Run an interactive pygame simulation or generate a headless report."""
import argparse
from pathlib import Path
from src.config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, WINDOW_PADDING, FPS, MOVE_INTERVAL_MS, START, GOAL
from src.environment import make_obstacles
from src.planner import astar
from src.metrics import write_metrics
from src.visualization import save_map

ROOT = Path(__file__).resolve().parent


def run_headless(seed: int, density: float) -> int:
    obstacles = make_obstacles(density=density, seed=seed)
    path = astar(GRID_WIDTH, GRID_HEIGHT, obstacles, START, GOAL)
    image = save_map(path, obstacles, START, GOAL, GRID_WIDTH, GRID_HEIGHT, ROOT / "outputs" / "navigation_result.png")
    report = write_metrics(path, obstacles, START, GOAL, ROOT / "outputs" / "metrics.json")
    print("AI-Based Autonomous Navigation System")
    print(f"Mode: headless | Seed: {seed} | Obstacles: {len(obstacles)}")
    print(f"Algorithm: A* | Path found: {'yes' if path else 'no'}")
    print(f"Path nodes: {len(path)} | Movement steps: {len(path)-1 if path else 'N/A'}")
    print(f"Saved map: {image.relative_to(ROOT)}")
    print(f"Saved metrics: {report.relative_to(ROOT)}")
    return 0 if path and path[-1] == GOAL else 2


def run_gui(seed: int, density: float) -> int:
    try:
        import pygame
    except ImportError:
        print("pygame is missing. Run: pip install -r requirements.txt")
        return 1
    pygame.init()
    width_px = GRID_WIDTH * CELL_SIZE
    height_px = GRID_HEIGHT * CELL_SIZE
    screen = pygame.display.set_mode((width_px + WINDOW_PADDING * 2, height_px + 92))
    pygame.display.set_caption("AI-Based Autonomous Navigation System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)
    obstacles = make_obstacles(density=density, seed=seed)
    path = astar(GRID_WIDTH, GRID_HEIGHT, obstacles, START, GOAL)
    if not path:
        print("No path found. Try a lower --density value.")
    index = 0; last_move = 0; paused = False; completed = False
    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q): running = False
                elif event.key == pygame.K_SPACE: paused = not paused
                elif event.key == pygame.K_r:
                    index = 0; completed = False; paused = False; last_move = now
                elif event.key == pygame.K_s:
                    save_map(path, obstacles, START, GOAL, GRID_WIDTH, GRID_HEIGHT, ROOT / "outputs" / "navigation_result.png")
                    write_metrics(path, obstacles, START, GOAL, ROOT / "outputs" / "metrics.json")
                    print("Saved outputs/navigation_result.png and outputs/metrics.json")
        if not paused and path and not completed and now - last_move >= MOVE_INTERVAL_MS:
            if index < len(path) - 1: index += 1
            if index >= len(path) - 1: completed = True
            last_move = now
        screen.fill((248, 250, 252))
        ox, oy = WINDOW_PADDING, 68
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(ox + x*CELL_SIZE, oy + y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                color = (52, 64, 84) if (x,y) in obstacles else (235, 240, 246)
                pygame.draw.rect(screen, color, rect)
        if path:
            for x,y in path[:index+1]:
                pygame.draw.rect(screen, (132, 202, 255), (ox+x*CELL_SIZE+5, oy+y*CELL_SIZE+5, CELL_SIZE-11, CELL_SIZE-11), border_radius=4)
        for point, color in ((START,(18,183,106)), (GOAL,(240,68,56))):
            x,y = point
            pygame.draw.circle(screen, color, (ox+x*CELL_SIZE+CELL_SIZE//2, oy+y*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3)
        if path:
            x,y = path[min(index,len(path)-1)]
            pygame.draw.circle(screen, (21,112,239), (ox+x*CELL_SIZE+CELL_SIZE//2, oy+y*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//4)
        status = "DESTINATION REACHED" if completed else ("PAUSED" if paused else "NAVIGATING")
        title = font.render(f"A* Navigation | {status} | Steps: {max(0,index)} / {max(0,len(path)-1)}", True, (16,24,40))
        controls = font.render("SPACE: pause/resume   R: restart   S: save proof outputs   Q/ESC: quit", True, (52,64,84))
        screen.blit(title, (WINDOW_PADDING, 18)); screen.blit(controls, (WINDOW_PADDING, height_px+78))
        pygame.display.flip(); clock.tick(FPS)
    pygame.quit()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--headless", action="store_true", help="generate image and metrics without opening a window")
    parser.add_argument("--seed", type=int, default=7, help="random map seed for repeatable runs")
    parser.add_argument("--density", type=float, default=0.19, help="obstacle density between 0 and 0.45")
    args = parser.parse_args()
    if not 0 <= args.density <= 0.45:
        parser.error("--density must be between 0 and 0.45")
    return run_headless(args.seed, args.density) if args.headless else run_gui(args.seed, args.density)

if __name__ == "__main__":
    raise SystemExit(main())
