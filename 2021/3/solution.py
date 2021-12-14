import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Part 1: power consumption
length = None
zeros_counts = None
ones_counts = None
for number in data.split('\n'):
    number = number.strip()

    # Skip possible empty lines
    if not number:
        continue

    # Initialize counters
    if length is None:
        length = len(number)
        zeros_counts = [0] * length
        ones_counts = [0] * length

    # Parse number
    for i, x in enumerate(number):
        if x == '0':
            zeros_counts[i] += 1
        elif x == '1':
            ones_counts[i] += 1
        else:
            print(f"Unknown value: `{x}`")

# Determine gamma rate
gamma_rate_binary = [1 if ones > zeros else 0 for zeros, ones in zip(zeros_counts, ones_counts)]
gamma_rate = sum(n << i for i, n in enumerate(reversed(gamma_rate_binary)))

# Epsilon rate is bitwise inverse
epsilon_rate = (2 ** length - 1) ^ gamma_rate

# Answer
print("gamma_rate={}, epsilon_rate={}, answer={}".format(gamma_rate, epsilon_rate, gamma_rate * epsilon_rate))
