import math

# Read data
input_file = "2024/16/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
grid = []
start = None
end = None

for r, row in enumerate(data.strip().split('\n')):
    grid_row = []
    for c, ch in enumerate(row):
        s = math.inf

        if ch == 'S':
            start = (r, c)
        elif ch == 'E':
            end = (r, c)
        elif ch == '.':
            pass

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


def neighbors_of(p, d):
    x, y = p
    neighbors = {}
    for new_d, (dx, dy) in DIRECTIONS.items():
        new_x = x + dx
        new_y = y + dy
        if is_reachable(x, y, d, new_x, new_y) and grid[new_x][new_y] != '#':
            # Either go forward or turn, but not both
            if new_d == d:
                neighbors[d] = (new_x, new_y)
            else:
                neighbors[new_d] = (x, y)

    return neighbors


# Breadth-first path search
start_direction = '>'  # start facing east
start_state = (start, '>', 0, [start])  # position, direction, score, path
to_visit = [start_state]
visited = dict()
visited[(start, start_direction)] = 0  # score
lowest_score = math.inf
all_paths = dict()
while to_visit:
    current, direction, score, path = to_visit.pop(0)

    if current == end:
        # Paths are only tracked as tiles, so only update the all_paths dict if the score is lower
        if score <= lowest_score:
            all_paths[tuple(path.copy())] = score
            lowest_score = score

    neighbors = neighbors_of(current, direction)
    for new_direction, new_pos in neighbors.items():
        # Either move forward or turn, but not both
        if new_direction == direction:
            new_score = score + 1
            new_path = path.copy() + [new_pos]
        else:
            new_score = score + 1000
            new_path = path.copy()

        new_state = (new_pos, new_direction, new_score, new_path)

        # Visit new tiles or revisit tiles if the score is lower
        if (new_pos, new_direction) not in visited.keys() or visited[(new_pos, new_direction)] >= new_score:
            visited[(new_pos, new_direction)] = new_score
            to_visit.append(new_state)

# Part 1: lowest score path
print(f"Lowest score: {lowest_score}")

# Count unique tiles
tiles = set()
for path, score in all_paths.items():
    if score == lowest_score:
        for tile in path:
            tiles.add(tile)

# Part 2: number of uniquely visited tiles
print(f"Number of tiles: {len(tiles)}")
