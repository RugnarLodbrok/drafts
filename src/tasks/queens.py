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

    pieces = {piece: [i for i, v in enumerate(slots_mask) if v] for piece, slots_mask in pieces.items()}
    yield from dancing_lynx(pieces, primary=set(range(2 * n)))


if __name__ == '__main__':
    for i, s in enumerate(queens(8)):
        print(i, s)
