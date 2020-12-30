import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

N = 25
queue = [0] * N
qsize = 0

# Part 1: find the first number that is not a sum of any two of the previous N numbers
index = -1
all_numbers = []
for line in data.split('\n'):
    try:
        x = int(line)
    except ValueError:
        continue
    index += 1
    all_numbers.append(x)

    valid_sums = []
    for i in range(N):
        for j in range(i + 1, N):
            s = queue[i] + queue[j]
            valid_sums.append(s)

    if x in valid_sums or qsize < N:
        queue = queue[1:] + [x]
        qsize += 1
    else:
        break

print(f"First invalid number: {x}")

# Part 2: find a the first invalid number and find the contiguous range of numbers before it that add up to that number
index = 0
numbers = []
while True:
    if sum(numbers) == x:
        break

    while sum(numbers) < x:
        numbers.append(all_numbers[index])
        index += 1

    while sum(numbers) > x:
        numbers.pop(0)

m, n = min(numbers), max(numbers)
print(f"Range found: min={m}, max={n}, sum={m+n}")
