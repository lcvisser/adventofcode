# Read data
input_file = "2024/09/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse the disk map
is_file = True
file_id = 0
file_blocks = []
file_positions = {}
file_sizes = {}
free_spaces = {}
current_position = 0
for n in [int(x) for x in data.strip()]:
    if is_file:
        file_blocks += [file_id] * n
        file_positions[file_id] = current_position
        file_sizes[file_id] = n
        file_id += 1
        is_file = False
    else:
        free_spaces[current_position] = n
        is_file = True

    current_position += n

# Move file blocks and compute checksum
free_space = list(free_spaces.values())
checksum1 = 0
moving_file = False
current_position = 0
while file_blocks:
    if moving_file:
        to_move = free_space.pop(0)
        for i in range(to_move):
            fid = file_blocks.pop()
            checksum1 += current_position * fid
            current_position += 1
        moving_file = False
    else:
        fid = file_blocks.pop(0)
        checksum1 += current_position * fid
        current_position += 1

        if not file_blocks:
            break

        if file_blocks[0] != fid:
            moving_file = True

# Part 1: checksum after file compacting
print(f"Checksum: {checksum1}")

# Move entire files and compute checksum
checksum2 = 0
while file_sizes:
    fid, file_size = file_sizes.popitem()
    sorted_free_space_positions = sorted(free_spaces.keys())
    for target_pos in sorted_free_space_positions:
        free_space_size = free_spaces[target_pos]
        if target_pos < file_positions[fid] and free_space_size >= file_size:
            # Free space at the current position of the file
            current_pos = file_positions[fid]
            free_spaces[current_pos] = file_size

            # Gobble right
            if current_pos + file_size in sorted_free_space_positions:
                right_free_space_position = current_pos + file_size
                right_free_space_size = free_spaces[right_free_space_position]
                free_spaces[current_pos] += right_free_space_size
                del free_spaces[right_free_space_position]

            # Gobble left
            p = current_pos
            while p >= 0:
                p -= 1
                if p in sorted_free_space_positions:
                    left_free_space_position = p
                    left_free_space_size = free_spaces[left_free_space_position]
                    if left_free_space_position + left_free_space_size == current_pos:
                        free_spaces[left_free_space_position] += free_spaces[current_pos]
                        del free_spaces[current_pos]

                    break  # only one position to try!

            # Move the file
            file_positions[fid] = target_pos

            # Update the free space at the new location
            del free_spaces[target_pos]
            free_spaces[target_pos + file_size] = free_space_size - file_size

            break

    checksum2 += sum(fid * (file_positions[fid] + i) for i in range(file_size))

# Part 2: checkusm after moving entire files
print(f"Checksum: {checksum2}")
