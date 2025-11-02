with open("2015/02/input.txt") as f:
    data = f.read()

# Part 1
total = 0
for gift in data.strip().split():
    l, w, h = [int(d) for d in gift.split("x")]
    sides = [l * w, w * h, h * l]
    smallest = sorted(sides)[0]
    needed = 2 * sum(sides) + smallest
    total += needed

print(f"Total gift wrapping paper needed: {total} feet")
