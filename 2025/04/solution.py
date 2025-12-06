with open("2025/04/input.txt") as f:
    data = f.read()

grid = []
for row in data.strip().split("\n"):
    grid.append([c for c in row])

def at(r, c):
    if r < 0 or r >= len(grid):
        return "."
    elif c < 0 or c >= len(grid[0]):
        return "."
    else:
        return grid[r][c]

# Part 1
accessible_rolls = 0
for r, _ in enumerate(grid):
    for c, _ in enumerate(row):
        neighbors = []
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            neighbors.append(at(r + dr, c + dc))

        if at(r, c) == "@" and neighbors.count("@") < 4:
            accessible_rolls += 1

print(f"Number of accessible rolls: {accessible_rolls}")
