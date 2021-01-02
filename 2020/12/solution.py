from math import pi, sin, cos
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


# data = """
# F10
# N3
# F7
# R90
# F11
# """

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
