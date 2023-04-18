"""Module containing various player type definitions."""
import random

from camelBetting.entities.move import Move, StonePut, BetOverall
from camelBetting.simulation import Simulation
from camelBetting.entities.board import Board

from typing import List, Tuple, Union


class Player:
    """Base Player class to inherit from."""

    def __init__(self, name: str):
        """Player constructor."""
        self.name = name

    def realize_move(self, moves: List[Move], board: Board) -> Move:
        """Choose a move from the list of possible moves.

        Args:
            moves: possible moves
            board: current board

        Returns:
            chosen move
        """
        raise NotImplementedError()


class BasicNpc(Player):
    """A player that chooses the highest EV value and places stones."""

    def _place_stone(self, moves: List[Move], board: Board, camel_pos: List[int]) -> Union[Move, None]:
        """Method for deciding whether to place a stone and where.

        Args:
            moves: possible moves
            board: current board
            camel_pos: positions of the camels

        Returns:
            move to place a stone or None
        """
        stones = {stone.player: i for i, stone in board.stones.items()}
        if self.name not in stones or stones[self.name] < min(camel_pos):
            stone_moves = [move for move in moves if isinstance(move, StonePut)]
            ideal_stone_moves = [move for move in stone_moves if
                                 max(camel_pos) < move.field_position < max(camel_pos) + 3]
            if len(ideal_stone_moves) > 0:
                return random.choice(ideal_stone_moves)
            inteligent_stone_moves = list(sorted(
                [move for move in stone_moves if max(camel_pos) < move.field_position],
                key=lambda x: x.field_position
            ))
            if len(inteligent_stone_moves) > 0:
                return inteligent_stone_moves[0]


class EvilNpc(BasicNpc):
    """NPC that chooses the highest EV value and places stones."""

    def __init__(
            self,
            name: str,
            threshold_for_overall_bets: int,
            game_approx_number: int,
    ):
        """Evil NPC constructor."""
        super().__init__(name)
        self.threshold_for_overall_bets = threshold_for_overall_bets
        self.game_approx_number = game_approx_number

    def realize_move(self, moves: List[Move], board: Board) -> Move:
        """Chooses to place a stone or best EV move in current situation.

        Args:
            moves: possible moves
            board: current board

        Returns:
            chosen move
        """
        camel_pos = [x[0] for x in board.camel_positions.values()]
        stone_move = self._place_stone(moves, board, camel_pos)
        if stone_move is not None:
            return stone_move

        sim = Simulation(board)
        etape_outcomes = sim.simulate_etape()
        move_evs = [(move, move.expected_value(etape_outcomes)) for move in moves
                    if not isinstance(move, BetOverall)]
        if max(camel_pos) >= self.threshold_for_overall_bets:
            game_approx = sim.approximate_game(self.game_approx_number)
            overall_evs = [(move, move.expected_value(game_approx)) for move in moves if isinstance(move, BetOverall)]
            move_evs += overall_evs

        move_evs = list(sorted(move_evs, key=lambda x: x[1], reverse=True))
        return move_evs[0][0]


class RandomNpc(BasicNpc):
    """NPC that chooses a random move apart from stone placing."""

    def __init__(self, name: str, threshold_for_overall_bets: int):
        """Random NPC constructor."""
        super().__init__(name)
        self.threshold_for_overall_bets = threshold_for_overall_bets

    def realize_move(self, moves: List[Move], board: Board) -> Move:
        """Chooses a random move apart from stone placing.

        Args:
            moves: possible moves
            board: current board

        Returns:
            chosen move
        """
        camel_pos = [x[0] for x in board.camel_positions.values()]
        stone_move = self._place_stone(moves, board, camel_pos)
        if stone_move is not None:
            return stone_move
        if max(camel_pos) > self.threshold_for_overall_bets:
            return random.choice([move for move in moves if not isinstance(move, StonePut)])
        return random.choice(
            [move for move in moves if not isinstance(move, StonePut) and not isinstance(move, BetOverall)]
        )
