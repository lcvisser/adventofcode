import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


COLORS = ["red", "green", "blue"]
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

# Parse data
possible_games = []
min_powers = []
for game in data.strip().split('\n'):
    game_id, reveals = game.split(':')
    game_no = int(game_id[len("Game "):])

    all_reveals_possible = True
    min_counts = {c: 0 for c in COLORS}
    for reveal in reveals.split(';'):
        cubes = reveal.split(',')
        counts = {color: int(count) for count, color in [c.strip().split(' ') for c in cubes]}

        if counts.get("red", 0) > MAX_RED or counts.get("green", 0) > MAX_GREEN or counts.get("blue", 0) > MAX_BLUE:
            all_reveals_possible = False

        for c in COLORS:
            min_counts[c] = max(min_counts[c], counts.get(c, 0))

    if all_reveals_possible:
        # All reveals possible
        possible_games.append(game_no)

    min_powers.append(min_counts["red"] * min_counts["green"] * min_counts["blue"])

# Part 1: sum of possible game IDs
print(f"Sum of possible game IDs: {sum(possible_games)}")

# Part 2: sum of minimal power sets
print(f"Sum of minimal power sets: {sum(min_powers)}")
