import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

numbers = []
for number in data.split('\n'):
    number = number.strip()
    if number:
        numbers.append(number)

# Part 1: power consumption
bits_per_position = zip(*numbers)
value_counts_per_position = [(n.count('0'), n.count('1')) for n in bits_per_position]
zeros_counts, ones_counts = zip(*value_counts_per_position)

# Determine gamma rate
gamma_rate_binary = [1 if ones > zeros else 0 for zeros, ones in zip(zeros_counts, ones_counts)]
gamma_rate = sum(n << i for i, n in enumerate(reversed(gamma_rate_binary)))

# Epsilon rate is bitwise inverse
epsilon_rate = (2 ** len(numbers[0]) - 1) ^ gamma_rate

# Answer
print("gamma_rate={}, epsilon_rate={}, answer={}".format(gamma_rate, epsilon_rate, gamma_rate * epsilon_rate))

# Part 2: life support
def reduce(remaining_numbers, keep, tie_condition, iteration=0):
    # Check for final number reached
    if len(remaining_numbers) == 1:
        return remaining_numbers[0]

    # Count bits values per position
    bits_per_position = list(zip(*remaining_numbers))
    zeros_counts = bits_per_position[iteration].count('0')
    ones_counts = bits_per_position[iteration].count('1')

    # Determine which one to keep
    if keep == "most":
        value_keep_zeros_gt_ones = '0'
        value_keep_zeros_lt_ones = '1'
    elif keep == "fewest":
        value_keep_zeros_gt_ones = '1'
        value_keep_zeros_lt_ones = '0'

    # Filter the remaining numbers
    if zeros_counts > ones_counts:
        filtered_numbers = filter(lambda n: n[iteration] == value_keep_zeros_gt_ones, remaining_numbers)
    elif zeros_counts < ones_counts:
        filtered_numbers = filter(lambda n: n[iteration] == value_keep_zeros_lt_ones, remaining_numbers)
    else:
        filtered_numbers = filter(lambda n: n[iteration] == tie_condition, remaining_numbers)

    # Filter recursively
    return reduce(list(filtered_numbers), keep, tie_condition, iteration + 1)

# Convert binary to integer
oxygen_rate = int(reduce(numbers, keep="most", tie_condition='1'), base=2)
carbon_rate = int(reduce(numbers, keep="fewest", tie_condition='0'), base=2)

# Answer
print("oxygen_rate={}, carbon_rate={}, answer={}".format(oxygen_rate, carbon_rate, oxygen_rate * carbon_rate))
