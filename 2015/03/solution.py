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

santa_position = (0, 0)
robot_position = (0, 0)
visited = { santa_position, robot_position}
santa_to_move = True
for d in instructions:
    dx, dy = moves[d]
    if santa_to_move:
        x, y = santa_position
        new_position = x + dx, y + dy
        visited.add(new_position)
        santa_position = new_position
    else:
        x, y = robot_position
        new_position = x + dx, y + dy
        visited.add(new_position)
        robot_position = new_position

    santa_to_move = not santa_to_move

# Part 2
print(f"Number of houses with at least one visit: {len(visited)}")
