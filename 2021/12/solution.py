from os import path

import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
neighbors = {}
for edge in data.strip().split('\n'):
    start_node, end_node = edge.split('-')

    # Add edge
    if start_node not in neighbors.keys():
        neighbors[start_node] = []
    neighbors[start_node].append(end_node)

    # If not at the starting node or end node, also add the reverse edge
    if start_node != "start" and end_node != "end":
        if end_node not in neighbors.keys():
            neighbors[end_node] = []
        neighbors[end_node].append(start_node)

# Define recursive travel function
paths = []
def travel(current_node, path=None):
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
            paths.append(completed_path)
        elif neighbor.islower() and neighbor in path:
            # We cannot go here, already visited
            pass
        else:
            # Continue travelling
            travel(neighbor, path.copy())

# Part 1: determine number of valid paths
travel("start")
print("Number of paths found: {}".format(len(paths)))
