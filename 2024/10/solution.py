# Read data
input_file = "2024/10/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse grid
grid = []
trailheads = []
peaks = []
height = 0
width = 0
for r, row in enumerate(data.strip().split('\n')):
    height = r

    grid_row = []
    for c, ch in enumerate(row):
        width = c

        number = int(ch)
        match number:
            case 0:
                trailheads.append((r, c))
            case 9:
                peaks.append((r, c))

        grid_row.append(number)

    grid.append(grid_row)


# Helper functions
def get_number_at(x, y):
    if 0 <= x <= height and 0 <= y <= width:
        return grid[x][y]
    else:
        return None


def get_neighbours_with_value(x, y, v):
    neighbours = []
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        d = (x + dx, y + dy)
        if get_number_at(*d) == v:
            neighbours.append(d)

    return neighbours


def find_number_of_trails(sx, sy):
    # Depth-first search starting from (sx, sy)
    to_visit = [(d, 1) for d in get_neighbours_with_value(sx, sy, 1)]
    peaks = set()  # unique peaks!
    while to_visit:
        current, value = to_visit.pop(0)
        if value == 9:
            peaks.add(current)
        else:
            for next_step in get_neighbours_with_value(*current, value + 1):
                to_visit.insert(0, (next_step, value + 1))

    return len(peaks)


# Compute trailhead scores
trailhead_scores = {}
for t in trailheads:
    number_of_peaks = find_number_of_trails(*t)
    trailhead_scores[t] = number_of_peaks

# Part 1: sum of trailhead scores
print(f"Sum of trailhead scores: {sum(trailhead_scores.values())}")
