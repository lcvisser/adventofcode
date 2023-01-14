import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

numbers = [int(x) for x in data.split()]

# Part one: find two numbers that add up to 2020 and compute their product
for i, a in enumerate(numbers):
    for _, b in enumerate(numbers[i:]):
        if a + b == 2020:
            print(a, b, a + b, a * b)

# Part two: find three numbers that add up to 2020 and compute their product
for i, a in enumerate(numbers):
    for j, b in enumerate(numbers[i:]):
        for _, c in enumerate(numbers[i + j:]):
            if a + b + c == 2020:
                print(a, b, c, a + b + c, a * b * c)
