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
        DATE: 2025/00/00
        STUDENT NAME: YOUR NAME
        STUDENT ID: XXXXXXXXX
        ========================================
        """)


#
# Basic search functions: Minimax and Alpha‑Beta
#

def minimax(grid, depth, maximizingPlayer, dep=4):
    """
    TODO (Part 1): Implement recursive Minimax search for Connect Four.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
    """
    # Placeholder return to keep function structure intact
    return 0, {0}


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
    # Placeholder return to keep function structure intact
    return 0, {0}


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
    """
    TODO (Part 3): Implement a more advanced board evaluation for agent_strong.
    Currently a placeholder that returns 0.
    """
    return 0  # Placeholder


def your_function(grid, depth, maximizingPlayer, alpha, beta, dep=4):
    """
    A stronger search function that uses get_heuristic_strong() instead of get_heuristic().
    You can employ advanced features (e.g., improved move ordering, deeper lookahead).

    Return:
      (boardValue, {setOfCandidateMoves})

    Currently a placeholder returning (0, {0}).
    """
    return 0, {0}
