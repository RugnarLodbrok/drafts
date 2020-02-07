"""
https://leetcode.com/problems/n-queens/

The n-queens puzzle is the problem of placing n queens on an n×n chessboard such that no two queens attack each other.



Given an integer n, return all distinct solutions to the n-queens puzzle.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space respectively.

Example:

Input: 4
Output: [
 [".Q..",  // Solution 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // Solution 2
  "Q...",
  "...Q",
  ".Q.."]
]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above.
"""
from py_tools.common import add_to_pythonpath

add_to_pythonpath(__file__, 2)

from src.dancing_lynx import dancing_lynx


def queens_4(n):
    assert n == 4, "not implemented"
    Y = {  # _   x-coord     y-coord     diag           r-diag
        (0, 0): [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        (0, 1): [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        (0, 2): [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        (0, 3): [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],

        (1, 0): [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        (1, 1): [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        (1, 2): [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        (1, 3): [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],

        (2, 0): [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        (2, 1): [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        (2, 2): [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        (2, 3): [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],

        (3, 0): [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        (3, 1): [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        (3, 2): [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        (3, 3): [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    }
    Y = {piece: [i for i, v in enumerate(slots_mask) if v] for piece, slots_mask in Y.items()}
    X = set(range(7))
    print("x, y:")
    print(X)
    print(Y)
    print("solutions:")
    yield from dancing_lynx(Y, primary=set(range(7)))


def queens(n):
    n_slots = 6 * (n - 1)

    pieces = {}
    for i in range(n):
        for j in range(n):
            constrains = [0 for _ in range(n_slots)]
            constrains[i] = 1  # x-constrain
            constrains[n + j] = 1  # y-constrain
            d = j + i - (n - 1)
            if abs(d) < n - 1:
                d += n - 2
                constrains[2 * n + d] = 1  # diag
            d = j - i
            if abs(d) < n - 1:
                d += n - 2
                constrains[4 * n - 3 + d] = 1  # r-diag
            pieces[(i, j)] = constrains

    for piece, constrains in pieces.items():
        print(piece, constrains)
        if piece[1] == n - 1:
            print("")
    # convert masks to values
    pieces = {piece: [i for i, v in enumerate(slots_mask) if v] for piece, slots_mask in pieces.items()}
    yield from dancing_lynx(pieces, primary=set(range(2 * n)))


if __name__ == '__main__':
    for s in queens(4):
        print(s)
