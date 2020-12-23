"""
Player functions
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


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
    sumX = 0
    sumO = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                sumX += 1
            if board[i][j] == O:
                sumO += 1
    if sumX == 0 and sumO == 0: 
        return X
    if sumX > sumO:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check that action is valid for board
    if action not in actions(board):
        raise Exception

    # deep copy board
    boardCopy = copy.deepcopy(board)

    # check which player's move it is
    currentPlayer = player(boardCopy)

    # update board with X or O (based on player)
    boardCopy[action[0]][action[1]] = currentPlayer

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check vertical
    for row in range(3): 
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return board[row][0]

    # Check horizontal
    for col in range(3): 
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[2][0] == board[1][1] and board[1][1] == board[0][2]: 
        return board[2][0]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board) == None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def maxValue(board, alpha, beta):
    if terminal(board):
        return (utility(board), (0,0))
    v = -math.inf
    max_action = ()

    for action in actions(board):
        curr_min = minValue(result(board, action), alpha, beta)[0]
        if curr_min > v:
            max_action = action
        v = max(v, curr_min)
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return (v, max_action)


def minValue(board, alpha, beta):
    if terminal(board):
        return (utility(board), (0,0))
    v = math.inf
    min_action = ()

    for action in actions(board):
        curr_max = maxValue(result(board, action), alpha, beta)[0]
        if curr_max < v:
            min_action = action
        v = min(v, curr_max)
        beta = min(beta, v)
        if beta <= alpha:
            break
    return (v, min_action)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X: # maximizing player
        max_move = maxValue(board, -math.inf, math.inf)[1]
        return max_move
    else: # minimizing player
        min_move = minValue(board, -math.inf, math.inf)[1]
        return min_move
