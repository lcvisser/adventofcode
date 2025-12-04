from operator import add, sub

with open("2025/01/input.txt") as f:
    data = f.read()

rotate = {"L": add, "R": sub}

# Part 1
dial = 50
password = 0
for instruction in data.strip().split("\n"):
    d = instruction[0]
    n = int(instruction[1:])
    dial = rotate[d](dial, n) % 100
    if dial == 0:
        password += 1

print(f"The password is: {password}")

# Part 2
dial = 50
password = 0
for instruction in data.strip().split("\n"):
    d = instruction[0]
    n = int(instruction[1:])
    for i in range(n):
        dial = rotate[d](dial, 1) % 100
        if dial == 0:
            password += 1

print(f"The password is: {password}")
