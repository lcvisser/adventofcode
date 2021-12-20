import copy
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
dots = []
dots_complete = False
fold_instructions = []
for line in data.strip().split('\n'):
    if line.strip() == '':
        dots_complete = True
        continue

    if not dots_complete:
        x, y = [int(x) for x in line.split(',')]
        dots.append((x, y))
    else:
        instruction, v = line.split('=')
        dim = instruction[-1]
        fold_instructions.append((dim, int(v)))

# Create dots grid
x_coords, y_coords = zip(*dots)
max_x, max_y = max(x_coords), max(y_coords)
grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]
for x, y in dots:
    grid[y][x] = 1

# Helper function to fold along y-axis
def fold_along_y(grid, fold_coord):
    max_y = len(grid)
    for y in reversed(range(fold_coord + 1, max_y)):
        target_y = max_y - y - 1
        row_to_fold = grid.pop(y)
        for x, value in enumerate(row_to_fold):
            grid[target_y][x] += value

    grid.pop(fold_coord)
    return grid

# Helper function to process a single fold instruction
def fold(grid, dim, fold_coord):
    if dim == 'x':
        # Transpose the grid and then fold along y-axis
        transposed_grid = [list(c) for c in zip(*grid)]
        transposed_folded_grid = fold_along_y(transposed_grid, fold_coord)
        grid = [list(c) for c in zip(*transposed_folded_grid)]
    elif dim == 'y':
        # Fold along y-axis
        grid = fold_along_y(grid, fold_coord)

    return grid

# Part 1: count visible dots after 1 folding instruction
grid1 = fold(copy.deepcopy(grid), *fold_instructions[0])
dot_count = 0
for row in grid1:
    for x in row:
        if x > 0:
            dot_count += 1

print(f"Number of dots after one fold: {dot_count}")
