import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')
template = lines[0]

insertions = {}
for line in lines[2:]:
    pair, insertion = [s.strip() for s in line.split('->')]
    insertions[pair] = insertion

# Process template
polymer = template
for i in range(10):
    j = 0
    while j < len(polymer):
        pair = polymer[j:j + 2]
        if pair in insertions:
            polymer = polymer[:j + 1] + insertions[pair] + polymer[j + 1:]
            j += 2
        else:
            j += 1

# Determine most and least common elements
elements = set(polymer)
element_counts = [(e, polymer.count(e)) for e in elements]
max_element = max(element_counts, key=lambda x: x[1])
min_element = min(element_counts, key=lambda x: x[1])

# Part 1: difference between most and least common elements after 10 iterations
print("Answer: {}".format(max_element[1] - min_element[1]))
