"""
https://leetcode.com/problems/sudoku-solver/

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
Empty cells are indicated by the character '.'.

Note:

The given board contain only digits 1-9 and the character '.'.
You may assume that the given Sudoku puzzle will have a single unique solution.
The given board size is always 9x9.

"""
from itertools import product

from src.dancing_lynx import DancingLynx


def sudoku(data):  # 27ms
    def get_possible_v(i, j):
        values = set(range(1, 10))
        for k in range(9):
            if data[i][k]:
                values.discard(data[i][k])
            if data[k][j]:
                values.discard(data[k][j])
        sq_i = (i // 3) * 3
        sq_j = (j // 3) * 3
        for m in range(sq_i, sq_i + 3):
            for n in range(sq_j, sq_j + 3):
                if data[m][n]:
                    values.discard(data[m][n])
        return values

    def recur(start_i, start_j):
        for i in range(start_i, 9):
            for j in range(start_j if i == start_i else 0, 9):
                if data[i][j]:
                    continue
                possible_vals = get_possible_v(i, j)
                for v in possible_vals:
                    data[i][j] = v
                    if recur(i, j):
                        return True
                    data[i][j] = 0
                return False
        return True

    recur(0, 0)


def sudoku_dancing_links(data):  # 3ms
    N = 9
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // 3) * 3 + (c // 3)  # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),  # row and column
            ("rn", (r, n)),  # row and number
            ("cn", (c, n)),  # column and number
            ("bn", (b, n))]  # box and number
    dl = DancingLynx(Y)
    for i, j in product(range(N), range(N)):
        if data[i][j]:
            dl.cover((i, j, data[i][j]))
    for solution in dl.solve():
        for i, j, v in solution:
            data[i][j] = v
        return


if __name__ == '__main__':
    data = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # sudoku(data)
    sudoku_dancing_links(data)
    for l in data:
        print(' '.join(map(str, l)))
