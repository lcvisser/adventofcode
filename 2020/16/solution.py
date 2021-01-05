import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# data = """class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50

# your ticket:
# 7,1,14

# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12"""

sections = data.split("\n\n")

# Parse fields and values
valid_ranges = {}
for line in sections[0].split('\n'):
    field, values = line.split(':')
    valid_ranges[field] = []
    for range_str in values.split(" or "):
        lower, upper = [int(v) for v in range_str.strip().split('-')]
        valid_ranges[field].append((lower, upper))

# Part 1: scan for invalid tickets
rate = 0
for line in sections[2].split('\n'):
    if len(line) == 0:
        continue
    if line.startswith("nearby tickets:"):
        continue

    values = [int(v) for v in line.split(',')]
    for v in values:
        validated = False
        for field, ranges in valid_ranges.items():
            if validated:
                break

            for lower, upper in ranges:
                if lower <= v <= upper:
                    validated = True
                    break

        if not validated:
            rate += v

print(f"Rate: {rate}")
