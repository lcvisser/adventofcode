import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


data = """
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
num = len(encrypted_file)

decrypted_file = encrypted_file.copy()
# print(0, [v for _, v in decrypted_file])
for i in range(num):

    item = encrypted_file[i]
    _, value = item
    if value == 0:
        continue

    curr = decrypted_file.index(item)
    goto = decrypted_file[(curr + value) % num]
    decrypted_file.pop(curr)
    move_index = decrypted_file.index(goto)

    if value > 0:
        decrypted_file.insert(move_index + 1, item)
    else:
        if move_index == 0:
            decrypted_file.append(item)
        else:
            decrypted_file.insert(move_index, item)


    # print(i + 1, [v for _, v in decrypted_file])

# print('-', [v for _, v in decrypted_file])
zeroindex = None
for i, (_, v) in enumerate(decrypted_file):
    if v == 0:
        zeroindex = i
        break

item1000 = decrypted_file[(zeroindex + 1000) % num]
item2000 = decrypted_file[(zeroindex + 2000) % num]
item3000 = decrypted_file[(zeroindex + 3000) % num]
print(sum([v for _, v in [item1000, item2000, item3000]]))
