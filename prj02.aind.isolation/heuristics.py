"""Heuristics for the Isolation game"""


def mobility(game, player):
    """
    
    :param isolation.Board game: 
    :param IsolationPlayer player: 
    :return: float
    """
    own_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opponent_moves)


def mobility_scaled(game, player):
    """

    :param isolation.Board game: 
    :param IsolationPlayer player: 
    :return: float
    """
    max_number_of_moves = 8
    own_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    available_empty_squares = len(game.get_blank_spaces())
    board_size = game.height * game.width
    # scaling_factor = board_size / available_empty_squares
    scaling_factor = max_number_of_moves / own_moves
    # the less the empty squares the more important the available moves
    return float(own_moves - opponent_moves) * scaling_factor


def common_moves(game, player):
    """

    :param isolation.Board game: 
    :param IsolationPlayer player: 
    :return: float
    """
    own_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    same_moves = list(set(own_moves) & set(opponent_moves))
    return float(len(same_moves))
