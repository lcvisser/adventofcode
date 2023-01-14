import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

tickets = data.split()

# Traverse the space [a, b) with the instructions in path
def binary_path(a, b, path):
    for d in path:
        delta = (b - a) // 2
        if d in ('F', 'L'):
            a, b = a, a + delta
        elif d in ('B', 'R'):
            a, b = a + delta, b
        else:
            raise ValueError

    return a

# Part 1: find the highest seat id in the list
highest_uid = -1
for ticket in tickets:
    row = binary_path(0, 128, ticket[:7])
    seat = binary_path(0, 8, ticket[7:])
    uid = row * 8 + seat
    if uid > highest_uid:
        highest_uid = uid

print(f"Highest seat id: {highest_uid}")

# Part 2: find your seat ID
uids = []
for ticket in tickets:
    row = binary_path(0, 128, ticket[:7])
    seat = binary_path(0, 8, ticket[7:])
    uid = row * 8 + seat
    uids.append(uid)

uids.sort()
for i in range(len(uids) - 1):
    diff = uids[i + 1] - uids[i]
    if diff == 2:
        my_uid = (uids[i] + uids[i + 1]) // 2
        break

print(f"My uid: {my_uid}")
