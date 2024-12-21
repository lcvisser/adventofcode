from math import prod

# Read data
input_file = "2024/14/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
GRID_WIDTH = 101
GRID_HEIGHT = 103

class Robot:
    def __init__(self, p0, v0):
        self._p0 = p0
        self._v0 = v0
        self.reset()

    def reset(self):
        self._px, self._py = self._p0
        self._vx, self._vy = self._v0

    def update(self, dt=1):
        self._px = (self._px + dt * self._vx) % GRID_WIDTH
        self._py = (self._py + dt * self._vy) % GRID_HEIGHT

    @property
    def position(self):
        return self._px, self._py


robots = []
for line in data.strip().split('\n'):
    pstr, vstr = line.split()
    p = [int(x) for x in pstr[2:].split(',')]
    v = [int(x) for x in vstr[2:].split(',')]
    robots.append(Robot(p,  v))

# Simulate
for i in range(len(robots)):
    robots[i].update(100)

# Define quadrants
q1_limits = [(0, GRID_WIDTH // 2), (0, GRID_HEIGHT // 2)]
q2_limits = [(GRID_WIDTH // 2 + 1, GRID_WIDTH), (0, GRID_HEIGHT // 2)]
q3_limits = [(0, GRID_WIDTH // 2), (GRID_HEIGHT // 2 + 1, GRID_HEIGHT)]
q4_limits = [(GRID_WIDTH // 2 + 1, GRID_WIDTH), (GRID_HEIGHT // 2 + 1, GRID_HEIGHT)]
quadrant_limits = [q1_limits, q2_limits, q3_limits, q4_limits]

# Count robots per quadrant
quadrant_counts = [0, 0, 0, 0]
for robot in robots:
    x, y = robot.position
    for q, limits in enumerate(quadrant_limits):
        xlim, ylim = limits
        xlim_min, xlim_max = xlim
        ylim_min, ylim_max = ylim

        if xlim_min <= x < xlim_max and ylim_min <= y < ylim_max:
            quadrant_counts[q] += 1
            break

# Part 1: product of number of robots per quadrant
print(f"Safety factor: {prod(quadrant_counts)}")

def print_grid(g):
    for row in g:
        print(''.join('.' if x == 0 else str(x) for x in row))
    print()

t_tree = 8159

grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
for i in range(len(robots)):
    robots[i].reset()
    robots[i].update(t_tree)
    x, y = robots[i].position
    grid[y][x] += 1

# Part 2: easter egg
print_grid(grid)
print(f"Time of easter egg: {t_tree}")
