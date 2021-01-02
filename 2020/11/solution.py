from copy import deepcopy
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

layout = []
for row in data.split('\n'):
    if len(row) > 0:
        layout.append(list(row))
layout2 = deepcopy(layout)

def num_occupied_adjacent(_layout, _i, _j):
    n = 0
    for s in (-1, 0, 1):
        for t in (-1, 0, 1):
            if s == 0 and t == 0:
                pass
            else:
                x = _i + s
                y = _j + t
                if x < 0 or y < 0:
                    pass
                elif x >= len(_layout) or y >= len(_layout[0]):
                    pass
                else:
                    if _layout[x][y] == '#':
                        n += 1

    return n

def update_layout(_layout):
    new_layout = deepcopy(_layout)
    new_occupied = 0
    for i, row in enumerate(_layout):
        for j, seat in enumerate(row):
            if seat in ('L', '#'):
                n_occ = num_occupied_adjacent(_layout, i, j)

            if seat == '.':
                new_layout[i][j] = '.'
            elif seat == 'L':
                if n_occ == 0:
                    new_layout[i][j] = '#'
                else:
                    new_layout[i][j] = 'L'
            elif seat == '#':
                if n_occ >= 4:
                    new_layout[i][j] = 'L'
                else:
                    new_layout[i][j] = '#'

            if new_layout[i][j] == '#':
                new_occupied += 1

    return new_layout, new_occupied

# Part 1: determine number of occupied seats when nothing changes anymore
while True:
    new_layout, n = update_layout(layout)
    if new_layout == layout:
        break
    else:
        layout = new_layout

print(f"Number of occupied seats: {n}")

# Part 2: determine number of occupied seats with new rules
def num_occupied_in_view(_layout, _i, _j):
    n = 0
    for s in (-1, 0, 1):
        for t in (-1, 0, 1):
            if s == 0 and t == 0:
                pass
            else:
                u = 0
                while True:
                    u += 1
                    x = _i + s * u
                    y = _j + t * u
                    if x < 0 or y < 0:
                        break
                    elif x >= len(_layout) or y >= len(_layout[0]):
                        break
                    else:
                        if _layout[x][y] == '#':
                            n += 1
                            break
                        elif _layout[x][y] == 'L':
                            break

    return n

def update_layout2(_layout):
    new_layout = deepcopy(_layout)
    new_occupied = 0
    for i, row in enumerate(_layout):
        for j, seat in enumerate(row):
            if seat in ('L', '#'):
                n_occ = num_occupied_in_view(_layout, i, j)

            if seat == '.':
                new_layout[i][j] = '.'
            elif seat == 'L':
                if n_occ == 0:
                    new_layout[i][j] = '#'
                else:
                    new_layout[i][j] = 'L'
            elif seat == '#':
                if n_occ >= 5:
                    new_layout[i][j] = 'L'
                else:
                    new_layout[i][j] = '#'

            if new_layout[i][j] == '#':
                new_occupied += 1

    return new_layout, new_occupied

while True:
    new_layout2, n = update_layout2(layout2)
    if new_layout2 == layout2:
        break
    else:
        layout2 = new_layout2

print(f"Number of occupied seats: {n}")
