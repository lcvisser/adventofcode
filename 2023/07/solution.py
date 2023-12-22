import sys
import collections
import enum
import functools


# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
hands = []
for line in data.strip().split('\n'):
    hand, bid = line.split()
    hands.append((hand, int(bid)))


CARDS = "123456789TJQKA"

class HandType(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def get_hand_type(hand):
    # Counter.most_common returns a list of N 2-tuples (key, value); maximum compare is 2 (for full house or two pair)
    count = collections.Counter(hand)
    highest_counts = count.most_common(2)
    most_common1 = highest_counts[0][1]
    if most_common1 != 5:
        most_common2 = highest_counts[1][1]
    else:
        most_common2 = 0

    if most_common1 == 5:
        return HandType.FIVE_OF_A_KIND
    elif most_common1 == 4:
        return HandType.FOUR_OF_A_KIND
    elif most_common1 == 3 and most_common2 == 2:
        return HandType.FULL_HOUSE
    elif most_common1 == 3 and most_common2 != 2:
        return HandType.THREE_OF_A_KIND
    elif most_common1 == 2 and most_common2 == 2:
        return HandType.TWO_PAIR
    elif most_common1 == 2 and most_common2 != 2:
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD

def hand_compare(hand1, hand2):
    hand_type1 = get_hand_type(hand1)
    hand_type2 = get_hand_type(hand2)
    if hand_type1 != hand_type2:
        # Primary rule (type-based)
        return hand_type1 - hand_type2
    else:
        # Secondary rule (high-card based)
        for c1, c2 in zip(hand1, hand2):
            if c1 != c2:
                return CARDS.index(c1) - CARDS.index(c2)

        raise RuntimeError

def hand_compare_helper(h1, h2):
    return hand_compare(h1[0], h2[0])


# Part 1: sum of bid times rank
hands.sort(key=functools.cmp_to_key(hand_compare_helper))
score = [(r + 1) * b for r, (_, b) in enumerate(hands)]
print(f"Winnings: {sum(score)}")
