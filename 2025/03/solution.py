with open("2025/03/input.txt") as f:
    data = f.read()

def compute_joltage(num_pos):
    total_joltage = 0
    for bank in data.strip().split("\n"):
        batteries = [int(v) for v in bank]
        joltage = [0] * num_pos
        batteries_used = [None] * num_pos
        for i, b in enumerate(batteries):
            for j in range(num_pos):
                if b > joltage[j] and i not in batteries_used[:j] and i < len(batteries) - (num_pos - j - 1):
                    joltage[j:] = batteries[i:i + 1 + (num_pos - j - 1)]
                    batteries_used[j:] = list(range(i, i + num_pos - j))
                    break

        total_joltage += sum(10**i * j for i, j in enumerate(reversed(joltage)))

    return total_joltage

# Part 1
print(f"Total joltage for n= 2: {compute_joltage(2)}")

# Part 2
print(f"Total joltage for n=12: {compute_joltage(12)}")
