import itertools
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
image = []
for line in data.strip().split('\n'):
    image.append([c for c in line])

# Find empty rows
n_rows = len(image)
empty_rows = []
for r in range(n_rows):
    if all(x == '.' for x in image[r]):
        empty_rows.append(r)

# Find empty columns
n_cols = len(image[0])
empty_cols = []
for c in range(n_cols):
    if all(image[r][c] == '.' for r in range(n_rows)):
        empty_cols.append(c)

# Expand image
image_expanded = []
for r, row in enumerate(image):
    image_expanded.append([])
    for c, ch in enumerate(row):
        image_expanded[-1].append(ch)
        if c in empty_cols:
            image_expanded[-1].append('.')

    if r in empty_rows:
        image_expanded.append(['.' for _ in range(n_cols + len(empty_cols))])

# Locate galaxies
galaxies = dict()
gid = 1
for r, row in enumerate(image_expanded):
    for c, ch in enumerate(row):
        if ch == '#':
            galaxies[gid] = (r, c)
            gid += 1

# Compute distances
dists = []
for a, b in itertools.combinations(galaxies.keys(), 2):
    d = abs(galaxies[a][0] - galaxies[b][0]) + abs(galaxies[a][1] - galaxies[b][1])
    dists.append(d)

# Part 1: sum of distances
print(f"Sum of distances: {sum(dists)}")
