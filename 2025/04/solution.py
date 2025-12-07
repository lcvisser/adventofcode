with open("2025/04/input.txt") as f:
    data = f.read()


the_grid = []
for row in data.strip().split("\n"):
    the_grid.append([c for c in row])


def at(grid, r, c):
    if r < 0 or r >= len(grid):
        return "."
    elif c < 0 or c >= len(grid[0]):
        return "."
    else:
        return grid[r][c]


def get_accessible_rolls(grid):
    accessible_rolls = []
    for r, _ in enumerate(the_grid):
        for c, _ in enumerate(row):
            neighbors = []
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                neighbors.append(at(the_grid, r + dr, c + dc))

            if at(the_grid, r, c) == "@" and neighbors.count("@") < 4:
                accessible_rolls.append((r, c))

    return accessible_rolls


def num_accessible_rolls(grid):
    return len(get_accessible_rolls(grid))


# Part 1
print(f"Number of accessible rolls: {num_accessible_rolls(the_grid)}")


# Part 2
def remove_rolls(grid, rolls):
    for r, c in rolls:
        grid[r][c] = "."

    return grid


def num_removable_rolls(grid):
    removed_rolls = 0
    while rolls := get_accessible_rolls(grid):
        removed_rolls += len(rolls)
        grid = remove_rolls(grid, rolls)

    return removed_rolls

print(f"Number of rolls removed: {num_removable_rolls(the_grid)}")
