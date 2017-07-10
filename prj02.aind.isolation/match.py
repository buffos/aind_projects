"""
Play a match between player A and player B
"""

import random
from isolation import Board
from collections import namedtuple

TIME_LIMIT = 150

Agent = namedtuple("Agent", ["player", "name"])

# TODO: 1. change player.get_move() to return pv.line , depth, score time
# TODO: 2. change back minimax and alpha beta to their original form.
# TODO: 3. provide better feedback from get_move() . think....
# TODO: 4. write quiescence search


def play_game(agent_1, agent_2):
    game = Board(agent_1, agent_2)
    # initialise with random move
    move = random.choice(game.get_legal_moves())
    game.apply_move(move)
