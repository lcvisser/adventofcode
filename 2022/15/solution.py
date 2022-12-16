import sys
import heapq

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


class Sensor:
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.distance_to_beacon = d

        self.coverage_firstrow = self.y - d
        self.coverage_lastrow = self.y + d

    def has_coverage(self, row):
        return self.coverage_firstrow <= row <= self.coverage_lastrow

    def coverage(self, row):
        if self.has_coverage(row):
            w = self.distance_to_beacon - abs(self.y - row)
            return self.x - w, self.x + w
        else:
            return None


# Parse data
target_row = 2000000
sensor_coverage_at_target_row = []
sensors = []
beacons = []
min_x = 0
max_x = 0
for line in data.strip().split('\n'):
    sensor_info, beacon_info = line.split(':')
    sensor_info = sensor_info[len("Sensor at "):]
    sensor_pos = [int(s[2:]) for s in sensor_info.split(', ')]
    beacon_info = beacon_info[len(" closest beacon is at "):]
    beacon_pos = [int(s[2:]) for s in beacon_info.split(', ')]

    # Keep track of area size
    min_x = min(min_x, sensor_pos[0])
    max_x = max(max_x, sensor_pos[0])
    min_x = min(min_x, beacon_pos[0])
    max_x = max(max_x, beacon_pos[0])

    # Keep track of beacons on the target row
    beacons.append(beacon_pos)

    # Configure the sensor
    dist_to_nearest_beacon = abs(beacon_pos[0] - sensor_pos[0]) + abs(beacon_pos[1] - sensor_pos[1])
    sensor = Sensor(*sensor_pos, dist_to_nearest_beacon)
    sensors.append(sensor)

    # Determine the maximum coverage of this sensor in x-direction
    coverage_min_x, coverage_max_x = sensor.coverage(sensor_pos[1])
    min_x = min(min_x, coverage_min_x)
    max_x = max(max_x, coverage_max_x)

    # Determine coverage at target row
    coverage = sensor.coverage(target_row)
    if coverage is not None:
        sensor_coverage_at_target_row.append(coverage)
        min_x = min(min_x, coverage[0])
        max_x = max(max_x, coverage[1])

# Build the coverage map at the target row
target_row_width = max_x - min_x + 1
target_row_coverage = ['.'] * target_row_width
for cs, ce in sensor_coverage_at_target_row:
    for i in range(cs, ce + 1):
        target_row_coverage[-min_x + i] = '#'
for b in beacons:
    if b[1] == target_row:
        target_row_coverage[-min_x + b[0]] = 'B'

# Part 1: number of positions that cannot have a beacon
print(f"Number of positions that cannot have a beacon at y={target_row}: {target_row_coverage.count('#')}")

# Part 2: find the distress beacon
max_dim = 4000000
found = False
for r in range(max_dim + 1):
    total_coverage = []
    for s in sensors:
        sensor_coverage = s.coverage(r)
        if sensor_coverage is None:
            continue

        # Sort sensor coverage by start and end using heapq
        ss, se = sensor_coverage
        ss = max(0, ss)
        se = min(max_dim, se)
        c = (ss, se)
        heapq.heappush(total_coverage, c)

    # Determine total coverage by popping from heap
    cs = 0
    ce = 1
    while total_coverage and not found:
        ss, se = heapq.heappop(total_coverage)
        if ss > ce + 1:
            # Gap in coverage, beacon found!
            hidden_x = ce + 1
            hidden_y = r
            found = True
        else:
            # Adjacent or covering; merge
            if se > ce:
                ce = se

    if found:
        break

# Tuning frequency of hidden beacon
frequency = hidden_x * max_dim + hidden_y
print(f"Hidden beacon at x={hidden_x}, y={hidden_y}; tuning frequency: {frequency}")
