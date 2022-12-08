import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

grid = [[int(x) for x in line] for line in lines]
grid_dim = (len(grid), len(grid[0]))

# Part 1: count number of visible trees
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

# Part 2: highest scenic score
from itertools import takewhile
def count_visible(idx, lst):
    this_tree_height = lst[idx]
    num_visible_before = 0
    for t in reversed(range(0, idx)):
        num_visible_before += 1
        if lst[t] >= this_tree_height:
            break

    num_visible_after = 0
    for t in range(idx + 1, len(lst)):
        num_visible_after += 1
        if lst[t] >= this_tree_height:
            break

    return num_visible_before, num_visible_after

max_scenic_score = 0
for row in range(1, grid_dim[0] - 1):
    for col in range(1, grid_dim[1] - 1):
        this_row = grid[row]
        this_column = [grid[r][col] for r in range(grid_dim[0])]
        this_tree_height = grid[row][col]
        visible_left, visible_right = count_visible(col, this_row)
        visible_top, visible_bottom = count_visible(row, this_column)
        scenic_score = visible_left * visible_right * visible_top * visible_bottom
        max_scenic_score = max(max_scenic_score, scenic_score)

print(f"Maximum scenic score: {max_scenic_score}")
