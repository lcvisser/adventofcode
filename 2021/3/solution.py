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
