import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


class GridPoint:
    def __init__(self, x, y, h, d):
        self.x = x
        self.y = y
        self.h = ord(h) - ord('a')
        self.dist = d
        self.prev = None


# Construct grid
start = None
finish = None
grid = []
for row, line in enumerate(data.strip().split('\n')):
    gridrow = []
    for col, h in enumerate(line):
        if h == 'S':
            start = (row, col)
            h = 'a'
            d = 0
        elif h == 'E':
            finish = (row, col)
            h = 'z'
            d = float("inf")
        else:
            d = float("inf")

        gridrow.append(GridPoint(row, col, h, d))

    grid.append(gridrow)

dim_x = len(grid)
dim_y = len(grid[1])

# Find path (Dijkstra)
sx, sy = start
grid[sx][sy].dist = 0

def get_neighbours(px, py, ph):
    potential_neighbours = [
        (px - 1, py),
        (px + 1, py),
        (px, py - 1),
        (px, py + 1)
    ]
    on_grid_neighbors = filter(lambda t: 0 <= t[0] < dim_x and 0 <= t[1] < dim_y, potential_neighbours)
    return filter(lambda t: grid[t[0]][t[1]].h <= ph + 1, on_grid_neighbors)

to_visit = []
for grid_row in grid:
    for p in grid_row:
        to_visit.append((p.x, p.y))

while to_visit:
    to_visit.sort(key=lambda p: grid[p[0]][p[1]].dist)
    cx, cy = to_visit.pop(0)
    if (cx, cy) == finish:
        break

    neighbours = get_neighbours(cx, cy, grid[cx][cy].h)
    for nx, ny in neighbours:
        new_dist = grid[cx][cy].dist + 1
        if new_dist < grid[nx][ny].dist:
            grid[nx][ny].dist = new_dist
            grid[nx][ny].prev = (cx, cy)

# Reconstruct the path
fx, fy = finish
u = finish
path = []
while u != start:
    path.insert(0, u)
    u = grid[u[0]][u[1]].prev

# Part 1: shortest path from S to E:
print(f"Shortest path length: {len(path)}")
