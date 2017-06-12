"""Calculating the Likelihood of superiority from the match result of 2 engines"""

import sys
import math


def erf(x):
    """
    Calculating the error function for python.
    From https://stackoverflow.com/questions/457408/is-there-an-easily-available-implementation-of-erf-for-python
    :param x: 
    :return: 
    """
    # save the sign of x
    sign = 1 if x >= 0 else -1
    x = abs(x)

    # constants
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    # A&S formula 7.1.26
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y  # erf(-x) = -erf(x)


def calculate_performance(wins_, draws_, losses_):
    # from https://chessprogramming.wikispaces.com/Match+Statistics
    games_ = wins_ + losses_ + draws_
    winning_fraction_ = (wins_ + 0.5 * draws_) / games_
    elo_difference_ = - math.log(1.0 / winning_fraction_ - 1.0) * 400.0 / math.log(10.0)
    los_ = .5 + .5 * erf((wins_ - losses_) / math.sqrt(2.0 * (wins_ + losses_)))
    return games_, winning_fraction_, elo_difference_, los_


if __name__ == "__main__":
    wins, draws, losses = 515, 0, 485

    if len(sys.argv) == 4:
        wins = sys.argv[1]
        losses = sys.argv[2]
        draws = sys.argv[3]
    elif len(sys.argv) == 1:
        pass
    else:
        print("Wrong number of arguments (wins, losses, draws)")
        exit(1)

    games, winning_fraction, elo_difference, los = calculate_performance(wins, draws, losses)
    print("Number of games: ", games)
    print("Winning fraction: ", winning_fraction)
    print("Elo difference: ", elo_difference)
    print("Likelihood of Superiority: {} %".format( los * 100))
