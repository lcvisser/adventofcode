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
    if any(grid[fold_coord]):
        raise ValueError(f"nonempty fold line at {fold_coord}")

    max_y = len(grid) - 1
    num_lines_to_fold = max_y - fold_coord
    for y in reversed(range(num_lines_to_fold)):
        # Determine target opposite the fold
        from_y = fold_coord + 1 + y
        to_y = fold_coord - 1 - y

        # Add the row onto its target row
        row_to_fold = grid.pop(from_y)
        for x, value in enumerate(row_to_fold):
            grid[to_y][x] += value

    # Pop the fold line
    grid.pop(fold_coord)
    return grid

# Helper function to process a single fold instruction
def fold(grid, dim, fold_coord):
    if dim == 'y':
        # Fold along y-axis
        new_grid = fold_along_y(grid, fold_coord)
    elif dim == 'x':
        # Transpose the grid and then fold along y-axis
        transposed_grid = [list(c) for c in zip(*grid)]
        transposed_folded_grid = fold_along_y(transposed_grid, fold_coord)

        # Transpose back
        new_grid = [list(c) for c in zip(*transposed_folded_grid)]

    return new_grid

# Part 1: count visible dots after 1 folding instruction
grid1 = fold(copy.deepcopy(grid), *fold_instructions[0])
dot_count = 0
for row in grid1:
    for x in row:
        if x > 0:
            dot_count += 1

print(f"Number of dots after one fold: {dot_count}")

# Part 2: complete folding and decode
def print_grid(grid):
    for i, row in enumerate(grid):
        print(''.join(' ' if x == 0 else '#' for x in row))
    print()

grid2 = copy.deepcopy(grid)
for dim, fold_coord in fold_instructions:
    grid2 = fold(grid2, dim, fold_coord)

print("Sheet after complete folding:")
print_grid(grid2)
