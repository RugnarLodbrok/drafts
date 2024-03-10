from random import shuffle


def experiment(n):
    seats = [False] * n
    tickets = list(range(n))
    shuffle(tickets)
    babka_ticket = tickets.pop(-1)
    if babka_ticket == 0:
        # seats[1] = True
        seats[0] = True
    else:
        seats[0] = True

    for ticket in tickets[:-1]:
        if not seats[ticket]:
            seats[ticket] = True
            continue
        for i, is_occupied in enumerate(seats):
            if not is_occupied:
                seats[i] = True
                break
    return seats[tickets[-1]]


def trial(m, n):
    total = 0
    for _ in range(m):
        total += experiment(n)
    return total / m


if __name__ == '__main__':
    print(trial(1000000, 10))