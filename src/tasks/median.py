# https://leetcode.com/problems/median-of-two-sorted-arrays/
from random import randrange

from py_tools.seq import nth


def median(a, b):
    return 0


def my_median(a, b):
    # slow implementation; used for validation
    def merger(a, b):
        if not a:
            yield from b
            return
        if not b:
            yield from a
            return
        a = iter(a)
        b = iter(b)
        x = next(a)
        y = next(b)
        while True:
            if x > y:
                yield y
                try:
                    y = next(b)
                except StopIteration:
                    yield x
                    return
            else:
                yield x
                try:
                    x = next(a)
                except StopIteration:
                    yield y
                    return

    len_2 = (len(a) + len(b)) // 2
    return nth(merger(a, b), len_2)


if __name__ == '__main__':
    a = list(sorted(randrange(1000) for _ in range(100)))
    b = list(sorted(randrange(1000) for _ in range(55)))
    print(a, b)
    print(median(a, b))
    print(my_median(a, b))

if __name__ == '__main__':
    pass
