import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

def char_to_priority(c):
    priority = ord(c)
    if 65 <= priority <= 90:
        priority -= 38
    elif 97 <= priority <= 122:
        priority -= 96
    else:
        raise ValueError(priority)

    return priority


# Part 1: sum of priorities
total_priority = 0
for line in lines:
    n = len(line)
    assert(n % 2 == 0)

    compartment1, compartment2 = set(line[0:n//2]), set(line[n//2:])
    in_both = compartment1 & compartment2
    assert(len(in_both) == 1)

    priority = char_to_priority(in_both.pop())
    total_priority += priority

print(f"Sum of priorities: {total_priority}")

# Part 2: sum of badge priorities
assert(len(lines) % 3 == 0)
i = 0
total_badge_priority = 0
while i < len(lines):
    group1, group2, group3 = [set(g) for g in lines[i:i+3]]
    badge = group1 & group2 & group3
    assert(len(badge) == 1)

    priority = char_to_priority(badge.pop())
    total_badge_priority += priority
    i += 3;

print(f"Sum of badge priorities: {total_badge_priority}")
