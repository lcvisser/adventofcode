import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

data3 = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

producer_coord = (500, 0)
max_x, max_y = producer_coord
min_x = producer_coord[0]

rock_segments = []
for line in data.strip().split('\n'):
    prev = None
    for coord in line.split(" -> "):
        sx, sy = coord.split(',')
        x = int(sx)
        y = int(sy)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        if prev is None:
            prev = (x, y)
        else:
            curr = (x, y)
            segment = [prev, curr]
            rock_segments.append(segment)
            prev = curr

producer = '+'
air = '.'
rock = '#'
sand = 'o'

def print_grid(_grid):
    for i, line in enumerate(_grid):
        print(f"{i:4d} " + ''.join(line[min_x-1:]) + air)

    print(f"{len(grid):4d} " + air * (max_x - min_x + 3))
    print()

grid = [[air] * (max_x + 1) for _ in range(max_y + 1)]
for segment in rock_segments:
    ss, se = segment
    if ss[1] == se[1]:
        # horizontal segment
        if ss[0] <= se[0]:
            for i in range(ss[0], se[0] + 1):
                grid[ss[1]][i] = rock
        else:
            for i in range(se[0], ss[0] + 1):
                grid[ss[1]][i] = rock

    elif ss[0] == se[0]:
        # vertical segment
        if ss[1] <= se[1]:
            for i in range(ss[1], se[1] + 1):
                grid[i][ss[0]] = rock
        else:
            for i in range(se[1], ss[1] + 1):
                grid[i][ss[0]] = rock


px, py = producer_coord
grid[py][px] = producer

# print("Initial grid")
# print_grid(grid)
sand_count = 0
dropped_into_void = False
while not dropped_into_void:
    sandx, sandy = producer_coord
    while sandy < max_y:
        if grid[sandy + 1][sandx] == air:
            # go straight down
            sandy += 1
        elif grid[sandy + 1][sandx - 1 ] == air:
            # down left
            sandx -= 1
            sandy += 1
        elif grid[sandy + 1][sandx + 1 ] == air:
            # down right
            sandx += 1
            sandy += 1
        else:
            # stop
            grid[sandy][sandx] = sand
            break
    else:
        dropped_into_void = True

    sand_count += 1
    # print(f"After sand {sand_count}")
    # print_grid(grid)

# Last sand unit counted fell down, so n - 1 are at rest
number_of_resting_units = sand_count - 1

# Part 1: number of sand units resting
print(f"Number of sand that came to rest: {sand_count - 1}")
