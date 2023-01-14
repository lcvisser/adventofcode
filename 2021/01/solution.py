import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

numbers = [int(x) for x in data.split()]

# Part 1: find number of times measurement increased from one the next.
increased = 0
for previous, current in zip(numbers[0:-1], numbers[1:]):
    if current > previous:
        increased += 1

print(f"Number of measurements that increased: {increased}")

# Part 2: find number of times measurement window sum increased from one to the next.
increased = 0
for i in range(1, len(numbers) - 1):
    window_a = sum(numbers[i - 1:i + 2])
    window_b = sum(numbers[i:i + 3])
    if window_b > window_a:
        increased += 1

print(f"Number of windowed measurements that increased: {increased}")
