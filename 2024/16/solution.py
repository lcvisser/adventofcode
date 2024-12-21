import math

# Read data
input_file = "2024/16/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
grid = []
start = None
end = None

scores = {}
facing = {}
prev = {}
to_visit = []

for r, row in enumerate(data.strip().split('\n')):
    grid_row = []
    for c, ch in enumerate(row):
        s = math.inf
        d = '?'

        if ch == 'S':
            start = (r, c)
            s = 0
            d = '>'  # start facing East
        elif ch == 'E':
            end = (r, c)
        elif ch == '.':
            pass

        if ch != '#':
            prev[(r, c)] = (-1, -1)  # invalid
            scores[(r, c)] = s
            facing[(r, c)] = d
            to_visit.append((r, c))

        grid_row.append(ch)

    grid.append(grid_row)


DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def is_reachable(x, y, d, new_x, new_y):
    dx = new_x - x
    dy = new_y - y
    all_directions = list(DIRECTIONS.keys())
    idx = all_directions.index(d)
    d_left = all_directions[(idx - 1) % 4]
    d_right = all_directions[(idx + 1) % 4]
    return (dx, dy) in (DIRECTIONS[d_left], DIRECTIONS[d], DIRECTIONS[d_right])


def neighbors_of(p):
    x, y = p
    neighbors = {}
    for d, (dx, dy) in DIRECTIONS.items():
        new_x = x + dx
        new_y = y + dy
        if is_reachable(x, y, d, new_x, new_y) and grid[new_x][new_y] != '#':
            neighbors[d] = (new_x, new_y)

    return neighbors


# Dijkstra's algorithm to find the lowest scoring path
to_visit.sort(key=lambda p: scores[p])
while to_visit:
    to_visit.sort(key=lambda p: scores[p])

    current = to_visit.pop(0)
    d = facing[current]
    score = scores[current]

    if current == end:
        break

    for side, loc in neighbors_of(current).items():
        new_score = score + 1
        if side != d:
            new_score += 1000

        if new_score < scores[loc]:
            scores[loc] = new_score
            facing[loc] = side
            prev[loc] = current

# Part 1: lowest score path
print(f"Lowest score: {scores[end]}")
