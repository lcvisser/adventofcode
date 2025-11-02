with open("2015/02/input.txt") as f:
    data = f.read()

total_paper = 0
total_ribbon = 0
for gift in data.strip().split():
    l, w, h = [int(d) for d in gift.split("x")]
    sides_area = [l * w, w * h, h * l]
    sides_perimeter = [2 * (l + w), 2 * (w + h), 2 * (h + l)]

    smallest_area = sorted(sides_area)[0]
    paper_needed = 2 * sum(sides_area) + smallest_area
    total_paper += paper_needed

    smallest_perimeter = sorted(sides_perimeter)[0]
    ribbon_needed = smallest_perimeter + l * w * h
    total_ribbon += ribbon_needed


# Part 1
print(f"Total gift wrapping paper needed: {total_paper} feet")

# Part 2:
print(f"Total ribbon needed: {total_ribbon} feet")
