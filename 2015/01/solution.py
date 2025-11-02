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
