"""Module containing various player type definitions."""
from camelBetting.entities.move import Move

from typing import List, Tuple


class Player:
    """Base Player class to inherit from."""

    def __init__(self, name: str):
        """Player constructor."""
        self.name = name

    def realize_move(self, moves: List[Move]) -> Move:
        """Choose a move from the list of possible moves.

        Args:
            moves: possible moves

        Returns:
            chosen move
        """
        raise NotImplementedError()
