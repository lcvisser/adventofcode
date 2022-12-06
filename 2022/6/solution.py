import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

def find_marker(data, length):
    mark = -1;
    for i in range(len(data) - length):
        preamble = set(data[i:i + length])
        if len(preamble) == length:
            mark = i + length
            break

    return mark

# Part 1: find preamble of length 4
mark = find_marker(data, 4)
print(f"First occurence of unique preamble: {mark}")

# Part 2: find message of length 14
mark = find_marker(data, 14)
print(f"First occurence of unique message: {mark}")
