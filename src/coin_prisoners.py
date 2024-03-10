from random import randrange


def s1(outcome: bool) -> bool:
    return True


def s2(outcome: bool) -> bool:
    return False


def s3(outcome: bool) -> bool:
    return outcome


def s4(outcome: bool) -> bool:
    return not outcome


strategies = [s1, s2, s3, s4]


def game(s_one, s_two):
    a = randrange(2)
    guess_1 = s_one(a)
    b = randrange(2)
    guess_2 = s_two(b)
    return (guess_1 == b) or (guess_2 == a)


def trial(n: int, s_one, s_two):
    total = 0
    for _ in range(n):
        total += game(s_one, s_two)
    return total / n


if __name__ == '__main__':
    for s_one in strategies:
        for s_two in strategies:
            print(s_one.__name__, s_two.__name__, trial(10000, s_one, s_two), sep='\t')
