from collections import Counter

# Read data
input_file = "2024/20/input.txt"
with open(input_file) as f:
    data = f.read()

data1 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

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
counter1 = Counter()
for p, pos in enumerate(nominal_route):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        dx2, dy2 = dx * 2, dy * 2
        try:
            if grid[x + dx][y + dy] == '#' and grid[x + dx2][y + dy2] != '#':
                end_of_cheat = (x + dx2, y + dy2)
                if end_of_cheat in nominal_route and nominal_route.index(end_of_cheat) > p:
                    saved = (nominal_route.index(end_of_cheat) - p) - 2  # minus 2 for taking the shortcut itself
                    counter1[saved] += 1
        except IndexError:
            pass  # out of grid

# Count cheats that save at least 100 picoseconds
n_cheats1 = 0
for saved, n in counter1.items():
    if saved >= 100:
        n_cheats1 += n

# Part 1: number of cheats that save at least 100 picoseconds
print(f"Number of cheats: {n_cheats1}")

# Helper function to compute cheat length
def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Find and count cheats with new rules
counter2 = Counter()
for p, pos1 in enumerate(nominal_route):
    print(f"{p} / {nominal_time}")
    end_of_cheats = filter(lambda pos2: dist(pos1, pos2) <= 20 and nominal_route.index(pos2) > p, nominal_route)
    for e in end_of_cheats:
        d = dist(pos1, e)
        saved = (nominal_route.index(e) - p) - d
        if saved >= 50:
            counter2[saved] += 1

# Count cheats that save at least 100 picoseonds
n_cheats2 = 0
for saved, n in counter2.items():
    if saved >= 100:
        n_cheats2 += n

# Part 2: number of cheats that save at least 100 picoseconds with the new rules
print(f"Number of cheats with new rules: {n_cheats2}")
