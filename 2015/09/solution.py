import re

with open("2015/09/input.txt") as f:
    data = f.read()

DISTANCE = re.compile("([a-zA-Z]+) to ([a-zA-Z]+) = ([0-9]+)")

all_cities = set()
distances = dict()
for line in data.strip().split("\n"):
    m = DISTANCE.match(line)
    src, dst, d = m.groups()

    all_cities.add(src)
    all_cities.add(dst)

    if src not in distances.keys():
        distances[src] = []

    if dst not in distances.keys():
        distances[dst] = []

    distances[src].append((dst, int(d)))
    distances[dst].append((src, int(d)))

# Part 1
shortest_distance = float("inf")
for starting_point in all_cities:
    current_city = starting_point
    current_distance = 0
    current_path = [current_city]

    to_visit = [(current_city, current_distance, current_path)]
    while to_visit:
        current_city, current_distance, path = to_visit.pop(0)

        if set(path) == all_cities:
            if current_distance < shortest_distance:
                shortest_distance = current_distance

        for next_city, next_dist in distances[current_city]:
            if next_city not in path:
                next_path = path.copy()
                next_path.append(next_city)
                to_visit.append((next_city, current_distance + next_dist, next_path))

print(f"Shortest path: {shortest_distance}")
