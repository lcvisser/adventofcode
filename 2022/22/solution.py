import sys
import copy

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

data = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

# Parse data
board, instructions = data.split("\n\n")

# Create the board grid
start = None
grid = []
maxlen = 0
for row in board.split('\n'):
    if row.strip() == "":
        continue
    if start is None:
        startcol = row.index('.')
    start = (0, startcol)
    grid.append(row)
    maxlen = max(maxlen, len(row))

# Pad the grid to make edge calculations easier
for i, row in enumerate(grid):
    grid[i] += ' ' * (maxlen - len(row))

# Parse the commands
distance = 0
commands0 = []
for c in instructions:
    if c.isdigit():
        distance = 10 * distance + int(c)
    elif c in ('R', 'L'):
        commands0.append(("move", distance))
        distance = 0
        commands0.append(("rotate", c))
    else:
        # End of command sequence
        if distance != 0:
            commands0.append(("move", distance))

# Orientations
orientations = ">v<^"


CUBE_DIM = 4

import typing

class Face(typing.NamedTuple):
    id: int
    loc: typing.Tuple[int, int]
    connects: typing.Dict[str, typing.Tuple[int, str]]

"""
  1
234
  56
"""
face1 = Face(id=1, loc=(0, 2), connects={"right": (6, "right"), "bottom": (4, "top"), "left": (3, "top"), "top": (2, "top")})
face2 = Face(id=2, loc=(1, 0), connects={"right": (3, "left"), "bottom": (5, "bottom"), "left": (6, "bottom"), "top": (1, "top")})
face3 = Face(id=3, loc=(1, 1), connects={"right": (4, "left"), "bottom": (5, "left"), "left": (2, "right"), "top": (1, "left")})
face4 = Face(id=4, loc=(1, 2), connects={"right": (6, "top"), "bottom": (5, "top"), "left": (3, "right"), "top": (1, "bottom")})
face5 = Face(id=5, loc=(2, 2), connects={"right": (6, "left"), "bottom": (2, "bottom"), "left": (3, "bottom"), "top": (4, "bottom")})
face6 = Face(id=6, loc=(2, 3), connects={"right": (1, "right"), "bottom": (2, "left"), "left": (5, "right"), "top": (4, "right")})
faces = {1: face1, 2: face2, 3: face3, 4: face4, 5: face5, 6: face6}

for src_face_id, face1 in faces.items():
    for edge1, (dest_face_id, edge2) in face1.connects.items():
        assert src_face_id == face1.id
        assert faces[dest_face_id].connects[edge2] == (src_face_id, edge1)


def face_id(r, c):
    face_row = r // CUBE_DIM
    face_col = c // CUBE_DIM
    for fid, f in faces.items():
        if (face_row, face_col) == f.loc:
            return fid

    raise ValueError(r, c)


def to_local_coord(r, c):
    fr = r % CUBE_DIM
    fc = c % CUBE_DIM
    fid = face_id(r, c)
    return fr, fc, fid


def to_global_coord(fr, fc, fid):
    r, c = [x * CUBE_DIM + y for x, y in zip(faces[fid].loc, (fr, fc))]
    return r, c


def edge_name(r, c, d):
    on_right_edge = c == CUBE_DIM - 1
    on_left_edge = c == 0
    on_top_edge = r == 0
    on_bottom_edge = r == CUBE_DIM - 1
    if on_right_edge and d == orientations.index('>'):
        return "right"
    elif on_bottom_edge and d == orientations.index('v'):
        return "bottom"
    elif on_left_edge and d == orientations.index('<'):
        return "left"
    elif on_top_edge and d == orientations.index('^'):
        return "top"
    else:
        return None


def mirror(x):
    return CUBE_DIM - 1 - x

def try_move(r, c, d):
    if d == orientations.index('>'):
        target = r, c + 1, d
    elif d == orientations.index('<'):
        target = r, c - 1, d
    elif d == orientations.index('v'):
        target = r + 1, c, d
    elif d == orientations.index('^'):
        target = r - 1, c, d
    else:
        raise ValueError(d)

    print(target)
    if grid[target[0]][target[1]] == '#':
        return r, c, d
    else:
        return target

def move(r, c, d):
    cr, cc, curr_face = to_local_coord(r, c)
    curr_edge = edge_name(cr, cc, d)

    if curr_edge is None:
        return try_move(r, c, d)

    target_face, target_edge = faces[curr_face].connects[curr_edge]
    print(f"Going from {curr_edge} edge on face {curr_face} to {target_edge} edge on face {target_face}")
    match target_edge:
        case "right":
            target_dir = orientations.index('<')
            cc_new = CUBE_DIM - 1
            match curr_edge:
                case "right": cr_new = mirror(cr)
                case "bottom": cr_new = cc
                case "left": cr_new = cr
                case "top": cr_new = mirror(cc)
        case "bottom":
            target_dir = orientations.index('^')
            cr_new = CUBE_DIM - 1
            match curr_edge:
                case "right": cc_new = cr
                case "bottom": cc_new = mirror(cc)
                case "left": cc_new = mirror(cr)
                case "top": cc_new = cc
        case "left":
            target_dir = orientations.index('>')
            cc_new = 0
            match curr_edge:
                case "right": cr_new = cr
                case "bottom": cr_new = mirror(cc)
                case "left": cr_new = mirror(cr)
                case "top": cr_new = cc
        case "top":
            target_dir = orientations.index('v')
            cr_new = 0
            match curr_edge:
                case "right": cc_new = mirror(cr)
                case "bottom": cc_new = cc
                case "left": cc_new = cr
                case "top": cc_new = mirror(cc)

    target_row, target_col = to_global_coord(cr_new, cc_new, target_face)
    print(target_row, target_col, target_dir)
    if grid[target_row][target_col] == '#':
        return r, c, d
    else:
        return target_row, target_col, target_dir



# Part 1: find the password by moving on the map
commands1 = copy.deepcopy(commands0)
facing = orientations.index('>')
row, col = start
while commands1:
    cmd, arg = commands1.pop(0)
    if cmd == "move":
        match facing:
            case 0:  # right
                for _ in range(arg):
                    if col + 1 == len(grid[row]) or grid[row][col + 1] == ' ':
                        # Edge on the right
                        other_edge_first_space = grid[row].find('.')
                        other_edge_first_wall = grid[row].find('#')
                        if other_edge_first_space < other_edge_first_wall:
                            col = other_edge_first_space
                        else:
                            # Wall on the other side, stuck
                            break
                    elif grid[row][col + 1] == '#':
                        # Stuck against wall
                        break
                    else:
                        col = col + 1
            case 2:  # left
                for _ in range(arg):
                    if col - 1 == -1 or grid[row][col - 1] == ' ':
                        # Edge on the left
                        other_edge_first_space = grid[row].rfind('.')
                        other_edge_first_wall = grid[row].rfind('#')
                        if other_edge_first_space > other_edge_first_wall:
                            col = other_edge_first_space
                        else:
                            # Wall on the other side, stuck
                            break
                    elif grid[row][col - 1] == '#':
                        # Stuck against wall
                        break
                    else:
                        col = col - 1
            case 1:  # down
                for _ in range(arg):
                    if row + 1 == len(grid) or (row + 1 < len(grid) and grid[row + 1][col] == ' '):
                        # Edge on the bottom, find where the top of the urrent section is
                        j = row
                        while grid[j][col] in ".#":
                            j -= 1
                            if j == -1:
                                break

                        if grid[j + 1][col] == '.':
                            row = j + 1
                        else:
                            # Stuck against wall
                            break
                    elif grid[row + 1][col] == '#':
                        # Stuck against wall
                        break
                    else:
                        row = row + 1
            case 3:  # up
                for _ in range(arg):
                    if row - 1 == -1 or (row - 1 >= 0 and grid[row - 1][col] == ' '):
                        # Edge on the top, find where the bottom of the current section is
                        j = row
                        while grid[j][col] in ".#":
                            j += 1
                            if j == len(grid):
                                break

                        if grid[j - 1][col] == '.':
                            row = j - 1
                        else:
                            # Stuck against wall
                            break
                    elif grid[row - 1][col] == '#':
                        # Stuck against wall
                        break
                    else:
                        row = row - 1

    elif cmd == "rotate":
        if arg == 'R':
            facing = (facing + 1) % len(orientations)
        else:
            facing = (facing - 1) % len(orientations)

    else:
        pass

# Compute password
def compute_password(r, c, d):
    return 1000 * (r + 1) + 4 * (col + 1) + facing

# Part 1: find the password
print(f"Password: {compute_password(row, col, facing)}")

grid_dbg = copy.deepcopy(grid)
commands2 = copy.deepcopy(commands0)
facing = orientations.index('>')
row, col = start
while commands2:
    cmd, arg = commands2.pop(0)

    grid_dbg[row] = [orientations[facing] if i == col else c for i, c in enumerate(grid_dbg[row])]
    for R in grid_dbg:
        print(''.join(R))
    print()

    if cmd == "move":
        for _ in range(arg):
            row, col, facing = move(row, col, facing)

            grid_dbg[row] = [orientations[facing] if i == col else c for i, c in enumerate(grid_dbg[row])]
            for R in grid_dbg:
                print(''.join(R))
            print()

    elif cmd == "rotate":
        if arg == 'R':
            facing = (facing + 1) % len(orientations)
        else:
            facing = (facing - 1) % len(orientations)

    else:
        pass

# Part 2: find the password after moving on a cube
print(f"Password: {compute_password(row, col, facing)}")
