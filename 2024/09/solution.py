# Read data
input_file = "2024/09/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse the disk map
is_file = True
file_id = 0
file_blocks = []
free_space = []
for n in [int(x) for x in data.strip()]:
    if is_file:
        file_blocks += [file_id] * n
        file_id += 1
        is_file = False
    else:
        free_space.append(n)
        is_file = True

# Move files and compute checksum
checksum = 0
moving_file = False
current_position = 0
while True:
    if moving_file:
        to_move = free_space.pop(0)
        for i in range(to_move):
            fid = file_blocks.pop()
            checksum += current_position * fid
            current_position += 1
        moving_file = False
    else:
        if not file_blocks:
            break

        fid = file_blocks.pop(0)
        checksum += current_position * fid
        current_position += 1

        if file_blocks[0] != fid:
            moving_file = True

# Part 1: checksum after file compacting
print(f"Checksum: {checksum}")
