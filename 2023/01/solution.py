
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
calibration_values = []
for line in data.strip().split('\n'):
    digits = [int(c) for c in line if c in "0123456789"]
    calibration_values.append(10 * digits[0] + digits[-1])

# Part 1: sum of calibration values:
print(f"Sum of calibration values: {sum(calibration_values)}")
