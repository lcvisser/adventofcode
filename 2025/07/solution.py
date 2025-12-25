with open("2025/07/input.txt") as f:
    data = f.read()

num_splits = 0
beams = None
for row in data.strip().split("\n"):
    for i, c in enumerate(row):
        if c == "S":
            beams = ["."] * len(row)
            beams[i] = "|"
            break

        if c == "^" and beams[i] == "|":
            num_splits += 1
            beams[i - 1] = "|"
            beams[i] = "."
            beams[i + 1] = "|"

print(f"Number of splits: {num_splits}")
