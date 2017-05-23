from collections import Counter

assignments = []


def assign_value(values, box, value, action_type):
    # type: (dict, list, str, int) -> dict

    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values

    global eliminate_counter, only_choice_counter, naked_twins_counter

    if values[box] == value:
        return values

    if action_type == 0:
        eliminate_counter += 1
    elif action_type == 1:
        only_choice_counter += 1
    elif action_type == 2:
        naked_twins_counter += 1

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(a, b):
    # type: (str, str) -> list
    """ Cross product of elements in a and elements in b."""
    return [s + t for s in a for t in b]


def grid_values(grid):
    # type: (str) -> dict
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    global boxes

    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    # type: (dict) -> None
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    global rows, cols

    width = 0
    if values:
        width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)


def eliminate(values):
    # type: (dict) -> dict

    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    global peers

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:  # for all the relevant boxes remove that digit from the available digit string
            assign_value(values, peer, values[peer].replace(digit, ''), action_type=0)
            #  values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    # type: (dict) -> dict
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    global unit_list
    for unit in unit_list:
        for digit in '123456789':
            d_places = [box for box in unit if digit in values[box]]
            if len(d_places) == 1:
                assign_value(values, d_places[0], digit, action_type=1)
                # values[d_places[0]] = digit
    return values


def naked_twins(values):
    # type: (dict) -> dict
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unit_list:
        # use counter to count the multiplicity of eligible numbers
        # if multiplicity == 2 and the length of the eligible strings == 2 then its a twin
        twins = [possible_values for possible_values, times_occurred in Counter([values[box] for box in unit]).items()
                 if times_occurred == 2 and len(possible_values) == 2]
        if len(twins) > 0:
            for t in twins:
                for u in unit:
                    if values[u] != t:  # for all boxes in the unit except the twins
                        # eliminate the first digit of twins from all unit peers
                        assign_value(values, u, values[u].replace(t[0], ''), action_type=2)
                        # eliminate the second digit of twins from all unit peers
                        assign_value(values, u, values[u].replace(t[1], ''), action_type=2)

    return values


def reduce_puzzle(values):
    # type: (dict) -> dict or bool
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked twins strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            # print("Error: Sudoku cannot be solved")
            return False
    return values


def search(values):
    # type: (dict) -> dict or bool
    """ Using depth-first search and propagation, try all possible values."""

    # First, reduce the puzzle using the previous function
    global search_counter
    search_counter += 1
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    #  n is the number of possibilities and s is the square we will split on
    #  Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    # type: (str, bool) -> dict or bool
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sudoku = grid_values(grid)
    solution = search(sudoku)

    if type(solution) == bool:
        print("The sudoku cannot be solved")
    return solution


def init(is_diagonal=True):
    global row_units, column_units, square_units, rows, cols
    all_units = row_units + column_units + square_units

    if is_diagonal:
        # for diagonal sudoku
        diagonal_1 = [rows[i] + cols[i] for i in range(9)]
        diagonal_2 = [rows[i] + cols[8 - i] for i in range(9)]
        diagonal_units = [diagonal_1, diagonal_2]
        all_units += diagonal_units  # diagonals are also regions of search

    t_units = dict((s, [u for u in all_units if s in u]) for s in boxes)
    t_peers = dict((s, set(sum(t_units[s], [])) - {s}) for s in boxes)  # all the relevant boxes for each box

    return all_units, t_units, t_peers


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

unit_list, units, peers = init(is_diagonal=True)
search_counter = 0
eliminate_counter = 0
only_choice_counter = 0
naked_twins_counter = 0

if __name__ == '__main__':
    diagonal_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diagonal_sudoku_grid))
    print('Statistics: ------------------')
    print('Elimination used: {0} times'.format(eliminate_counter))
    print('Only Choice used: {0} times'.format(only_choice_counter))
    print('Naked Twins used: {0} times'.format(naked_twins_counter))
    print('Search used: {0} times'.format(search_counter))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
