import heapq
import itertools
import math

with open("2025/08/input.txt") as f:
   data = f.read()

junction_boxes = []
for row in data.strip().split("\n"):
    x, y, z = [int(v) for v in row.split(",")]
    junction_boxes.append((x, y, z))

def dist(first, second):
    x1, y1, z1 = first
    x2, y2, z2 = second
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

distances = []
for first, second in itertools.combinations(junction_boxes, 2):
    d = dist(first, second)
    heapq.heappush(distances, (d, (first, second)))

circuits = []

num_connections_to_make = 1000
connections_made = 0
while True:
    _, (first, second) = heapq.heappop(distances)
    first_in_circuit = None
    second_in_circuit = None
    for c in range(len(circuits)):
        if first in circuits[c]:
            first_in_circuit = c

        if second in circuits[c]:
            second_in_circuit = c

    if first_in_circuit is None and second_in_circuit is None:
        # New circuit
        circuits.append({first, second})
    elif first_in_circuit == second_in_circuit:
        # Nothing to do
        pass
    elif first_in_circuit is not None and second_in_circuit is None:
        # Connect
        circuits[first_in_circuit].add(second)
    elif first_in_circuit is None and second_in_circuit is not None:
        # Connect
        circuits[second_in_circuit].add(first)
    else:
        # Merge
        circuits[first_in_circuit].update(circuits[second_in_circuit])
        del circuits[second_in_circuit]

    connections_made += 1
    if connections_made == num_connections_to_make:
        # Part 1:
        sorted_circuits = sorted(circuits, key=lambda c: len(c), reverse=True)

        p = 1
        for i in range(3):
            p *= len(sorted_circuits[i])

        print(f"Product of lengths of 3 longest circuits: {p}")

    if connections_made > 2 and len(circuits) == 1 and len(circuits[0]) == len(junction_boxes):
        # Part 2:
        print(f"Product of x-coordinates of final connection: {first[0] * second[0]}")
        break
