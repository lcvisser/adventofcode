import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data (do NOT strip)
lines = data.split('\n')

# Determine initial crate stacking
i = 0
stacks = dict()
while lines[i].strip():
    stack_number = 0
    for n, c in enumerate(lines[i]):
        # New stack at column 0, 3, 7, 11, ...
        if n == 0 or (n + 1) % 4 == 0:
            stack_number += 1
            if stack_number not in stacks.keys():
                stacks[stack_number] = []

        # Crate
        if c == '[':
            stacks[stack_number].append(lines[i][n + 1])

    i += 1

# Parse the instructions
while i < len(lines):
    if lines[i].strip() == '':
        i += 1
        continue

    # Parse current instruction
    tokens = lines[i].split(' ')
    try:
        _, a, _, s, _, d = tokens
    except:
        print(tokens)

    amount = int(a)
    source_stack = int(s)
    dest_stack = int(d)

    # Top crate is the first element in the list
    for j in range(amount):
        stacks[dest_stack].insert(0, stacks[source_stack].pop(0))

    i += 1

# Part 1: top crate after restacking
top_crates = ''.join(s[0] for s in stacks.values())
print(f"Top crates: {top_crates}")
