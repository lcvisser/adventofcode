import re

with open("2025/02/input.txt") as f:
    data = f.read()

# Part 1
TWICE_REPEATED_SEQUENCE = re.compile(r"([0-9]+)(\1)")

sum_of_invalid_ids1 = 0
for rng in data.strip().split(","):
    lower, upper = rng.split("-")
    for i in range(int(lower), int(upper) + 1):
        if TWICE_REPEATED_SEQUENCE.fullmatch(str(i)):
            sum_of_invalid_ids1 += i

print(f"Sum of invalid IDs: {sum_of_invalid_ids1}")

# Part 2
REPEATED_SEQUENCES = re.compile(r"([0-9]+)\1+")

sum_of_invalid_ids2 = 0
for rng in data.strip().split(","):
    lower, upper = rng.split("-")
    for i in range(int(lower), int(upper) + 1):
        if REPEATED_SEQUENCES.fullmatch(str(i)):
            sum_of_invalid_ids2 += i

print(f"Sum of invalid IDs: {sum_of_invalid_ids2}")
