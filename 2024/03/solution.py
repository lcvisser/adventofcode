import re

# Read data
input_file = "2024/03/input.txt"
with open(input_file) as f:
    data = f.read()

mul = re.compile(r"mul\((\d+),(\d+)\)")
instructions = mul.findall(data)
total1 = sum(int(a) * int(b) for a, b in instructions)

# Part 1: sum of all mul() instruction results
print(f"Sum of all multiplications: {total1}")

do = re.compile(r"do\(\)")
dont = re.compile(r"don\'t\(\)")

current_do = do.search(data, 0)
current_dont = dont.search(data, 0)
current_mul = mul.search(data, 0)

total2 = 0
enable_mul = True
while current_mul is not None:
    current_mul_start = current_mul.start()

    if current_do is None:
        current_do_start = len(data)
    else:
        current_do_start = current_do.start()

    if current_dont is None:
        current_dont_start = len(data)
    else:
        current_dont_start = current_dont.start()

    current_pos = min([current_mul_start, current_do_start, current_dont_start])
    if current_pos == current_mul_start:
        if enable_mul:
            total2 += int(current_mul.group(1)) * int(current_mul.group(2))

        current_mul = mul.search(data, current_mul.end())
    elif current_pos == current_do_start:
        enable_mul = True
        current_do = do.search(data, current_do.end())
    elif current_pos == current_dont_start:
        enable_mul = False
        current_dont = dont.search(data, current_dont.end())

# Part 2: sum of all enabled mul() instruction results
print(f"Sum of all enabled multiplications: {total2}")
