import sys
import copy

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

        # Put crate on stack (top stack is first element)
        if c == '[':
            stacks[stack_number].append(lines[i][n + 1])

    i += 1

# Parse the instructions
stacks1 = copy.deepcopy(stacks)
stacks2 = copy.deepcopy(stacks)
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

    # Part 1: restack crates one by one
    for j in range(amount):
        stacks1[dest_stack].insert(0, stacks1[source_stack].pop(0))

    # Part 2: restack crates all at once
    stacks2[dest_stack] = stacks2[source_stack][0:amount] + stacks2[dest_stack]
    for j in range(amount):
        stacks2[source_stack].pop(0)

    i += 1

# Part 1: top crate after restacking
top_crates1 = ''.join(s[0] for s in stacks1.values())
print(f"Top crates: {top_crates1}")

# Part 2: top crate after restacking
top_crates2 = ''.join(s[0] for s in stacks2.values())
print(f"Top crates: {top_crates2}")