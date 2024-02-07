import numpy as np
import matplotlib.pyplot as plt
from math import log2, sqrt, log, log10
from random import randrange
from statistics import median


def plot(x: np.ndarray, y: np.ndarray):
    # # Experimental data points
    # x = np.array([1, 2, 3, 4, 5])
    # y = np.array([2, 3, 4, 5, 6])

    # Calculate linear regression
    coefficients = np.polyfit(x, y, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    # Generate points for the linear approximation line
    x_line = np.linspace(min(x), max(x), 100)
    y_line = slope * x_line + intercept

    # Plot the points and linear approximation
    # plt.errorbar(x, y, yerror=0, capsize=5, fmt='o', label='Experimental Points Error Bars')
    plt.scatter(x, y, label='Experimental Points')
    plt.plot(x_line, y_line, color='red', label=f'Linear Approximation, slope={slope}')
    plt.xlabel('log10(количество игр)')
    plt.ylabel('медианный выигрыш')
    plt.title('Linear Approximation')
    plt.legend()
    plt.grid(True)
    plt.show()


def game() -> int:
    win = 1
    while randrange(2):
        win *= 2
    return win


def game_add() -> int:
    win = 0
    while randrange(2):
        win += 1
    return win


def trial(n: int, game_fn=game) -> float:
    total = 0
    for _ in range(n):
        total += game_fn()
    return total / n


def veryfy_pesudo_random():
    max = 0
    for i in range(1, 100000000):
        if not (i & (i - 1)):
            print(f'2**{int(log2(i))}:')
        x = game_add()
        if x > max:
            max = x
            print(f'\t{x}')


def trials_median(m, n) -> float:
    outcomes = []
    for _ in range(m):
        outcomes.append(trial(n))
    return median(outcomes)


def trials_median_sigma(m, n) -> tuple[float, float]:
    """
    todo: find what is the best rounding to minimize (int(sqrt(x) + A)**2 - x)
    """
    a = int(sqrt(m) + .7)
    outcomes = []
    for _ in range(a):
        outcomes.append(trials_median(a, n))
    sigma = np.std(outcomes)
    return median(outcomes), sigma  # type: ignore


"""
10 2.9
100 4.6
1000 6.298500000000001
10000 7.96
100000 9.586704999999998
1000000 11.081346
"""
DATA = {
    'xx': [10, 100, 1000, 10000, 100000, 1000000],
    'yy': [2.9, 4.6, 6.2985, 7.96, 9.586705, 11.081346],
}


def calculate():
    xx = [10, 100, 1000, 10000, int(1e5), int(1e6)]
    yy = []
    for m in xx:
        n_trials = max([1000, int(1e7) // m])
        yy.append(trials_median(n_trials, m))
        print(m, yy[-1])


def main():
    plot([log10(x) for x in DATA['xx']], DATA['yy'])


if __name__ == '__main__':
    main()
