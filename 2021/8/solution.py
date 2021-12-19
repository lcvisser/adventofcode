import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
all_patterns = []
all_outputs = []
for line in data.strip().split('\n'):
    pattern_str, output_str = line.split('|')
    pattern = pattern_str.strip().split(' ')
    output = output_str.strip().split(' ')
    all_patterns.append(pattern)
    all_outputs.append(output)

# Part 1: count occurences 1, 4, 7 and 8 in output
count = 0
for output in all_outputs:
    for n in output:
        if len(n) in (2, 4, 3, 7):
            count += 1

print(f"Answer: {count}")
