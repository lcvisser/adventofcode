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

# Locate galaxies
galaxies = dict()
gid = 1
for r, row in enumerate(image):
    for c, ch in enumerate(row):
        if ch == '#':
            galaxies[gid] = (r, c)
            gid += 1

# Compute distances
def compute_distances(galaxies, expansion_factor):
    dists = []
    for a, b in itertools.combinations(galaxies.keys(), 2):
        xa = min(galaxies[a][0], galaxies[b][0])
        xb = max(galaxies[a][0], galaxies[b][0])
        nx = sum(1 for x in range(xa, xb) if x in empty_rows)
        dx = xb - xa + nx * (expansion_factor - 1)  # do not count the empty rows twice, so -1

        ya = min(galaxies[a][1], galaxies[b][1])
        yb = max(galaxies[a][1], galaxies[b][1])
        ny = sum(1 for y in range(ya, yb) if y in empty_cols)
        dy = yb - ya + ny * (expansion_factor - 1)  # do not count the empty rows twice, so -1

        d = dx + dy
        dists.append(d)

    return dists

# Part 1: sum of distances
dists1 = compute_distances(galaxies, 2)
print(f"Sum of distances (expansion=2): {sum(dists1)}")

# Part 2: sum of distances in expanded universe
dists2 = compute_distances(galaxies, 1000000)
print(f"Sum of distances (expansion=1000000): {sum(dists2)}")
