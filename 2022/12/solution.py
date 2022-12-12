import sys
import copy

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


class GridPoint:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = ord(h) - ord('a')
        self.dist = float("inf")
        self.prev = None


# Construct grid
start = None
alt_starts = []
finish = None
grid0 = []
for row, line in enumerate(data.strip().split('\n')):
    gridrow = []
    for col, h in enumerate(line):
        if h == 'S':
            start = (row, col)
            h = 'a'
        elif h == 'a':
            alt_starts.append((row, col))
        elif h == 'E':
            finish = (row, col)
            h = 'z'

        gridrow.append(GridPoint(row, col, h))

    grid0.append(gridrow)

dim_x = len(grid0)
dim_y = len(grid0[1])

# Find path (Dijkstra)
def find_path(grid, sx, sy):
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
    u = finish
    path = []
    if grid[u[0]][u[1]].prev is not None:
        while u != (sx, sy):
            path.insert(0, u)
            u = grid[u[0]][u[1]].prev

        length_of_path = len(path)
    else:
        # Unreachable
        length_of_path = float("inf")

    return length_of_path

# Part 1: shortest path from S to E:
grid1 = copy.deepcopy(grid0)
grid1[start[0]][start[1]].dist = 0
print(f"Shortest path length: {find_path(grid1, *start)}")

# Part 2: shortest scenic path (brute force; the finish cannot be reached from many of the starting points, so it would
# be faster to ignore those)
path_lengths = []
all_starts = [start] + alt_starts
for i, s in enumerate(all_starts):
    gridx = copy.deepcopy(grid0)
    gridx[s[0]][s[1]].dist = 0
    length = find_path(gridx, *s)
    path_lengths.append(length)

    print(f"path {i} of {len(all_starts)}: {length}")

print(f"Shortest scenic path length: {min(path_lengths)}")
