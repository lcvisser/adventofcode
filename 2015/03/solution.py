with open("2015/03/input.txt") as f:
    instructions = f.read()

# Horizontal, vertical
moves = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, 1),
    "v": (0, -1)
}

current_position = (0, 0)
visited = { current_position }
for d in instructions:
    x, y = current_position
    dx, dy = moves[d]
    new_position = x + dx, y + dy
    visited.add(new_position)
    current_position = new_position

# Part 1
print(f"Number of houses visited: {len(visited)}")
