import itertools
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
grid = []
start = None
for r, line in enumerate(data.strip().split('\n')):
    if 'S' in line:
        assert start is None
        c = line.index('S')
        start = (r, c)

    grid.append([c for c in line])

# Determine connected pipes
connected = []
r, c = start
if r != 0 and grid[r - 1][c] in "|7F":
    connected.append((r - 1, c))
if r != len(grid) and grid[r + 1][c] in "|JL":
    connected.append((r + 1, c))
if c != 0 and grid[r][c - 1] in "-LF":
    connected.append((r, c - 1))
if c != len(grid[0]) - 1 and grid[r][c + 1] in "-J7":
    connected.append((r, c + 1))

# Start towards one of the two connected pipes and travel until reaching the start again
path = [start, connected[0]]
while path[-1] != start:
    r, c = path[-1]
    match grid[r][c]:
        case '|':
            to_check = [(r - 1, c), (r + 1, c)]
        case '-':
            to_check = [(r, c - 1), (r, c + 1)]
        case 'L':
            to_check = [(r - 1, c), (r, c + 1)]
        case 'J':
            to_check = [(r - 1, c), (r, c - 1)]
        case '7':
            to_check = [(r, c - 1), (r + 1, c)]
        case 'F':
            to_check = [(r, c + 1), (r + 1, c)]

    # Make sure not to go back
    if to_check[0] != path[-2]:
        path.append(to_check[0])
    else:
        path.append(to_check[1])

# Part 1: furthest distance from start
dist = (len(path) - 1) // 2
print(f"Furthest distance: {dist}")

# Remove all random bits of pipe that are not part of the path
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if (r, c) in path:
            grid[r][c] = '+'
        else:
            grid[r][c] = '.'

# Scale up the grid by 2x so that flood fill can go between the pipes
grid2 = []
for line in grid:
    line2 = list(itertools.repeat('.', 2 * len(line)))
    grid2.append(line2)
    grid2.append(line2.copy())

# Scale up and interpolate the path
path2 = []
for i in range(len(path) - 1):
    r1, c1 = path[i]
    r2, c2 = path[i + 1]
    path2.append((r1, c1))
    if r1 == r2:
        path2.append((r1, (c1 + c2) / 2))
    elif c1 == c2:
        path2.append(((r1 + r2) / 2, c1))
    else:
        raise RuntimeError

# Copy the scaled-up path onto the scaled-up grid
for r, c in path2:
    r, c = int(2 * r), int(2 * c)
    grid2[r][c] = '+'

# Prepare flood fill: start from every empty tile on the edges
max_r = len(grid2) - 1
max_c = len(grid2[0]) - 1
to_visit = []
for r in range(max_r + 1):
    if grid2[r][0] == '.':
        to_visit.append((r, 0))
for c in range(max_c + 1):
    if grid2[0][c] == '.':
        to_visit.append((0, c))

# Flood fill
while to_visit:
    r, c = to_visit.pop(0)
    if grid2[r][c] == '.':
        grid2[r][c] = 'x'

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r_next, c_next = r + dr, c + dc
        if 0 <= r_next <= max_r and 0 <= c_next <= max_c and grid2[r_next][c_next] == '.':
            to_visit.insert(0, (r_next, c_next))

# Count the tiles that are still empty on both the scaled and original maps
empty_count = 0
for r in range(max_r + 1):
    for c in range(max_c + 1):
        if r % 2 == 0 and c % 2 == 0:
            if grid2[r][c] == '.' and grid[r // 2][c // 2] == '.':
                empty_count += 1
                grid[r // 2][c // 2] = 'I'

# Part 2: number of empty tiles enclosed by the loop
print(f"Number of empty tiles: {empty_count}")
