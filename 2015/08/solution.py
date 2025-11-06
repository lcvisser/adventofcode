with open("2015/08/input.txt", "rb") as f:
    data = f.read()

# Part 1
code_length = 0
char_length = 0
for d in data.strip().split(b'\n'):
    code_length += len(d)
    s = d.decode("unicode_escape")
    char_length += len(s) - 2  # -2 for the enclosing quotes

print(f"code_length - char_length = {code_length - char_length}")
