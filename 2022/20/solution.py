import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


data_ex = """
1
2
-3
3
-2
0
4
"""

# Parse data
encrypted_file = [(i, int(x)) for i, x in enumerate(data.strip().split('\n'))]
decrypted_file = encrypted_file.copy()
num = len(encrypted_file)

# Decrypt
for i in range(num):
    # Find the original item at this location
    item = encrypted_file[i]
    _, value = item
    if value == 0:
        continue

    # Determine where it is now and how much it should move (abs(v) // v gives the sign, abs(v) % (n - 1) the number of
    # places we need to move; the -1 is because n - 1 moves in the circular list brings us back to the orginal
    # position)
    curr = decrypted_file.index(item)
    to_move = (abs(value) // value) * (abs(value) % (num - 1))

    # Determine which index we need to insert after
    if to_move > 0:
        index_to_insert_after = (curr + to_move) % num
    else:
        index_to_insert_after = (curr + to_move) % num - 1  # if we move backwards, we need to go one further

    # Track the item we want to insert after and remove the item being moved
    item_to_insert_after = decrypted_file[index_to_insert_after]
    decrypted_file.remove(item)

    # Find the target item back and insert after it
    goto = decrypted_file.index(item_to_insert_after)
    decrypted_file.insert(goto + 1, item)

# Find the location of the zero
zeroindex = None
for i, (_, v) in enumerate(decrypted_file):
    if v == 0:
        zeroindex = i
        break

# Part 1: coordinate after mixing
item1000 = decrypted_file[(zeroindex + 1000) % num]
item2000 = decrypted_file[(zeroindex + 2000) % num]
item3000 = decrypted_file[(zeroindex + 3000) % num]
coordinate = sum([v for _, v in [item1000, item2000, item3000]])
print(f"Coordinate: {coordinate}")
