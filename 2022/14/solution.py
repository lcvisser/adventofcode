import sys
import copy

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Sand producer location
producer_coord = (500, 0)
max_x, max_y = producer_coord
min_x = producer_coord[0]

# Parse data for rock segments
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

# Grid markers
producer = '+'
air = '.'
rock = '#'
sand = 'o'

# Prepare the grid (sand will flow diagonally, so make it wide enough for that)
grid = [[air] * (max_x + max_y) for _ in range(max_y + 1)]
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

# Show initial grid
px, py = producer_coord
grid[py][px] = producer

# Propagate sand
def drop_sand(_grid, _max_y):
    sand_count = 0
    dropped_into_void = False
    stuck_at_start = False
    while not dropped_into_void and not stuck_at_start:
        sandx, sandy = producer_coord
        while sandy < _max_y:
            if _grid[sandy + 1][sandx] == air:
                # Go straight down
                sandy += 1
            elif _grid[sandy + 1][sandx - 1 ] == air:
                # Go down and to left
                sandx -= 1
                sandy += 1
            elif _grid[sandy + 1][sandx + 1 ] == air:
                # Go down and to the right
                sandx += 1
                sandy += 1
            else:
                # Stop
                _grid[sandy][sandx] = sand

                if (sandx, sandy) == producer_coord:
                    stuck_at_start = True

                break
        else:
            dropped_into_void = True

        sand_count += 1

    return sand_count

# Grid copies
grid1 = copy.deepcopy(grid)
grid2 = copy.deepcopy(grid)

# Last sand unit counted fell down, so n - 1 are at rest
number_of_resting_units1 = drop_sand(grid1, max_y) - 1

# Part 1: number of sand units resting
print(f"Number of sand that came to rest: {number_of_resting_units1}")

# Add floor
grid2.append([air] * len(grid[0]))
grid2.append([rock] * len(grid[0]))

# Now all units should be counted
number_of_resting_units2 = drop_sand(grid2, max_y + 2)

# Part 2: number of sand units resting on the floor
print(f"Number of sand that came to rest on the floor: {number_of_resting_units2}")
