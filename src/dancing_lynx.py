"""
basic implementation source:
https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

understanding primary ans secondary constrains:
http://www.nohuddleoffense.de/2019/01/20/dancing-links-algorithm-x-and-the-n-queens-puzzle/
"""

MAX_INT = 2147483647


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
                cols = select(piece)
                yield from recur()
                deselect(piece, cols)
                solution.pop()

    def select(piece):
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

    def deselect(piece, cols):
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
            if slot in X:
                X[slot].add(piece)
    primary_mut = set(primary or X)
    yield from recur()


def dancing_lynx_mask(pieces: dict, primary_n=None):
    """
    Algorithm X of Donald Knuth (version for mask constrains format)

    example input:
    {'A': [0, 1, 0, 0, 1, 0, 0, 0],
     'B': [0, 1, 0, 0, 1, 0, 0, 0],
     'C': [0, 0, 0, 0, 1, 1, 0, 1],
     'D': [0, 0, 0, 1, 0, 1, 1, 0],
     'E': [0, 0, 1, 1, 0, 0, 1, 1],
     'F': [0, 0, 1, 0, 0, 0, 0, 1]}

    `slots` are `constrains` for short
    :param pieces: dict {piece: [slots]}; dict of pieces and its constrains mask
    :param primary_n: count of primary constrains; All are primary by default
    :return: list of solutions; solution is list of pieces
    """

    def iter_mask(mask):
        for i, v in enumerate(mask):
            if v:
                yield i

    def shortest_slot():
        result = None
        shortest = MAX_INT
        for slot in range(primary_n):
            if not X_enabled[slot]:
                continue
            pieces = X[slot]
            if len(pieces) < shortest:
                result = slot
                shortest = len(pieces)
        return result

    def select(piece):
        cols = []
        for slot in iter_mask(Y[piece]):
            for p in X[slot]:
                for s in iter_mask(Y[p]):
                    if s != slot:
                        X[s].remove(p)
            cols.append(X[slot])
            X_enabled[slot] = 0
            if slot < primary_n:
                primary_remaining[0] -= 1
        return cols

    def deselect(piece, cols):
        for slot in reversed(list(iter_mask(Y[piece]))):  # todo: is reversed needed?
            if slot < primary_n:
                primary_remaining[0] += 1
            X_enabled[slot] = 1
            X[slot] = cols.pop()  # todo:is this needed? since we don not remove cols from X
            for p in X[slot]:
                for s in iter_mask(Y[p]):
                    if s != slot:
                        X[s].add(p)

    def recur():
        if not primary_remaining[0]:
            yield solution[:]
        else:
            c = shortest_slot()
            for piece in list(X[c]):
                solution.append(piece)
                cols = select(piece)
                yield from recur()
                deselect(piece, cols)
                solution.pop()
            pass

    solution = []
    Y = pieces
    slots_n = None
    for piece, slots in Y.items():
        if slots_n:
            assert slots_n == len(slots)
        else:
            slots_n = len(slots)
    primary_n = primary_n or slots_n
    X = [set() for _ in range(slots_n)]
    for piece, slots in Y.items():
        for i, v in enumerate(slots):
            if v:
                X[i].add(piece)
    X_enabled = [1 for _ in range(slots_n)]
    primary_remaining = [primary_n]
    yield from recur()


if __name__ == '__main__':
    # `dancing_lynx` ~3 times faster then dancing_lynx_mask
    print("value approach:")
    for s in dancing_lynx({'A': [1, 4, 7],
                           'B': [1, 4],
                           'C': [4, 5, 7],
                           'D': [3, 5, 6],
                           'E': [2, 3, 6, 7],
                           'F': [2, 7]}, primary=set(range(1, 8))):
        print(s)

    print("mask approach:")
    for s in dancing_lynx_mask({'A': [1, 0, 0, 1, 0, 0, 1],
                                'B': [1, 0, 0, 1, 0, 0, 0],
                                'C': [0, 0, 0, 1, 1, 0, 1],
                                'D': [0, 0, 1, 0, 1, 1, 0],
                                'E': [0, 1, 1, 0, 0, 1, 1],
                                'F': [0, 1, 0, 0, 0, 0, 1]}, primary_n=7):
        print(s)
