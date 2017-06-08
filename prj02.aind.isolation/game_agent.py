"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


# region heuristics
def test(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves ** 2 / (1 + opp_moves)) + float(own_moves / (1 + opp_moves ** 2))


def open_move_score(game, player):
    """

    :param isolation.Board game: 
    :param IsolationPlayer player: 
    :return: float
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


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
    scaling_factor = max_number_of_moves / own_moves if own_moves > 0 else max_number_of_moves
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


def player_distance(game, player):
    y1, x1 = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))
    return float((y1 - y2) ** 2 + (x1 - x2) ** 2)


def combined_1(game, player):
    own_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    open_move_score = len(own_moves)
    mobility = len(own_moves) - len(opponent_moves)
    same_moves = len(list(set(own_moves) & set(opponent_moves)))

    return float(0.2 * open_move_score + 0.4 * mobility + 0.4 * same_moves)


def combined_2(game, player):
    own_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    board_size = game.height * game.width
    moves_to_board = game.move_count / board_size

    if moves_to_board > 0.5:  # closer to endgame (most squares are occupied
        return float(len(own_moves) * 2 - len(opponent_moves))
    else:
        return float(len(own_moves) - len(opponent_moves) * 2)


def combined_3(game, player):
    own_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    board_size = game.height * game.width
    moves_to_board = game.move_count / board_size

    if moves_to_board >= 0.8:  # closer to endgame (most squares are occupied
        return float(len(own_moves) * 4 - len(opponent_moves))
    elif 0.4 <= moves_to_board < 0.8:
        return float(len(own_moves) * 2 - len(opponent_moves))
    else:
        return float(len(own_moves) - len(opponent_moves) * 2)


# endregion


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : IsolationPlayer
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return combined_1(game, player)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : IsolationPlayer
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return combined_2(game, player)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : IsolationPlayer
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return combined_3(game, player)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate successors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.resignation_move = (-1, -1)


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if len(legal_moves) == 0:
            return self.resignation_move
        else:
            best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            return best_move  # Handle any actions required after timeout as needed

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        _, best_move = self.do_minimax(game, depth)
        return best_move

    def do_minimax(self, game, depth, maximizing_mode=True):
        best_move = self.resignation_move
        best_score = float('-inf') if maximizing_mode else float('inf')
        min_or_max = max if maximizing_mode else min
        legal_moves = game.get_legal_moves()

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # at leaf nodes (or terminal nodes) we are just interested in the evaluation of the position
        # we are not predicting best line. Lowest recursion point
        if depth == 0 or len(legal_moves) == 0:  # end of search or terminal_node
            return self.score(game, self), best_move

        for move in legal_moves:  # active players legal moves
            score, _ = self.do_minimax(game.forecast_move(move), depth - 1, not maximizing_mode)
            best_score, best_move = min_or_max((best_score, best_move), (score, move))  # standard tuple comparison

        return best_score, best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = self.resignation_move
        search_depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                best_move = self.alphabeta(game, search_depth)
                search_depth += 1

        except SearchTimeout:
            # when timeout occurs we return the best move from the previous iteration step
            return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers
        

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        _, best_move = self.do_alpha_beta(game, depth, alpha, beta)
        return best_move

    def do_alpha_beta(self, game, depth, alpha=float("-inf"), beta=float("inf"), max_mode=True):
        best_score = alpha if max_mode else beta
        legal_moves = game.get_legal_moves()

        if len(legal_moves)==0:
            best_move = self.resignation_move
        else:
            best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # at leaf nodes (or terminal nodes) we are just interested in the evaluation of the position
        # we are not predicting best line. Lowest recursion point
        if depth == 0 or len(legal_moves) == 0:  # end of search or terminal_node
            return self.score(game, self), best_move

        for move in legal_moves:
            if max_mode:
                score, _ = self.do_alpha_beta(game.forecast_move(move), depth - 1, best_score, beta, not max_mode)
                if score > best_score:  # update best score (max)
                    best_score, best_move = score, move
                if best_score >= beta:  # the minimizer has already a better option
                    return best_score, best_move
            else:
                score, _ = self.do_alpha_beta(game.forecast_move(move), depth - 1, alpha, best_score, not max_mode)
                if score < best_score:  # update best score (min)
                    best_score, best_move = score, move
                if best_score <= alpha:  # the maximizer has already a better option
                    return best_score, best_move

        return best_score, best_move
