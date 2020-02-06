"""
https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
"""
from collections import defaultdict


def dancing_lynx(X, Y):
    def recur():
        if not X:
            yield solution[:]
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = select(r)
                for s in recur():
                    yield s
                deselect(r, cols)
                solution.pop()

    def select(r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    solution = []
    X = {slot: set() for slot in X}
    for piece, slots in Y.items():
        for slot in slots:
            X[slot].add(piece)
    yield from recur()


if __name__ == '__main__':
    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}
    for s in dancing_lynx(X, Y):
        print(s)
