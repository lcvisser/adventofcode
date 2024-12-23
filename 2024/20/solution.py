from collections import Counter

# Read data
input_file = "2024/20/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse grid
grid = []
height = 0
width = 0
start = None
end = None
for r, row in enumerate(data.strip().split('\n')):
    height = r

    grid_row = []
    for c, ch in enumerate(row):
        width = c

        if ch == 'S':
            start = (r, c)
        elif ch == 'E':
            end = (r, c)

        grid_row.append(ch)

    grid.append(grid_row)

# Breadth-first search to find the nominal shortest route
def find_route(src, dst):
    to_visit = [(src, [src])]
    visited = set()
    while to_visit:
        curr, path = to_visit.pop(0)
        if curr == dst:
            return path

        if curr not in visited:
            visited.add(curr)
            x, y = curr
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if grid[new_x][new_y] != '#':
                    new_pos = (new_x, new_y)
                    new_path = path.copy() + [new_pos]
                    to_visit.append((new_pos, new_path))

# Determine nominal route
nominal_route = find_route(start, end)
nominal_time = len(nominal_route)

# Find and count cheats
counter = Counter()
for p, pos in enumerate(nominal_route):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        dx2, dy2 = dx * 2, dy * 2
        try:
            if grid[x + dx][y + dy] == '#' and grid[x + dx2][y + dy2] != '#':
                end_of_cheat = (x + dx2, y + dy2)
                if end_of_cheat in nominal_route and nominal_route.index(end_of_cheat) > p:
                    saved = (nominal_route.index(end_of_cheat) - p) - 2  # minus 2 for taking the shortcut itself
                    counter[saved] += 1
        except IndexError:
            pass  # out of grid

# Find cheats that save at least 100 picoseconds
n_cheats = 0
for saved, n in counter.items():
    if saved >= 100:
        n_cheats += n

# Part 1: number of cheats that save at least 100 picoseconds
print(f"Number of cheats: {n_cheats}")
