with open("2025/07/input.txt") as f:
    data = f.read()

num_splits = 0
beams = None
paths = None
for row in data.strip().split("\n"):
    for i, c in enumerate(row):
        if c == "S":
            beams = ["."] * len(row)
            beams[i] = "|"
            paths = [0] * len(row)
            paths[i] = 1
            break

        if c == "^" and beams[i] == "|":
            num_splits += 1
            beams[i - 1] = "|"
            beams[i] = "."
            beams[i + 1] = "|"
            p = paths[i]
            paths[i] = 0
            paths[i - 1] += p
            paths[i + 1] += p


print(f"Number of splits: {num_splits}")
print(f"Number of paths: {sum(paths)}")
