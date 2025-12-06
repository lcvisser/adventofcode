with open("2025/03/input.txt") as f:
    data = f.read()

total_joltage = 0
for bank in data.strip().split("\n"):
    batteries = [int(v) for v in bank]
    num_batteries = len(batteries)
    joltage_tens = 0
    joltage_ones = 0
    for i, b in enumerate(batteries):
        if b > joltage_tens and i < num_batteries - 1:
            joltage_tens = b
            joltage_ones = batteries[i + 1]
        elif b > joltage_ones:
            joltage_ones = b

    total_joltage += 10 * joltage_tens + joltage_ones

print(f"Total joltage: {total_joltage}")
