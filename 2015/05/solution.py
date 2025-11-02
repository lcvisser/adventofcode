import re

with open("2015/05/input.txt") as f:
    data = f.read()

VOWELS = re.compile(r"[aeiou]")
PAIR = re.compile(r"([a-z])\1")
BAD_TUPLE = re.compile(r"ab|cd|pq|xy")

nice_string_count = 0
for s in data.strip().split():
    has_three_vowels = len(VOWELS.findall(s)) >= 3
    has_pair = PAIR.search(s) is not None
    has_bad_tuple = BAD_TUPLE.search(s) is not None

    if has_three_vowels and has_pair and not has_bad_tuple:
        nice_string_count += 1

print(f"Number of nice strings: {nice_string_count}")
