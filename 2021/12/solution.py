import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
neighbors = {}
for edge in data.strip().split('\n'):
    start_node, end_node = edge.split('-')

    # Reverse nodes if "start" is the end node or "end" is the start"
    if end_node == "start" or start_node == "end":
        start_node, end_node = end_node, start_node

    # Add edge
    if start_node not in neighbors.keys():
        neighbors[start_node] = []
    neighbors[start_node].append(end_node)

    # If not at the starting node or end node, also add the reverse edge
    if start_node != "start" and end_node != "end":
        if end_node not in neighbors.keys():
            neighbors[end_node] = []
        neighbors[end_node].append(start_node)

# Define recursive travel function for part 1
paths1 = []
def travel1(current_node, path=None):
    # Initialize path if needed
    if path is None:
        path = []

    # Add current node to the path
    path.append(current_node)

    # Visit neighbors
    for neighbor in neighbors[current_node]:
        if neighbor == "end":
            # Path completed
            completed_path = path.copy()
            completed_path.append("end")
            paths1.append(completed_path)
        elif neighbor.islower() and neighbor in path:
            # We cannot go here, already visited
            pass
        else:
            # Continue travelling
            travel1(neighbor, path.copy())

# Part 1: determine number of valid paths
travel1("start")
print("Number of paths found: {}".format(len(paths1)))

# Define recursive travel function for part 2
paths2 = []
def travel2(current_node, path=None, any_small_cave_visited_twice=False):
    # Initialize path if needed
    if path is None:
        path = []

    # Add current node to the path
    path.append(current_node)

    # Visit neighbors
    for neighbor in neighbors[current_node]:
        if neighbor == "end":
            # Path completed
            completed_path = path.copy()
            completed_path.append("end")
            paths2.append(completed_path)
        elif neighbor.islower() and neighbor in path:
            if any_small_cave_visited_twice is False:
                # Small cave already visited, but only once, and no other small caves visited twice yet, so continue
                travel2(neighbor, path.copy(), True)
            else:
                pass
        else:
            # Continue travelling
            travel2(neighbor, path.copy(), any_small_cave_visited_twice)

# Part 2: determine number of valid paths with new rules
travel2("start")
print("Number of paths found: {}".format(len(paths2)))
