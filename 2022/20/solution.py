import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
encrypted_data = [int(x) for x in data.strip().split('\n')]

# Decrypt
def init(encrypted_data, key=1):
    return [(i, x * key) for i, x in enumerate(encrypted_data)]

def decrypt(encrypted_file, previous=None):
    if previous is None:
        decrypted_file = encrypted_file.copy()
    else:
        decrypted_file = previous
    num = len(encrypted_file)

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

    return decrypted_file


def compute_coordinate(decrypted_file):
    num = len(decrypted_file)

    # Find the location of the zero
    zeroindex = None
    for i, (_, v) in enumerate(decrypted_file):
        if v == 0:
            zeroindex = i
            break

    # Compute the coordinate
    item1000 = decrypted_file[(zeroindex + 1000) % num]
    item2000 = decrypted_file[(zeroindex + 2000) % num]
    item3000 = decrypted_file[(zeroindex + 3000) % num]
    return sum([v for _, v in [item1000, item2000, item3000]])

# Part 1: coordinate after mixing once
ef = init(encrypted_data)
df = decrypt(ef)
coordinate1 = compute_coordinate(df)
print(f"Coordinate after mixing once: {coordinate1}")

# Part 2: coordinate after mixing ten times
ef = init(encrypted_data, key=811589153)
df = None
for _ in range(10):
    df = decrypt(ef, df)

coordinate2 = compute_coordinate(df)
print(f"Coordinate after mixing ten times: {coordinate2}")
