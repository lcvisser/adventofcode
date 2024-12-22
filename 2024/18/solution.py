import math

# Read data
input_file = "2024/18/input.txt"
with open(input_file) as f:
    data = f.read()

# Define grid
WIDTH = 71
HEIGHT = 71

grid = [['.'] * WIDTH for _ in range(HEIGHT)]
start = (0, 0)
end = (WIDTH - 1, HEIGHT - 1)

# Helper functions
def set_grid(x, y, v):
    grid[y][x] = v


def print_grid(g):
    for row in g:
        print(''.join(row))
    print()


# Parse data
n = 0
for line in data.strip().split('\n'):
    x, y = [int(v) for v in line.split(',')]
    set_grid(x, y, '#')
    n += 1
    if n == 1024:
        break

# Dijkstra's algorithm to find the shortest path
distances = dict()
previous = dict()
to_visit = []

for y, row in enumerate(grid):
    for x, ch in enumerate(row):
        if ch == '.':
            p = (x, y)
            distances[p] = math.inf
            to_visit.append(p)

distances[start] = 0

shortest_path = math.inf
while to_visit:
    to_visit.sort(key=lambda p: distances[p])
    current = to_visit.pop(0)
    d = distances[current]

    if current == end:
        shortest_path = d
        break

    x, y = current
    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        new_p = (new_x, new_y)
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and new_p in to_visit:
            new_d = d + 1
            if new_d < distances[new_p]:
                distances[new_p] = new_d
                previous[new_p] = current

# Part 1: shortest path out
print(f"Shortest path: {shortest_path}")
