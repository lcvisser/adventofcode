import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

dataex = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

# Parse data
XY = {}
XZ = {}
YZ = {}
for cube in data.strip().split('\n'):
    x, y, z = [int(n) for n in cube.split(',')]

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

# Helper function to count faces per plane
def count_faces(plane):
    face_count = 0
    for col in plane.values():
        prev_h = None
        for h in sorted(col):
            if prev_h is None:
                col_face_count = 1  # face of bottom cube
                prev_h = h
            else:
                if h > prev_h + 1:
                    face_count += 2  # close previous stack, start new stack

            prev_h = h

        col_face_count += 1  # final face
        face_count += col_face_count

    return face_count

# Part 1: surface area
xy_faces = count_faces(XY)
xz_faces = count_faces(XZ)
yz_faces = count_faces(YZ)
print(f"Surface area: {xy_faces + xz_faces + yz_faces}")
