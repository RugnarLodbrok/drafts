"""
basic implementation source:
https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

understanding primary ans secondary constrains:
http://www.nohuddleoffense.de/2019/01/20/dancing-links-algorithm-x-and-the-n-queens-puzzle/
"""

MAX_INT = 2147483647


class DancingLynx:
    def __init__(self, pieces, primary=None):
        self.Y = pieces
        all_slots = set()
        for piece, slots in self.Y.items():
            all_slots.update(slots)
        self.X = {slot: set() for slot in all_slots}
        for piece, slots in self.Y.items():
            for slot in slots:
                self.X[slot].add(piece)
        self.primary = primary or set(self.X)
        self.primary_mut = set(self.primary)

    def solve(self):
        def shortest_slot():
            result = None
            shortest = MAX_INT
            for slot, pieces in self.X.items():
                if slot not in self.primary:
                    continue
                if len(pieces) < shortest:
                    result = slot
                    shortest = len(pieces)
            return result

        def recur():
            if not self.primary_mut:
                yield solution[:]
            else:
                c = shortest_slot()
                for piece in list(self.X[c]):
                    solution.append(piece)
                    cols = self.cover(piece)
                    yield from recur()
                    self.uncover(piece, cols)
                    solution.pop()
                pass

        solution = []
        yield from recur()

    def cover(self, piece):
        X = self.X
        Y = self.Y
        cols = []
        for slot in Y[piece]:
            for p in X[slot]:
                for s in Y[p]:
                    if s != slot:
                        X[s].remove(p)
            cols.append(X.pop(slot))
            if slot in self.primary:
                self.primary_mut.remove(slot)
        return cols

    def uncover(self, piece, cols):
        X = self.X
        Y = self.Y
        for slot in reversed(Y[piece]):
            if slot in self.primary:
                self.primary_mut.add(slot)
            X[slot] = cols.pop()
            for p in X[slot]:
                for s in Y[p]:
                    if s != slot:
                        X[s].add(p)


def dancing_lynx(pieces: dict, primary: set = None):
    """
    Algorithm X of Donald Knuth

    example input:
    {'A': [1, 4, 7],
     'B': [1, 4],
     'C': [4, 5, 7],
     'D': [3, 5, 6],
     'E': [2, 3, 6, 7],
     'F': [2, 7]}

    `slots` are `constrains` for short
    :param pieces: dict {piece: [slots]}; dict of pieces and its constrains
    :param primary: set of slots; search for exact cover only for this slots;
                    all slots by default
    :return: list of solutions; solution is list of pieces
    """

    def shortest_slot():
        result = None
        shortest = MAX_INT
        for slot, pieces in X.items():
            if slot not in primary:
                continue
            if len(pieces) < shortest:
                result = slot
                shortest = len(pieces)
        return result

    def recur():
        if not primary_mut:
            yield solution[:]
        else:
            c = shortest_slot()
            for piece in list(X[c]):
                solution.append(piece)
                cols = cover(piece)
                yield from recur()
                uncover(piece, cols)
                solution.pop()
            pass

    def cover(piece):
        cols = []
        for slot in Y[piece]:
            for p in X[slot]:
                for s in Y[p]:
                    if s != slot:
                        X[s].remove(p)
            cols.append(X.pop(slot))
            if slot in primary:
                primary_mut.remove(slot)
        return cols

    def uncover(piece, cols):
        for slot in reversed(Y[piece]):
            if slot in primary:
                primary_mut.add(slot)
            X[slot] = cols.pop()
            for p in X[slot]:
                for s in Y[p]:
                    if s != slot:
                        X[s].add(p)

    solution = []
    Y = pieces
    all_slots = set()
    for piece, slots in Y.items():
        all_slots.update(slots)
    X = {slot: set() for slot in all_slots}
    for piece, slots in Y.items():
        for slot in slots:
            X[slot].add(piece)
    primary = primary or set(X)
    primary_mut = set(primary)
    yield from recur()


if __name__ == '__main__':
    for s in dancing_lynx({'A': [1, 4, 7],
                           'B': [1, 4],
                           'C': [4, 5, 7],
                           'D': [3, 5, 6],
                           'E': [2, 3, 6, 7],
                           'F': [2, 7]}, primary=set(range(1, 8))):
        print(s)
