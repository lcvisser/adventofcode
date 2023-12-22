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


class HandType(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def get_hand_type(hand, use_jokers=False):
    # Count cards
    count = collections.Counter(hand)

    # Use jokers to raise the highest count even higher
    if use_jokers and 'J' in count:
        num_jokers = count['J']
        count['J'] = 0
    else:
        num_jokers = 0

    # Counter.most_common returns a list of N 2-tuples (key, value); maximum compare is 2 (for full house or two pair)
    highest_counts = count.most_common(2)
    most_common1 = highest_counts[0][1] + num_jokers  # no effect if use_jokers == False
    if most_common1 != 5:
        most_common2 = highest_counts[1][1]
    else:
        most_common2 = 0

    # Determine type
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

def hand_compare(hand1, hand2, cards, use_jokers=False):
    hand_type1 = get_hand_type(hand1, use_jokers)
    hand_type2 = get_hand_type(hand2, use_jokers)
    if hand_type1 != hand_type2:
        # Primary rule (type-based)
        return hand_type1 - hand_type2
    else:
        # Secondary rule (high-card based)
        for c1, c2 in zip(hand1, hand2):
            if c1 != c2:
                return cards.index(c1) - cards.index(c2)

        raise RuntimeError

# Part 1: sum of bid times rank
def hand_compare_helper1(h1, h2):
    cards = "23456789TJQKA"
    return hand_compare(h1[0], h2[0], cards, use_jokers=False)

score1 = [(r + 1) * b for r, (_, b) in enumerate(sorted(hands, key=functools.cmp_to_key(hand_compare_helper1)))]
print(f"Winnings: {sum(score1)}")

# Part 2: sum of bid times rank with jokers
def hand_compare_helper2(h1, h2):
    cards = "J23456789TQKA"
    return hand_compare(h1[0], h2[0], cards, use_jokers=True)

score2 = [(r + 1) * b for r, (_, b) in enumerate(sorted(hands, key=functools.cmp_to_key(hand_compare_helper2)))]
print(f"Winnings with jokers: {sum(score2)}")
