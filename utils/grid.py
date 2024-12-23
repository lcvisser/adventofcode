def parse_grid(data):
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

    return grid, width, height


def print_grid(g):
    for row in g:
        print(''.join('.' if x == 0 else str(x) for x in row))
    print()