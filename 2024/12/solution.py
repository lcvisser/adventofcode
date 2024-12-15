# Read data
input_file = "2024/12/input.txt"
with open(input_file) as f:
    data = f.read()


DIRECTIONS = {
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1),
}


# Parse grid
grid = []
height = 0
width = 0
for r, row in enumerate(data.strip().split('\n')):
    height = r

    grid_row = []
    for c, ch in enumerate(row):
        width = c
        grid_row.append(ch)

    grid.append(grid_row)


# Helper functions for grid
def crop_at(x, y):
    if 0 <= x <= height and 0 <= y <= width:
        return grid[x][y]
    else:
        return None


def neighbours_of(x, y, crop):
    same_crop = []
    adjacent = {}
    for dir, (dx, dy) in DIRECTIONS.items():
        d = (x + dx, y + dy)
        c = crop_at(*d)
        if c == crop:
            same_crop.append(d)
        else:
            adjacent[dir] = d

    return same_crop, adjacent


FILL = '.'
def fill(x, y):
    grid[x][y] = FILL


def make_graph(plots):
    graph = dict()
    for plot, adjacent_plots in plots.items():
        x, y = plot
        for direction in adjacent_plots.keys():
            # The top-left corner has the same coordinate as the plot, the others are +1 in x and/or y direction from
            # it. Each corner can have only one edge (directed graph) by processing clock-wise.
            match direction:
                case "up":
                    src = (x, y)
                case "right":
                    src = (x, y + 1)
                case "down":
                    src = (x + 1, y + 1)
                case "left":
                    src = (x + 1, y)

            # "direction" is pointing to the side of the plot that has the "adj" plot, so the edge direction is rotated
            # 90 degrees right.
            idx = list(DIRECTIONS.keys()).index(direction)
            idx = (idx + 1) % 4
            edge_direction = list(DIRECTIONS.keys())[idx]

            # Determine source and destination node coordinates
            src_x, src_y = src
            dx, dy = DIRECTIONS[edge_direction]
            dst = (src_x + dx, src_y + dy)

            # Add to graph
            if src not in graph.keys():
                graph[src] = []
            graph[src].append(dst)

    return graph


def count_corners(graph):
    def _determine_direction(_curr, _nxt):
        delta = (_nxt[0] - _curr[0], _nxt[1] - _curr[1])
        for direction, d in DIRECTIONS.items():
            if delta == d:
                break

        return direction

    # Find a node that is on a corner
    curr = list(graph.keys())[0]  # arbitrary
    nxt = graph[curr][0]
    direction = _determine_direction(curr, nxt)
    while True:
        curr = nxt
        nxt = graph[curr][0]
        new_direction = _determine_direction(curr, nxt)
        if new_direction != direction:
            break

    # curr is now a node that is on a corner; remove from the graph
    corners = 1
    nxt = graph[curr].pop(0)
    if len(graph[curr]) == 0:
        del graph[curr]

    # Walk the graph; each corner is a new side
    start = curr
    prev_direction = _determine_direction(curr, nxt)
    while True:
        direction = _determine_direction(curr, nxt)
        if direction != prev_direction:
            corners += 1

        prev_direction = direction

        curr = nxt
        if curr in graph.keys():
            nxt = graph[curr].pop(0)
            if len(graph[curr]) == 0:
                del graph[curr]
        else:
            assert curr == start
            break

    if graph:
        # Still perimeter left, must be a loop!
        corners += count_corners(graph)

    return corners


def count_sides(perimeter_plots):
    perimeter_graph = make_graph(perimeter_plots)
    sides = count_corners(perimeter_graph)
    return sides


def determine_properties_of_area(sx, sy):
    crop = crop_at(sx, sy)
    area = 0
    perimeter = 0
    to_visit = [(sx, sy)]
    visited = set()
    perimeter_plots = dict()
    adjacent = set()

    # Fill to determine area
    while to_visit:
        current = to_visit.pop(0)
        if current not in visited:
            visited.add(current)
            x, y = current
            neighbours, adjacent_plots = neighbours_of(x, y, crop)
            area += 1
            perimeter += (4 - len(neighbours))

            # Keep track of perimeter plots for fencing later
            if adjacent_plots:
                perimeter_plots[current] = adjacent_plots

            # Plots to fill
            for n in neighbours:
                to_visit.append(n)

            # Keep track of adjacent plots with different crops
            for a in filter(lambda p: 0 <= p[0] <= height and 0 <= p[1] <= width, adjacent_plots.values()):
                adjacent.add(a)

    # Count sides of area
    sides = count_sides(perimeter_plots)

    # Set fill marker
    for v in visited:
        fill(*v)

    return area, perimeter, sides, adjacent


# Compute areas an perimeters to determine price
starting_points = [(0, 0)]
price = 0
price_discount = 0
while starting_points:
    # Next area (may be filled in the mean time though)
    start = starting_points.pop(0)
    crop = crop_at(*start)
    if crop == FILL:
        continue

    # Compute area and perimeter for pricing, save adjacent crop plots
    area, perimeter, sides, adjacent = determine_properties_of_area(*start)
    price += area * perimeter
    price_discount += area * sides

    # Add adjacent crop plots for future processing
    for a in filter(lambda x: crop_at(*x) != FILL, adjacent):
        starting_points.append(a)

# Part 1: price of fencing
print(f"Price of fencing: {price}")

# Part 2: price of fencing with discount
print(f"Discounted price of fencing: {price_discount}")
