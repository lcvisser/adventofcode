import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


def check_correct_order(left, right):
    decided = False
    correct = False
    if type(left) == int and type(right) == int:
        if left < right:
            decided = True
            correct = True
        elif left == right:
            decided = False
            correct = False
        else:
            decided = True
            correct = False
    else:
        if type(left) == int:
            left = [left]
        if type(right) == int:
            right = [right]

        nl = len(left)
        nr = len(right)
        if nl == 0 and nr == 0:
            decided = False
            correct = False
        else:
            while left and right and not decided:
                ll = left.pop(0)
                rr = right.pop(0)
                correct, decided = check_correct_order(ll, rr)
                if decided:
                    break
            else:
                nl = len(left)
                nr = len(right)
                if nl == 0 and nr > 0:
                    decided = True
                    correct = True
                elif nl > 0 and nr == 0:
                    decided = True
                    correct = False
                else:
                    decided = False
                    correct = False

    return correct, decided

# Part 1: sum of indices of correct pairs of packets
sum_correct_indices = 0
for index, pair in enumerate(data.strip().split("\n\n")):
    leftstr, rightstr = pair.split('\n')
    left = eval(leftstr)
    right = eval(rightstr)

    in_order, _ = check_correct_order(left, right)
    if in_order:
        sum_correct_indices += (index + 1)

print(f"Sum of indices: {sum_correct_indices}")
