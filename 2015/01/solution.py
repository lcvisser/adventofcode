with open("2015/01/input.txt", "r") as f:
    instructions = f.read()

# Part 1
current_floor = 0
for c in instructions:
    if c == "(":
        current_floor += 1
    elif c == ")":
        current_floor -= 1

print(f"Final floor: {current_floor}")

# Part 2
current_floor = 0
target_floor = -1
character_index = 0
for i, c in enumerate(instructions):
    if c == "(":
        current_floor += 1
    elif c == ")":
        current_floor -= 1

    if current_floor == target_floor:
        character_index = i + 1  # starting index is 1
        break

print(f"First time to reach target floor at character: {character_index}")
