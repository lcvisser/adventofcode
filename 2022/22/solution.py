import sys
import typing

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

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

# Parse the commands
distance = 0
commands = []
for c in instructions:
    if c.isdigit():
        distance = 10 * distance + int(c)
    elif c in ('R', 'L'):
        commands.append(("move", distance))
        distance = 0
        commands.append(("rotate", c))
    else:
        # End of command sequence, add last number as "move" command
        if distance != 0:
            commands.append(("move", distance))

# Orientations
ORIENTATIONS = ">v<^"


class Square(typing.NamedTuple):
    id: int
    loc: typing.Tuple[int, int]
    connects: typing.Dict[str, typing.Tuple[int, str]]


class MapNavigator:
    def __init__(self, grid, squares, square_dim):
        self.grid = grid
        self.squares = squares
        self.square_dim = square_dim

        # Check if the edge mapping is complete
        for src_square_id, square1 in squares.items():
            for edge1, (dest_square_id, edge2) in square1.connects.items():
                assert src_square_id == square1.id
                assert squares[dest_square_id].connects[edge2] == (src_square_id, edge1)

    def get_square_id(self, r, c):
        """Get the ID of the current square."""
        square_row = r // self.square_dim
        square_col = c // self.square_dim
        for sid, s in self.squares.items():
            if (square_row, square_col) == s.loc:
                return sid

        raise ValueError(r, c)

    def to_local_coord(self, r, c):
        """Convert global coordinates to square-local coordinates."""
        lr = r % self.square_dim
        lc = c % self.square_dim
        sid = self.get_square_id(r, c)
        return lr, lc, sid

    def to_global_coord(self, lr, lc, sid):
        """Convert square-local coordinates to global coordinates."""
        r, c = [x * self.square_dim + y for x, y in zip(self.squares[sid].loc, (lr, lc))]
        return r, c

    def get_edge_name(self, r, c, d):
        """Get the edge name for the current location if on an edge and facing it."""
        on_right_edge = c == self.square_dim - 1
        on_left_edge = c == 0
        on_top_edge = r == 0
        on_bottom_edge = r == self.square_dim - 1

        if on_right_edge and d == ORIENTATIONS.index('>'):
            return "right"
        elif on_bottom_edge and d == ORIENTATIONS.index('v'):
            return "bottom"
        elif on_left_edge and d == ORIENTATIONS.index('<'):
            return "left"
        elif on_top_edge and d == ORIENTATIONS.index('^'):
            return "top"
        else:
            return None

    def mirror_coord(self, x):
        """Mirror a coordinate along the center line of a square"""
        return self.square_dim - 1 - x

    def try_move(self, r, c, d):
        """Try to move one step in the facing direction."""
        # Determine target location
        if d == ORIENTATIONS.index('>'):
            target = r, c + 1, d
        elif d == ORIENTATIONS.index('<'):
            target = r, c - 1, d
        elif d == ORIENTATIONS.index('v'):
            target = r + 1, c, d
        elif d == ORIENTATIONS.index('^'):
            target = r - 1, c, d
        else:
            raise ValueError(d)

        # Move if not blocked, otherwise return the current location
        if self.grid[target[0]][target[1]] == '#':
            return r, c, d
        else:
            return target

    def move(self, r, c, d):
        """Move one step."""
        # Determine where we are on the current square
        lr, lc, curr_square = self.to_local_coord(r, c)
        curr_edge = self.get_edge_name(lr, lc, d)

        # Try to move if we are not on the edge of the square
        if curr_edge is None:
            return self.try_move(r, c, d)

        # We are on the edge of a square, determine where it maps to and see if we can move there
        target_square, target_edge = self.squares[curr_square].connects[curr_edge]
        match target_edge:
            case "right":
                target_dir = ORIENTATIONS.index('<')
                lc_new = self.square_dim - 1
                match curr_edge:
                    case "right": lr_new = self.mirror_coord(lr)
                    case "bottom": lr_new = lc
                    case "left": lr_new = lr
                    case "top": lr_new = self.mirror_coord(lc)
            case "bottom":
                target_dir = ORIENTATIONS.index('^')
                lr_new = self.square_dim - 1
                match curr_edge:
                    case "right": lc_new = lr
                    case "bottom": lc_new = self.mirror_coord(lc)
                    case "left": lc_new = self.mirror_coord(lr)
                    case "top": lc_new = lc
            case "left":
                target_dir = ORIENTATIONS.index('>')
                lc_new = 0
                match curr_edge:
                    case "right": lr_new = lr
                    case "bottom": lr_new = self.mirror_coord(lc)
                    case "left": lr_new = self.mirror_coord(lr)
                    case "top": lr_new = lc
            case "top":
                target_dir = ORIENTATIONS.index('v')
                lr_new = 0
                match curr_edge:
                    case "right": lc_new = self.mirror_coord(lr)
                    case "bottom": lc_new = lc
                    case "left": lc_new = lr
                    case "top": lc_new = self.mirror_coord(lc)

        # Move if not blocked, otherwise return the current location
        target_row, target_col = self.to_global_coord(lr_new, lc_new, target_square)
        if grid[target_row][target_col] == '#':
            return r, c, d
        else:
            return target_row, target_col, target_dir

    def navigate(self, start, commands):
        """Navigate by following the commands."""
        facing = ORIENTATIONS.index('>')
        row, col = start
        while commands:
            cmd, arg = commands.pop(0)
            if cmd == "move":
                for _ in range(arg):
                    row, col, facing = self.move(row, col, facing)
            elif cmd == "rotate":
                if arg == 'R':
                    facing = (facing + 1) % len(ORIENTATIONS)
                else:
                    facing = (facing - 1) % len(ORIENTATIONS)
            else:
                pass

        return row, col, facing


# Compute password for given location and direction faced
def compute_password(r, c, d):
    return 1000 * (r + 1) + 4 * (col + 1) + facing


# Our input's squares look like this:
#   1122
#   1122
#   33
#   33
# 4455
# 4455
# 66
# 66

# Part 1: find the password by moving on the map
square1 = Square(id=1, loc=(0, 1), connects={"right": (2, "left"), "bottom": (3, "top"), "left": (2, "right"), "top": (5, "bottom")})
square2 = Square(id=2, loc=(0, 2), connects={"right": (1, "left"), "bottom": (2, "top"), "left": (1, "right"), "top": (2, "bottom")})
square3 = Square(id=3, loc=(1, 1), connects={"right": (3, "left"), "bottom": (5, "top"), "left": (3, "right"), "top": (1, "bottom")})
square4 = Square(id=4, loc=(2, 0), connects={"right": (5, "left"), "bottom": (6, "top"), "left": (5, "right"), "top": (6, "bottom")})
square5 = Square(id=5, loc=(2, 1), connects={"right": (4, "left"), "bottom": (1, "top"), "left": (4, "right"), "top": (3, "bottom")})
square6 = Square(id=6, loc=(3, 0), connects={"right": (6, "left"), "bottom": (4, "top"), "left": (6, "right"), "top": (4, "bottom")})
squares1 = {1: square1, 2: square2, 3: square3, 4: square4, 5: square5, 6: square6}

navigator1 = MapNavigator(grid, squares1, 50)
row, col, facing = navigator1.navigate(start, commands.copy())
print(f"Password: {compute_password(row, col, facing)}")

# Part 2: find the password by moving on a cube
square1 = Square(id=1, loc=(0, 1), connects={"right": (2, "left"), "bottom": (3, "top"), "left": (4, "left"), "top": (6, "left")})
square2 = Square(id=2, loc=(0, 2), connects={"right": (5, "right"), "bottom": (3, "right"), "left": (1, "right"), "top": (6, "bottom")})
square3 = Square(id=3, loc=(1, 1), connects={"right": (2, "bottom"), "bottom": (5, "top"), "left": (4, "top"), "top": (1, "bottom")})
square4 = Square(id=4, loc=(2, 0), connects={"right": (5, "left"), "bottom": (6, "top"), "left": (1, "left"), "top": (3, "left")})
square5 = Square(id=5, loc=(2, 1), connects={"right": (2, "right"), "bottom": (6, "right"), "left": (4, "right"), "top": (3, "bottom")})
square6 = Square(id=6, loc=(3, 0), connects={"right": (5, "bottom"), "bottom": (2, "top"), "left": (1, "top"), "top": (4, "bottom")})
squares2 = {1: square1, 2: square2, 3: square3, 4: square4, 5: square5, 6: square6}

navigator2 = MapNavigator(grid, squares2, 50)
row, col, facing = navigator2.navigate(start, commands.copy())
print(f"Password: {compute_password(row, col, facing)}")
