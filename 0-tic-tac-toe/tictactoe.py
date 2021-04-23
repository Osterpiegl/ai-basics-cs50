"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

BASIC_MINIMAX = False

number_of_calls_to_max_value = 0
number_of_calls_to_min_value = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for line in board:
        for element in line:
            if element == X:
                x_count += 1
            elif element == O:
                o_count += 1

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i, line in enumerate(board):
        for j, element in enumerate(line):
            if element == EMPTY:
                actions.append((i,j))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if(board[action[0]][action[1]] != EMPTY):
        raise Exception
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal
    for i in range(3):
        if (board[i][0] != EMPTY) and (board[i][0] == board[i][1]) and (board[i][1] == board[i][2]):
            if(board[i][0] == X):
                return X
            else:
                return O
        if (board[0][i] != EMPTY) and (board[0][i] == board[1][i]) and (board[1][i] == board[2][i]):
            if(board[0][i] == O):
                return O
            else:
                return X

    # Diagonals
    if (board[0][0] != EMPTY) and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if(board[0][0] == X):
            return X
        else:
            return O
    if (board[0][2] != EMPTY) and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if(board[0][2] == X):
            return X
        else:
            return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    # Draw
    for line in board:
        for element in line:
            if element == EMPTY:
                return  False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    if BASIC_MINIMAX:
        return minimax_basic(board)
    else:
        return minimax_alpha_beta(board)


def minimax_basic(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X: # Max player
        best_value = -math.inf
        optimal_action = None
        for action in actions(board):
            max = min_value(result(board, action))
            if max > best_value:
                best_value = max
                optimal_action = action
        return optimal_action
    elif player(board) == O:    # Min player
        best_value = math.inf
        optimal_action = None
        for action in actions(board):
            min = max_value(result(board, action))
            if min < best_value:
                best_value = min
                optimal_action = action
        return optimal_action

def min_value(board):
    global number_of_calls_to_min_value
    number_of_calls_to_min_value += 1

    if terminal(board):
        return utility(board)

    min_v = math.inf
    for action in actions(board):
        min_v = min(min_v, max_value(result(board, action)))
    
    return min_v

def max_value(board):
    global number_of_calls_to_max_value
    number_of_calls_to_max_value += 1

    if terminal(board):
        return utility(board)

    max_v = -math.inf
    for action in actions(board):
        max_v = max(max_v, min_value(result(board, action)))
    
    return max_v


def minimax_alpha_beta(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        best_value = -math.inf
        optimal_action = None
        for action in actions(board):
            max = min_value_alpha_beta(result(board, action), best_value)
            if max > best_value:
                best_value = max
                optimal_action = action
        return optimal_action
    elif player(board) == O:
        best_value = math.inf
        optimal_action = None
        for action in actions(board):
            min = max_value_alpha_beta(result(board, action), best_value)
            if min < best_value:
                best_value = min
                optimal_action = action
        return optimal_action

def min_value_alpha_beta(board, tmp_max):
    global number_of_calls_to_min_value
    number_of_calls_to_min_value += 1

    if terminal(board):
        return utility(board)

    min_v = math.inf
    for action in actions(board):
        if min_v < tmp_max:
            break
        min_v = min(min_v, max_value_alpha_beta(result(board, action), min_v))
    
    return min_v

def max_value_alpha_beta(board, tmp_min):
    global number_of_calls_to_max_value
    number_of_calls_to_max_value += 1

    if terminal(board):
        return utility(board)

    max_v = -math.inf
    for action in actions(board):
        if max_v > tmp_min:
            break
        max_v = max(max_v, min_value_alpha_beta(result(board, action), max_v))
    
    return max_v

def print_exec_stats():
    print("Number of max_value calls:", number_of_calls_to_max_value)
    print("Number of min_value calls:", number_of_calls_to_min_value)