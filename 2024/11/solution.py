import functools

# Read data
input_file = "2024/11/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
numbers = [int(x) for x in data.strip().split()]

# Rule implementation
def apply_rules(output_list, n):
    if output_list is None:
        output_list = []

    if n == 0:
        output_list.append(1)
    elif len(str(n)) % 2 == 0:
        n_string = str(n)
        half = len(n_string) // 2
        n1 = int(n_string[:half])
        n2 = int(n_string[half:])
        output_list += [n1, n2]
    else:
        output_list.append(n * 2024)

    return output_list

# Apply rules 25 times
for n in range(25):
    numbers = functools.reduce(apply_rules, numbers, None)

# Part 1: number of stones after 25 blinks
print(f"Number of stones: {len(numbers)}")
