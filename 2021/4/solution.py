
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# A board and some helper functions
class Board:
    def __init__(self, board_number, board):
        self._board_number = board_number
        self._board = board
        self._sum_all_numbers = sum(sum(row) for row in board)
        self._rc = [0] * 5
        self._cc = [0] * 5

    @property
    def board_number(self):
        return self._board_number

    def has_won(self):
        return 5 in self._rc or 5 in self._cc

    def sum_unmarked(self):
        return self._sum_all_numbers

    def add_drawn_number(self, number):
        for r, row in enumerate(self._board):
            for c, n in enumerate(row):
                if n == number:
                    self._rc[r] += 1
                    self._cc[c] += 1
                    self._sum_all_numbers -= number
                    return

# Play function
def play(boards, numbers):
    for n in numbers:
        for board in boards:
            board.add_drawn_number(n)
            if board.has_won():
                print("board {} has won: sum={}, last_number={}, answer={}".format(
                    board.board_number,
                    board.sum_unmarked(),
                    n,
                    board.sum_unmarked() * n
                ))
                return
    else:
        print("no winner")

# Parse data
lines = data.split('\n')

numbers_to_draw = [int(n) for n in lines.pop(0).split(',')]
lines.pop(0)  # empty line

boards = []
for i in range(len(lines) // 6):
    board = [[int(n) for n in filter(None, line.split(' '))] for line in lines[6 * i:6 * i + 5]]
    boards.append(Board(i, board))

# Part 1: play the game
play(boards, numbers_to_draw)
