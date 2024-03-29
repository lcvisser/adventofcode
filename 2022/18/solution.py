import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
XY = {}
XZ = {}
YZ = {}
cubes = []
maxx = 0
maxy = 0
maxz = 0

# Helper function to update plane views
def add_to_planes(x, y, z):
    xy = (x, y)
    if xy not in XY.keys():
        XY[xy] = []
    if z not in XY[xy]:
        XY[xy].append(z)

    xz = (x, z)
    if xz not in XZ.keys():
        XZ[xz] = []
    if y not in XZ[xz]:
        XZ[xz].append(y)

    yz = (y, z)
    if yz not in YZ.keys():
        YZ[yz] = []
    if x not in YZ[yz]:
        YZ[yz].append(x)

for cube in data.strip().split('\n'):
    x, y, z = [int(n) for n in cube.split(',')]
    cubes.append((x, y, z))
    add_to_planes(x, y, z)
    maxx = max(maxx, x)
    maxy = max(maxy, y)
    maxz = max(maxz, z)


# Helper function to count faces per plane view
def count_faces(plane):
    potential_pockets = []
    face_count = 0
    for coord, col in plane.items():
        prev_h = None
        for h in sorted(col):
            if prev_h is None:
                col_face_count = 1  # face of bottom cube
                prev_h = h
            else:
                if h > prev_h + 1:
                    # Pocket
                    face_count += 2  # close previous stack, start new stack
                    for i in range(prev_h + 1, h):
                        potential_pockets.append((coord, i))

            prev_h = h

        col_face_count += 1  # final face
        face_count += col_face_count

    return face_count, potential_pockets

# Part 1: surface area
xy_faces, pockets_xy = count_faces(XY)
xz_faces, pockets_xz = count_faces(XZ)
yz_faces, pockets_yz = count_faces(YZ)
print(f"Surface area: {xy_faces + xz_faces + yz_faces}")

# Part 2: remove pockets
potential_pockets1 = set((x, y, z) for (x, y), z in pockets_xy)
potential_pockets2 = set((x, y, z) for (x, z), y in pockets_xz)
potential_pockets3 = set((x, y, z) for (y, z), x in pockets_yz)
potential_pockets = potential_pockets1.intersection(potential_pockets2).intersection(potential_pockets3)

# Flood-fill to detect which places are on the outside
start = (0, 0, 0)
assert start not in cubes
filled = set()
to_visit = [start]
while to_visit:
    v = to_visit.pop(0)
    x, y, z = v

    if v not in filled:
        filled.add(v)

    neighbors = [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1)
    ]

    for w in filter(lambda _w: 0 <= _w[0] <= maxx and 0 <= _w[1] <= maxy and 0 <= _w[2] <= maxz, neighbors):
        if w not in filled and w not in to_visit and w not in cubes:
            to_visit.append(w)

# Find the actual pockets by removing the filled places from the set of potential pockets
actual_pockets = potential_pockets.difference(filled)

# Now really fill the actual pockets so they don't get counted
for p in actual_pockets:
    add_to_planes(*p)

# Count again the number of faces, but now with all the pockets filled
xy_faces, _ = count_faces(XY)
xz_faces, _ = count_faces(XZ)
yz_faces, _ = count_faces(YZ)
print(f"Surface area without pockets: {xy_faces + xz_faces + yz_faces}")
