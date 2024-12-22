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
def get_grid(x, y):
    return grid[y][x]

def set_grid(x, y, v):
    grid[y][x] = v


# Parse data
byte_coords = []
for line in data.strip().split('\n'):
    x, y = [int(v) for v in line.split(',')]
    byte_coords.append((x, y))

for _ in range(1024):
    b = byte_coords.pop(0)
    set_grid(*b, '#')

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
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        new_p = (new_x, new_y)
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and new_p in to_visit:
            new_d = d + 1
            if new_d < distances[new_p]:
                distances[new_p] = new_d
                previous[new_p] = current

# Part 1: shortest path out
print(f"Shortest path: {shortest_path}")

# Fill function to see if we can reach exit
def can_reach_exit(n):
    to_fill = [start]

    while to_fill:
        x, y = to_fill.pop(0)
        set_grid(x, y, n)
        if (x, y) == end:
            return True

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and get_grid(new_x, new_y) not in ('#', n):
                to_fill.insert(0, (new_x, new_y))

    return False

# Start dropping more bytes
n = 0  # fill value, so that we don't need to copy the grid all the time
while can_reach_exit(n):
    b = byte_coords.pop(0)
    set_grid(*b, '#')
    n += 1

# Part 2: coordinates of blocking byte
print(f"Blocking byte coordinates: {','.join(str(x) for x in b)}")
