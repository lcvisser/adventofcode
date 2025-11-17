s = "3113322113"

# Part 1
num_iter = 40
for i in range(num_iter):
    new_s = ""
    current_ch = s[0]
    count = 0
    while s:
        ch, s = s[0], s[1:]
        if ch == current_ch:
            count += 1
        else:
            new_s += f"{count}{current_ch}"
            current_ch = ch
            count = 1

    new_s += f"{count}{current_ch}"
    s = new_s

print(f"Length after {num_iter} iterations: {len(s)}")
