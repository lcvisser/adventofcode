from math import prod
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
grid = []
for row in data.strip().split('\n'):
    grid.append(list(int(x) for x in row))

def compute_basin(r, c, basin):
    # Starting point
    value = grid[r][c]

    # Check for limit of basin
    if value == 9:
        return
    else:
        basin.append((r, c))

    # Travel in all directions
    if r > 0 and grid[r - 1][c] > value:
        compute_basin(r - 1, c, basin)
    if r < len(grid) - 1 and grid[r + 1][c] > value:
        compute_basin(r + 1, c, basin)
    if c > 0 and grid[r][c - 1] > value:
        compute_basin(r, c - 1, basin)
    if c < len(grid[0]) - 1 and grid[r][c + 1] > value:
        compute_basin(r, c + 1, basin)

    return

# Find low points and count risk
risk = 0
basin_sizes = []
for i, row in enumerate(grid):
    for j, value in enumerate(row):
        # Check cells above and below
        if i == 0:
            above_higher = True
            below_higher = grid[i + 1][j] > value
        elif i == len(grid) - 1:
            above_higher = grid[i - 1][j] > value
            below_higher = True
        else:
            above_higher = grid[i - 1][j] > value
            below_higher = grid[i + 1][j] > value

        # Check cells left and right
        if j == 0:
            left_higher = True
            right_higher = grid[i][j + 1] > value
        elif j == len(row) - 1:
            left_higher = grid[i][j - 1] > value
            right_higher = True
        else:
            left_higher = grid[i][j - 1] > value
            right_higher = grid[i][j + 1] > value

        # Check if low point
        if above_higher and below_higher and left_higher and right_higher:
            # Part 1: risk
            risk += 1 + value

            # Part 2: basin size:
            basin = [(i, j)]
            compute_basin(i, j, basin)
            size = len(set(basin))
            basin_sizes.append(size)

# Part 1: total risk
print(f"Total risk: {risk}")

# Part 2: product of sizes of three largest basins
print("Product of basin sizes: {}". format(prod(sorted(basin_sizes)[-3:])))
