"""
https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
"""
from py_tools.seq import first, rest


def dancing_lynx(pieces: dict, primary: set = None):
    """
    Algorithm X of Donald Knuth
    example input:

    Y = {'A': [1, 4, 7],
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
        result = first(X)  # todo what if first is not primary?
        shortest = len(X[result])
        for slot in rest(X):
            if primary is not None and slot not in primary:
                continue
            if len(X[slot]) < shortest:
                result = slot
                shortest = len(X[result])
        return result

    def is_done():
        if primary is None:
            return not X
        return not (set(X).intersection(primary))

    def recur():
        if is_done():
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
        return cols

    def deselect(piece, cols):
        for slot in reversed(Y[piece]):
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
    for s in dancing_lynx(pieces, primary=set(range(7))):
        print(s)
