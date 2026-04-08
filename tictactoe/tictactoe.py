"""
Tic Tac Toe Player
"""

import math

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
    count_x = 0
    count_o = 0

    for row in board:
        for cell in row:
            if cell == X:
                count_x += 1
            elif cell == O:
                count_o += 1

    # X starts
    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible.add((i, j))
    return possible


def result(board, action):
    i, j = action

    # Validate coordinates
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
        raise ValueError("Invalid action: out of bounds")

    # Validate emptiness
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: cell is not empty")

    # Deep-ish copy (board is 3 lists of 3 immutable values)
    new_board = [row.copy() for row in board]

    new_board[i][j] = player(board)
    return new_board


def winner(board):

    # Horizontales
    if board[0][0] == board[0][1] == board[0][2] and board[0][0] is not EMPTY:
        return board[0][0]

    if board[1][0] == board[1][1] == board[1][2] and board[1][0] is not EMPTY:
        return board[1][0]

    if board[2][0] == board[2][1] == board[2][2] and board[2][0] is not EMPTY:
        return board[2][0]

    # Verticales
    if board[0][0] == board[1][0] == board[2][0] and board[0][0] is not EMPTY:
        return board[0][0]

    if board[0][1] == board[1][1] == board[2][1] and board[0][1] is not EMPTY:
        return board[0][1]

    if board[0][2] == board[1][2] == board[2][2] and board[0][2] is not EMPTY:
        return board[0][2]

    # Diagonales
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True

def utility(board):
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Output: a tuple (i, j) or None if terminal.
    """

    # 1) Si el juego terminó, no hay movimiento posible
    if terminal(board):
        return None

    # Helpers internos: devuelven VALORES (no acciones)
    def max_value(b):
        # X quiere maximizar
        if terminal(b):
            return utility(b)

        v = -math.inf
        for action in actions(b):
            v = max(v, min_value(result(b, action)))
        return v

    def min_value(b):
        # O quiere minimizar
        if terminal(b):
            return utility(b)

        v = math.inf
        for action in actions(b):
            v = min(v, max_value(result(b, action)))
        return v

    turn = player(board)

    # 2) Si juega X: elegir la acción con mayor valor futuro
    if turn == X:
        best_action = None
        best_score = -math.inf

        for action in actions(board):
            score = min_value(result(board, action))  # porque después juega O
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    # 3) Si juega O: elegir la acción con menor valor futuro
    else:
        best_action = None
        best_score = math.inf

        for action in actions(board):
            score = max_value(result(board, action))  # porque después juega X
            if score < best_score:
                best_score = score
                best_action = action

        return best_action