import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

grid = [[int(x) for x in line] for line in lines]

# Part 1: Count number of visible trees
grid_dim = (len(grid), len(grid[0]))
total_visible = 0
for row in range(grid_dim[0]):
    for col in range(grid_dim[1]):
        on_outer_row = row == 0 or row == grid_dim[0] - 1
        on_outer_col = col == 0 or col == grid_dim[1] - 1

        if on_outer_row or on_outer_col:
            total_visible += 1
        else:
            this_row = grid[row]
            this_column = [grid[r][col] for r in range(grid_dim[0])]
            this_tree_height = grid[row][col]
            visible_from_left = all(h < this_tree_height for h in this_row[:col])
            visible_from_right = all(h < this_tree_height for h in this_row[col + 1:])
            visible_from_top = all(h < this_tree_height for h in this_column[:row])
            visible_from_bottom = all(h < this_tree_height for h in this_column[row + 1:])
            if visible_from_left or visible_from_right or visible_from_top or visible_from_bottom:
                total_visible += 1

print(f"Total number of trees visible: {total_visible}")
