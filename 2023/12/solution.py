import re
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

data2 = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
# Parse data
rows = []
for line in data.strip().split('\n'):
    record, gs_str = line.split()
    gs = [int(n) for n in gs_str.split(',')]
    rows.append((record, gs))


SPRING_MATCHER = re.compile(r"#+")
def determine_arrangements(record, required_groups):
    to_check = [(0, '')]
    valid_arrangements = 0
    while to_check:
        i, arrangement = to_check.pop(0)

        # Count groups in current arrangement
        group_lengths = [len(g) for g in SPRING_MATCHER.findall(arrangement)]
        if group_lengths == required_groups and '#' not in record[i:]:
            # Group requirement met and no more springs left in the record
            valid_arrangements += 1
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
            to_check.insert(0, (i + 1, arrangement + '#'))
            to_check.insert(0, (i + 1, arrangement + '.'))
        else:
            to_check.insert(0, (i + 1, arrangement + s))

    return valid_arrangements

# Part 1: sum of all arrangements
num_arrangements1 = sum(determine_arrangements(r, g) for r, g in rows)
print(f"Sum of all arrangements: {num_arrangements1}")

# Part 2: sum of all arrangements when unfolded
num_arrangements2 = sum(determine_arrangements(f"{r}?{r}?{r}?{r}?{r}", g * 5) for r, g in rows)
print(f"Sum of all arrangements when unfolded: {num_arrangements2}")
