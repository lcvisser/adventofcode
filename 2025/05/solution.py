with open("2025/05/input.txt") as f:
    data = f.read()

fresh, available = data.strip().split("\n\n")

fresh_id_ranges = []
for r in fresh.strip().split("\n"):
    start, end = [int(v) for v in r.split("-")]
    fresh_id_ranges.append((start, end))

# Part 1
num_fresh = 0
for a in available.strip().split("\n"):
    for start, end in fresh_id_ranges:
        if start <= int(a) <= end:
            num_fresh += 1
            break

print(f"Number of fresh ingredients: {num_fresh}")
