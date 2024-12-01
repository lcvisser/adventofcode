# Read data
input_file = "2024/01/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
left_list_str, right_list_str = zip(*[x.split() for x in data.strip().split('\n')])
left_list = [int(x) for x in left_list_str]
right_list = [int(x) for x in right_list_str]

# Sort both lists
left_list.sort()
right_list.sort()

distances = [abs(a - b) for a, b in zip(left_list, right_list)]

# Part 1: sum of distances
print(f"Sum of distances: {sum(distances)}")
