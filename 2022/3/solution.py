import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

# Part 1: sum of priorities
total_priority = 0
for line in lines:
    if line.strip() == '':
        continue

    n = len(line)
    assert(n % 2 == 0)

    compartment1, compartment2 = set(line[0:n//2]), set(line[n//2:])
    in_both = compartment1 & compartment2
    assert(len(in_both) == 1)

    priority = ord(in_both.pop())
    if 65 <= priority <= 90:
        priority -= 38
    elif 97 <= priority <= 122:
        priority -= 96
    else:
        raise ValueError(priority)

    total_priority += priority

print(f"Sum of priorities: {total_priority}")
