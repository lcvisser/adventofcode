import copy
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
octopuses = []
for line in data.strip().split('\n'):
    octopuses.append(list(int(x) for x in line))

# Simulation class
class Simulation:
    def __init__(self, grid):
        self._grid = grid
        self._height = len(grid)
        self._width = len(grid[0])

        self._all_cells = set()
        for i in range(self._height):
            for j in range(self._width):
                self._all_cells.add((i, j))

        self._needs_to_flash = []
        self._has_flashed = []
        self.num_flashes = 0

    def __repr__(self):
        return '\n'.join(str(r) for r in self._grid) + '\n'

    def increment_all(self):
        """Increment the entire grid."""
        for i in range(self._height):
            for j in range(self._width):
                self._grid[i][j] += 1

    def increment_nearby(self, r, c):
        """Increment the cells around (r,c)."""
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    pass
                else:
                    if 0 <= r + i < self._height and 0 <= c + j < self._width:
                        self._grid[r + i][c + j] += 1

    def check_all(self):
        """Check the entire grid for octopuses that reached the flash threshold."""
        for i in range(self._height):
            for j in range(self._width):
                if self._grid[i][j] > 9:
                    self._needs_to_flash.append((i, j))

    def check_nearby(self, r, c):
        """Check the cells around (r, c) for octopuses that reached the flash threshold."""
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    pass
                else:
                    if 0 <= r + i < self._height and 0 <= c + j < self._width:
                        if self._grid[r + i][c + j] > 9 and (r + i, c + j) not in self._has_flashed:
                            self._needs_to_flash.append((r + i, c + j))

    def flash(self):
        """Let the octpuses flash."""
        # Flash octopuses that reached the energy level and propagate if needed
        while self._needs_to_flash:
            r, c = self._needs_to_flash.pop(0)
            if (r, c) not in self._has_flashed:
                self.num_flashes += 1
                self._has_flashed.append((r, c))
                self.increment_nearby(r, c)
                self.check_nearby(r, c)

        # Check if the entire grid has flashed
        if set(self._has_flashed) == self._all_cells:
            return True
        else:
            # Reset the energy levels from octopuses that have flashed
            while self._has_flashed:
                r, c = self._has_flashed.pop(0)
                self._grid[r][c] = 0
            return False

    def run_one_step(self):
        """Run a single simulation step."""
        self.increment_all()
        self.check_all()
        return self.flash()

# Part 1: simulate 100 steps
sim = Simulation(copy.deepcopy(octopuses))
for i in range(100):
    sim.run_one_step()

print(f"Number of observed flashes: {sim.num_flashes}")

# Part 2: simulate until all octopuses sync
sim = Simulation(copy.deepcopy(octopuses))
synced = False
iteration = 0
while not synced:
    synced = sim.run_one_step()
    iteration += 1
print(f"First iteration to sync: {iteration}")
