# Read data
input_file = "2024/06/input.txt"
with open(input_file) as f:
    data = f.read()


# Row and column increments for each direction
DIRECTIONS = {
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1),
}


def new_state(x, y, d, obstacles):
    dx, dy = DIRECTIONS[d]
    if (x + dx, y + dy) in obstacles:
        idx = list(DIRECTIONS.keys()).index(d)
        idx = (idx + 1) % 4
        d = list(DIRECTIONS.keys())[idx]
    else:
        x, y = x + dx, y + dy

    return x, y, d


# Parse grid
start = None
obstacles = []
width = 0
height = 0
for r, line in enumerate(data.strip().split('\n')):
    height = r
    for c, char in enumerate(line):
        width = c
        if char == '^':
            start = (r,c)
        elif char == '#':
            obstacles.append((r, c))


# Keep track of unique visited positiions
visited = set()
visited.add(start)

# Go
state = (*start, "up")
while True:
    state = new_state(*state, obstacles)
    x, y, _ = state
    if x < 0 or x > width or y < 0 or y > height:
        break
    else:
        visited.add((x, y))

# Part 1: number of positions visited
print(f"Number of positions visited: {len(visited)}")


# Helper function to check if there is a loop
def has_loop(obstacle_x, obstacle_y, start_x, start_y):
    looped = False

    state = (start_x, start_y, "up")
    path = [state]
    while True:
        state = new_state(*state, obstacles + [(obstacle_x, obstacle_y)])

        x, y, _ = state
        if x < 0 or x > width or y < 0 or y > height:
            break
        elif state in path:
            looped = True
            break
        else:
            path.append(state)

    return looped


# Find loops
loop_count = 0
for i, (r, c) in enumerate(visited):
    if (r, c) != start:
        if has_loop(r, c, *start):
            loop_count += 1

# Part 2: Number of positions that result in a loop
print(f"Number of positions that result in a loop: {loop_count}")
