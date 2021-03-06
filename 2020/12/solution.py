from math import pi, sin, cos
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

instructions = []
for line in data.split('\n'):
    try:
        instr = line[0]
        arg = int(line[1:])
    except (IndexError, ValueError):
        continue

    instructions.append((instr, arg))

# Part 1: move the ship according to the instructions
class Ship:
    def __init__(self):
        self._orientation = 0
        self._x = 0
        self._y = 0

    def _update_orientation(self, instr, arg):
        if instr == 'L':
            self._orientation += arg
        elif instr == 'R':
            self._orientation -= arg
        else:
            raise ValueError("wrong instruction: {}".format(instr))

    def _update_location(self, instr, arg):
        if instr == 'N':
            self._y += arg
        elif instr == 'S':
            self._y -= arg
        elif instr == 'E':
            self._x += arg
        elif instr == 'W':
            self._x -= arg
        else:
            raise ValueError("wrong instruction: {}".format(instr))

    def _move(self, instr, arg):
        if instr == 'F':
            angle = self._orientation / 180 * pi
            self._x += int(arg * cos(angle))
            self._y += int(arg * sin(angle))
        else:
            raise ValueError("wrong instruction: {}".format(instr))

    def handle_instruction(self, instr, arg):
        if instr in ('L', 'R'):
            self._update_orientation(instr, arg)
        elif instr in ('N', 'S', 'E', 'W'):
            self._update_location(instr, arg)
        else:
            self._move(instr, arg)

    @property
    def position(self):
        return self._x, self._y, self._orientation

ship = Ship()
for x in instructions:
    ship.handle_instruction(*x)

distance = abs(ship.position[0]) + abs(ship.position[1])
print(f"Manhattan distance travelled: {distance}")

# Part 2: move the waypoint according to the instructions
class ShipWithWaypoint:
    def __init__(self, u0=10, v0=1):
        self._x = 0
        self._y = 0
        self._u = u0
        self._v = v0

    def _rotate_waypoint(self, instr, arg):
        if instr == 'L':
            angle = arg / 180 * pi
        elif instr == 'R':
            angle = -arg / 180 * pi
        else:
            raise ValueError("wrong instruction: {}".format(instr))

        u = int(round(cos(angle) * self._u - sin(angle) * self._v))
        v = int(round(sin(angle) * self._u + cos(angle) * self._v))
        self._u, self._v = u, v

    def _move_waypoint(self, instr, arg):
        if instr == 'N':
            self._v += arg
        elif instr == 'S':
            self._v -= arg
        elif instr == 'E':
            self._u += arg
        elif instr == 'W':
            self._u -= arg
        else:
            raise ValueError("wrong instruction: {}".format(instr))

    def _move_ship(self, instr, arg):
        if instr == 'F':
            self._x += arg * self._u
            self._y += arg * self._v
        else:
            raise ValueError("wrong instruction: {}".format(instr))

    def handle_instruction(self, instr, arg):
        if instr in ('L', 'R'):
            self._rotate_waypoint(instr, arg)
        elif instr in ('N', 'S', 'E', 'W'):
            self._move_waypoint(instr, arg)
        else:
            self._move_ship(instr, arg)

    @property
    def position(self):
        return self._x, self._y, self._u, self._v

ship = ShipWithWaypoint()
for x in instructions:
    ship.handle_instruction(*x)

distance = abs(ship.position[0]) + abs(ship.position[1])
print(f"Manhattan distance travelled: {distance}")
