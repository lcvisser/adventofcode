# Read data
input_file = "2024/12/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse grid
grid = []
height = 0
width = 0
for r, row in enumerate(data.strip().split('\n')):
    height = r

    grid_row = []
    for c, ch in enumerate(row):
        width = c
        grid_row.append(ch)

    grid.append(grid_row)


# Helper functions for grid
def get_crop_at(x, y):
    if 0 <= x <= height and 0 <= y <= width:
        return grid[x][y]
    else:
        return None


def neighbours_of(x, y, crop):
    same_crop = []
    adjacent = []
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        d = (x + dx, y + dy)
        c = get_crop_at(*d)
        if c == crop:
            same_crop.append(d)
        elif c is not None:
            adjacent.append(d)

    return same_crop, adjacent


# Helper functions to fill an area
FILL = '.'

def fill(x, y):
    grid[x][y] = FILL


def fill_area_at(sx, sy):
    crop = get_crop_at(sx, sy)

    area = 0
    perimeter = 0
    to_visit = [(sx, sy)]
    visited = set()
    adjacent = set()
    while to_visit:
        current = to_visit.pop(0)
        if current not in visited:
            visited.add(current)

            neighbours, adjacent_crops = neighbours_of(*current, crop)
            area += 1
            perimeter += (4 - len(neighbours))

            for n in neighbours:
                to_visit.append(n)
            for a in adjacent_crops:
                adjacent.add(a)

    for v in visited:
        fill(*v)

    return area, perimeter, adjacent


# Compute areas an perimeters to determine price
starting_points = [(0, 0)]
price = 0
while starting_points:
    # Next area (may be filled in the mean time though)
    start = starting_points.pop(0)
    if get_crop_at(*start) == FILL:
        continue

    # Compute area and perimeter for pricing, save adjacent crop plots
    area, perimeter, adjacent = fill_area_at(*start)
    price += area * perimeter

    # Add adjacent crop plots for future processing
    for a in filter(lambda x: get_crop_at(*x) != FILL, adjacent):
        starting_points.append(a)

# Part 1: price of fencing
print(f"Price of fencing: {price}")
