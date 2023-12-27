import re
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
rows = []
for line in data.strip().split('\n'):
    record, gs_str = line.split()
    gs = [int(n) for n in gs_str.split(',')]
    rows.append((record, gs))


SPRING_MATCHER = re.compile(r"#+")
def determine_arrangements(record, required_groups):
    to_check = [(0, '')]
    valid_arrangements = []
    while to_check:
        i, arrangement = to_check.pop(0)

        # Count groups in current arrangement
        group_lengths = [len(g) for g in SPRING_MATCHER.findall(arrangement)]
        if group_lengths == required_groups and '#' not in record[i:]:
            # Group requirement met and no more springs left in the record
            valid_arrangements.append(arrangement)
            continue

        # Check if following this branch makes sense (abort if groups so far are not following requirement)
        ng = len(group_lengths)
        if ng > 0 and group_lengths[:ng - 1] != required_groups[:ng - 1]:
            continue

        # End of record
        if i == len(record):
            continue

        # Next arrangement
        s = record[i]
        if s == '?':
            to_check.append((i + 1, arrangement + '#'))
            to_check.append((i + 1, arrangement + '.'))
        else:
            to_check.append((i + 1, arrangement + s))

    return valid_arrangements

# Part 1: sum of all arrangements
num_arrangements = []
for r in rows:
    a = determine_arrangements(*r)
    num_arrangements.append(len(a))

print(f"Sum of all arrangements: {sum(num_arrangements)}")
