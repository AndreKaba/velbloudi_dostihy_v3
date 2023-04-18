from typing import List

from camelBetting.entities.board import Board, CAMELS
from camelBetting.entities.move import Move, DiceRoll, StonePut, BetEtapeWinner, BetOverall


def simulation_moves(board: Board) -> List[Move]:
    """Get moves for simulation.

    Args:
        board: current board

    Returns:
        list of moves
    """
    moves = []
    player = board.current_player
    for camel in board.camels_to_roll:
        for i in [1, 2, 3]:
            moves.append(DiceRoll(board, player, camel, i))

    return moves


def possible_game_moves(board: Board, player: str) -> List[Move]:
    """Get all moves.

    Args:
        board: current board
        player: current player name

    Returns:
        list of moves
    """
    moves = [DiceRoll(board, player)]
    for field_position in range(2, 17):
        for positive in [True, False]:
            moves.append(StonePut(board, player, field_position, positive))
    for camel in CAMELS:
        moves.append(BetEtapeWinner(board, player, camel))
        moves.append(BetOverall(board, player, camel, True))
        moves.append(BetOverall(board, player, camel, False))

    return [move for move in moves if move.available]