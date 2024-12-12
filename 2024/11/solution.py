import collections
import functools

# Read data
input_file = "2024/11/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
numbers = [int(x) for x in data.strip().split()]

# Rule implementation
def apply_rules(n):
    if n == 0:
       return [1]
    elif len(str(n)) % 2 == 0:
        n_string = str(n)
        half = len(n_string) // 2
        n1 = int(n_string[:half])
        n2 = int(n_string[half:])
        return [n1, n2]
    else:
        return [n * 2024]


def apply_rules_reduce(output_list, n):
    if output_list is None:
        output_list = []

    new_n = apply_rules(n)
    output_list.extend(new_n)
    return output_list

# Apply rules 25 times
numbers1 = numbers.copy()
for _ in range(25):
    numbers1 = functools.reduce(apply_rules_reduce, numbers1, None)

# Part 1: number of stones after 25 blinks
print(f"Number of stones after 25 blinks: {len(numbers1)}")

numbers2 = numbers.copy()
counter = collections.Counter(numbers2)
for _ in range(75):
    old_counts = collections.Counter()
    new_counts = collections.Counter()

    for number, count in counter.items():
        old_counts[number] = count

        # Must iteratively update new_counts, for case NN -> N, N
        new_numbers = apply_rules(number)
        for n in new_numbers:
            new_counts.update({n: count})

    counter -= old_counts
    counter += new_counts

# Part 2: number of stones after 75 blinks
print(f"Number of stones after 75 blinks: {counter.total()}")
