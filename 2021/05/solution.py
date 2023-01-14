import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
line_coords = []
max_x = 0
max_y = 0
for line in data.split('\n'):
    if not line.strip():
        continue

    p0, p1 = line.split("->")
    x0, y0 = [int(n) for n in p0.split(',')]
    x1, y1 = [int(n) for n in p1.split(',')]
    line_coords.append([(x0, y0), (x1, y1)])

    if x0 > max_x:
        max_x = x0
    if x1 > max_x:
        max_x = x1

    if y0 > max_y:
        max_y = y0
    if y1 > max_y:
        max_y = y1

# Create grid
grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]
for (x0, y0), (x1, y1) in line_coords:
    if x0 == x1:
        # Vertical line
        if y0 > y1:
            y0, y1 = y1, y0

        for y in range(y0, y1 + 1):
            grid[y][x0] += 1
    elif y0 == y1:
        # Horizontal line
        if x0 > x1:
            x0, x1 = x1, x0

        for x in range(x0, x1 + 1):
            grid[y0][x] += 1

# Count dangerous points
danger_count = 0
for row in grid:
    for n in row:
        if n >= 2:
            danger_count += 1

# Part 1: number of points with two or more lines crossing through it
print(f"Answer part 1: {danger_count}")

# Create grid
grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]
for (x0, y0), (x1, y1) in line_coords:
    if x0 == x1:
        # Vertical line
        if y0 > y1:
            y0, y1 = y1, y0

        for y in range(y0, y1 + 1):
            grid[y][x0] += 1
    elif y0 == y1:
        # Horizontal line
        if x0 > x1:
            x0, x1 = x1, x0

        for x in range(x0, x1 + 1):
            grid[y0][x] += 1
    elif abs(x1 - x0) == abs(y1 - y0):
        # Diagonal line
        if x0 > x1 and y0 > y1:
            # NW direction; reverse both coordinates
            xy = zip(range(x1, x0 + 1), range(y1, y0 + 1))
        elif x0 > x1 and y0 <= y1:
            # SW direction; reverse x-coordinates, but re-reverse them to match with correct y-coordinate
            xy = zip(reversed(range(x1, x0 + 1)), range(y0, y1 + 1))
        elif x0 <= x1 and y0 > y1:
            # NE direction; reverse y-coordinates, but re-reverse them to match with correct x-coordinate
            xy = zip(range(x0, x1 + 1), reversed(range(y1, y0 + 1)))
        else:
            # SE direction; use coordinates as given
            xy = zip(range(x0, x1 + 1), range(y0, y1 + 1))

        for x, y in xy:
            grid[y][x] += 1

# Count dangerous points
danger_count = 0
for row in grid:
    for n in row:
        if n >= 2:
            danger_count += 1

# Part 2: number of points with two or more lines crossing through it including diagonal lines
print(f"Answer part 2: {danger_count}")
