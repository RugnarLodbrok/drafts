"""
https://leetcode.com/problems/unique-paths-iii/

On a 2-dimensional grid, there are 4 types of squares:

1 represents the starting square.  There is exactly one starting square.
2 represents the ending square.  There is exactly one ending square.
0 represents empty squares we can walk over.
-1 represents obstacles that we cannot walk over.
Return the number of 4-directional walks from the starting square to the ending square, that walk over every non-obstacle square exactly once.



Example 1:

Input: [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]
Output: 2
Explanation: We have the following two paths:
1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2)
2. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2)
Example 2:

Input: [[1,0,0,0],[0,0,0,0],[0,0,0,2]]
Output: 4
Explanation: We have the following four paths:
1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2),(2,3)
2. (0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(1,3),(2,3)
3. (0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(1,1),(0,1),(0,2),(0,3),(1,3),(2,3)
4. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2),(2,3)
Example 3:

Input: [[0,1],[2,0]]
Output: 0
Explanation:
There is no path that walks over every empty square exactly once.
Note that the starting and ending square can be anywhere in the grid.


Note:

1 <= grid.length * grid[0].length <= 20

"""

START = 1
EMPTY = 0
END = 2
OBS = -1


def find_paths(grid):
    start = None
    m = len(grid)
    n = len(grid[0])
    expected_len = 2
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if v == START:
                start = (i, j)
            if v == EMPTY:
                expected_len += 1

    path = []

    def possible_steps(i, j):
        if j > 0:
            yield i, j - 1
        if j < n - 1:
            yield i, j + 1
        if i > 0:
            yield i - 1, j
        if i < m - 1:
            yield i + 1, j

    def recur(i, j):
        path.append((i, j))
        if grid[i][j] == END:
            yield path
            path.pop(-1)
            return
        grid[i][j] = OBS
        for i_new, j_new in possible_steps(i, j):
            if grid[i_new][j_new] != OBS:
                yield from recur(i_new, j_new)
        grid[i][j] = EMPTY
        path.pop(-1)

    for path in recur(*start):
        if len(path) == expected_len:
            yield path[:]


if __name__ == '__main__':
    for i in (
            [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]],
            [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]],
            [[0, 1], [2, 0]],
    ):
        for j, p in enumerate(find_paths(i)):
            print(f"{j}.\t", p)
        print("")
