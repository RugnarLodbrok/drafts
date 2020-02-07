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


if __name__ == '__main__':

    pieces = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7],
    }
    for s in dancing_lynx(pieces, primary=set(range(1, 8))):
        print(s)
