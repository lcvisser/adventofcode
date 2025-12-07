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

# Part 2
num_ids = 0
last_end = 0
for start, end in sorted(fresh_id_ranges, key=lambda r: r[0]):
    if start <= last_end:
        start = last_end + 1

    if end <= last_end:
        continue

    num_ids += end - start + 1
    last_end = end

print(f"Number of fresh IDs: {num_ids}")
