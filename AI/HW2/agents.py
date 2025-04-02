import numpy as np
import random
import game

def print_INFO():
    """
    Prints your homework submission details.
    Please replace the placeholders (date, name, student ID) with valid information
    before submitting.
    """
    print(
        """========================================
        DATE: 2025/04/03
        STUDENT NAME: 蔡懷恩
        STUDENT ID: 112550020
        ========================================
        """)


#
# Basic search functions: Minimax and Alpha‑Beta
#

def minimax(grid, depth, maximizingPlayer, dep=4): # maximizingPlayer's type is bool
    """
    TODO (Part 1): Implement recursive Minimax search for Connect Four.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
    """
    # 迴圈結束條件
    if grid.terminate() or depth == 0:
        return get_heuristic(grid), {0} # 回傳{0}因為用不到

    best_value = -np.inf if maximizingPlayer else np.inf # player1 => -∞, player2 => ∞
    best_moves = set()
    valid_moves = grid.valid

    for col in valid_moves:
        next_grid = game.drop_piece(grid, col)
        val, _ = minimax(next_grid, depth - 1, not maximizingPlayer)

        if maximizingPlayer:
            if val > best_value:
                best_value = val
                best_moves = {col}
            elif val == best_value:
                best_moves.add(col)
        else:
            if val < best_value:
                best_value = val
                best_moves = {col}
            elif val == best_value:
                best_moves.add(col)

    if not best_moves:
        best_moves = set(valid_moves) if valid_moves else {0} # best_moves為空就回傳vaild_moves

    return best_value, best_moves


def alphabeta(grid, depth, maximizingPlayer, alpha, beta, dep=4):
    """
    TODO (Part 2): Implement Alpha-Beta pruning as an optimization to Minimax.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
      - Prune branches when alpha >= beta
    """
    # 迴圈結束條件
    if grid.terminate() or depth == 0:
        return get_heuristic(grid), {0} # 回傳{0}因為用不到

    best_value = -np.inf if maximizingPlayer else np.inf # player1 => -∞, player2 => ∞
    best_moves = set()
    valid_moves = grid.valid

    for col in valid_moves:
        next_grid = game.drop_piece(grid, col)
        val, _ = alphabeta(next_grid, depth - 1, not maximizingPlayer, alpha, beta)

        if maximizingPlayer:
            if val > best_value:
                best_value = val
                best_moves = {col}
            elif val == best_value:
                best_moves.add(col)
            alpha = max(alpha, val) # 目前已知「Max player 的最佳選擇」
            if beta <= alpha:
                break
        else:
            if val < best_value:
                best_value = val
                best_moves = {col}
            elif val == best_value:
                best_moves.add(col)
            beta = min(beta, val) # 目前已知「Min player 的最佳選擇」
            if beta <= alpha:
                break

    if not best_moves:
        best_moves = set(valid_moves) if valid_moves else {0} # best_moves為空就回傳vaild_moves

    return best_value, best_moves


#
# Basic agents
#

def agent_minimax(grid):
    """
    Agent that uses the minimax() function with a default search depth (e.g., 4).
    Must return a single column (integer) where the piece is dropped.
    """
    return random.choice(list(minimax(grid, 4, True)[1]))


def agent_alphabeta(grid):
    """
    Agent that uses the alphabeta() function with a default search depth (e.g., 4).
    Must return a single column (integer) where the piece is dropped.
    """
    return random.choice(list(alphabeta(grid, 4, True, -np.inf, np.inf)[1]))


def agent_reflex(grid):
    """
    A simple reflex agent provided as a baseline:
      - Checks if there's an immediate winning move.
      - Otherwise picks a random valid column.
    """
    wins = [c for c in grid.valid if game.check_winning_move(grid, c, grid.mark)]
    if wins:
        return random.choice(wins)
    return random.choice(grid.valid)


def agent_strong(grid):
    """
    TODO (Part 3): Design your own agent (depth = 4) to consistently beat the Alpha-Beta agent (depth = 4).
    This agent will typically act as Player 2.
    """
    # Placeholder logic that calls your_function().
    return random.choice(list(your_function(grid, 4, False, -np.inf, np.inf)[1]))


#
# Heuristic functions
#

def get_heuristic(board):
    """
    Evaluates the board from Player 1's perspective using a basic heuristic.

    Returns:
      - Large positive value if Player 1 is winning
      - Large negative value if Player 2 is winning
      - Intermediate scores based on partial connect patterns
    """
    num_twos       = game.count_windows(board, 2, 1)
    num_threes     = game.count_windows(board, 3, 1)
    num_twos_opp   = game.count_windows(board, 2, 2)
    num_threes_opp = game.count_windows(board, 3, 2)

    score = (
          1e10 * board.win(1)
        + 1e6  * num_threes
        + 10   * num_twos
        - 10   * num_twos_opp
        - 1e6  * num_threes_opp
        - 1e10 * board.win(2)
    )
    return score


def get_heuristic_strong(board):
    # Favor center control
    center_col = board.column // 2 #中間(3)
    center_score = 0
    for c in range(board.column):
        weight = 3 - abs(center_col - c)  # 越靠近中心，weight 越高（最大是3）
        for r in range(board.row):
            if board.table[r][c] == 1: # player 1
                center_score += weight
            if board.table[r][c] == 2: # player 2
                center_score -= weight

    num_twos       = game.count_windows(board, 2, 1)
    num_threes     = game.count_windows(board, 3, 1)
    num_twos_opp   = game.count_windows(board, 2, 2)
    num_threes_opp = game.count_windows(board, 3, 2)

    score  = 0
    score += 10   * center_score

    score += 1e10 * board.win(1)
    score += 1e6  * num_threes
    score += 100  * num_twos

    score -= 1e10 * board.win(2)
    score -= 1e6  * num_threes_opp
    score -= 100  * num_twos_opp

    return score


def your_function(grid, depth, maximizingPlayer, alpha, beta, dep=4): #複製alphabeta的
    """
    TODO (Part 3): Implement a more advanced board evaluation for agent_strong.
    """
    # 迴圈結束條件
    if grid.terminate() or depth == 0: # 回傳{0}因為用不到
        return get_heuristic_strong(grid), {0}

    best_value = -np.inf if maximizingPlayer else np.inf # player1 => -∞, player2 => ∞
    best_moves = set()
    valid_moves = grid.valid

    for col in valid_moves:
        next_grid = game.drop_piece(grid, col)
        val, _ = your_function(next_grid, depth - 1, not maximizingPlayer, alpha, beta)

        if maximizingPlayer:
            if val > best_value:
                best_value = val
                best_moves = {col}
            elif val == best_value:
                best_moves.add(col)
            alpha = max(alpha, val) # 目前已知「Max player 的最佳選擇」
            if beta <= alpha:
                break
        else:
            if val < best_value:
                best_value = val
                best_moves = {col}
            elif val == best_value:
                best_moves.add(col)
            beta = min(beta, val) # 目前已知「Min player 的最佳選擇」
            if beta <= alpha:
                break

    if not best_moves:
        best_moves = set(valid_moves) if valid_moves else {0} # best_moves為空就回傳vaild_moves

    return best_value, best_moves