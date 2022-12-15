import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

data_example = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

# Parse data
sensor_coverage_at_target_row = []
beacons = []
target_row = 2000000  # 10
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
    if beacon_pos[1] == target_row:
        beacons.append(beacon_pos[0])

    # Determine the maximum coverage of this sensor in x-direction
    dist_to_nearest_beacon = abs(beacon_pos[0] - sensor_pos[0]) + abs(beacon_pos[1] - sensor_pos[1])
    coverage_min_x = sensor_pos[0] - dist_to_nearest_beacon
    coverage_max_x = sensor_pos[0] + dist_to_nearest_beacon
    min_x = min(min_x, coverage_min_x)
    max_x = max(max_x, coverage_max_x)

    # Determine coverage at target row
    startrow_range = sensor_pos[1] - dist_to_nearest_beacon
    endrow_range = sensor_pos[1] + dist_to_nearest_beacon
    if startrow_range <= target_row <= endrow_range:
        w = dist_to_nearest_beacon - abs(sensor_pos[1] - target_row)
        coverage = (sensor_pos[0] - w, sensor_pos[0] + w)
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
    target_row_coverage[-min_x + b] = 'B'

# Part 1: number of positions that cannot have a beacon
print(f"Number of positions that cannot have a beacon at y={target_row}: {target_row_coverage.count('#')}")
