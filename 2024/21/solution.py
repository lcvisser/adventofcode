import functools
import math

# Numeric keypad
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
numeric_keypad = {
#  from   to : direction
    'A': {          '0': '<',           '3': '^'},
    '0': {                    'A': '>', '2': '^'},
    '1': {                    '2': '>', '4': '^'},
    '2': {'0': 'v', '1': '<', '3': '>', '5': '^'},
    '3': {'A': 'v', '2': '<',           '6': '^'},
    '4': {'1': 'v',           '5': '>', '7': '^'},
    '5': {'2': 'v', '4': '<', '6': '>', '8': '^'},
    '6': {'3': 'v', '5': '<',           '9': '^'},
    '7': {'4': 'v',           '8': '>'          },
    '8': {'5': 'v', '7': '<', '9': '>'          },
    '9': {'6': 'v', '8': '<'                    }
}

# Directional keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
directional_keypad = {
#  from   to : direction
    'A': {'>': 'v', '^': '<'                    },
    '^': {'v': 'v',           'A': '>'          },
    '<': {                    'v': '>'          },
    'v': {          '<': '<', '>': '>', '^': '^'},
    '>': {          'v': '<',           'A': '^'}
}

KEYPADS = {
    "numeric": numeric_keypad,
    "directional": directional_keypad
}


@functools.cache
def find_movement(src, dst, keypad_name):
    keypad = KEYPADS[keypad_name]

    # Depth-first search to find all paths and determine the shortest
    to_visit = [(src, "", "", 0)]  # current, path, directions, score
    lowest_score = math.inf
    shortest_path = ""
    while to_visit:
        curr, path, directions, score = to_visit.pop(0)

        if curr == dst:
            if score <= lowest_score:
                shortest_path = directions
                lowest_score = score
            continue

        for nxt, dir in keypad[curr].items():
            if nxt not in path:
                s = score
                if directions != "":
                    # Prefer to go in straight lines
                    if dir == directions[-1]:
                        s += 1
                    else:
                        s += 1000
                else:
                    s += 1  # first step, direction doesn't matter

                to_visit.insert(0, (nxt, path + nxt, directions + dir, s))

    return shortest_path


def find_sequence_for_keypad(code, keypad_name):
    sequence = ""
    for s, d in zip(code[:-1], code[1:]):
        sequence += find_movement(s, d, keypad_name)
        sequence += 'A'  # push the button

    return sequence


def find_sequence_for(code):
    numeric_keypad_sequence = find_sequence_for_keypad('A' + code, "numeric")
    directional_keypad_sequence1 = find_sequence_for_keypad('A' + numeric_keypad_sequence, "directional")
    directional_keypad_sequence2 = find_sequence_for_keypad('A' + directional_keypad_sequence1, "directional")
    return directional_keypad_sequence2


# Read data
input_file = "2024/21/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
codes = data.strip().split('\n')

# Compute complexities and sum
complexities = []
for code in codes:
    seq = find_sequence_for(code)
    length = len(seq)
    value = int(code[:-1])
    complexities.append(length * value)

# Part 1
print(f"Sum of complexities: {sum(complexities)}")
