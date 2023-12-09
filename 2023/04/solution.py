import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
total_points = 0
for card in data.strip().split('\n'):
    _, numbers = card.split(':')
    winning_numbers_str, given_numbers_str = numbers.split('|')
    winning_numbers = set(int(s) for s in winning_numbers_str.split())
    given_numbers = set(int(s) for s in given_numbers_str.split())

    m = len(given_numbers & winning_numbers)
    if m > 0:
        total_points += 2**(m - 1)

# Part 1: total number of points
print(f"Total number of points: {total_points}")
