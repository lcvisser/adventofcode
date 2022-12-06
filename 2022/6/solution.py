import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Part 1: find unique preamble
mark = -1;
for i in range(len(data) - 4):
    preamble = set(data[i:i + 4])
    if len(preamble) == 4:
        mark = i + 4
        break

print(f"First occurence of unique preamble: {mark}")
