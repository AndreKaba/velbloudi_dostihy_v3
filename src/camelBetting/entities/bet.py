"""Module containing the bets."""
from typing import Tuple


class EtapeBet:
    """Etape bet class."""

    def __init__(self, camel: str, value: int):
        """Etape bet constructor.

        Args:
            camel: camel to bet on
            value: how much does winning earn
        """
        self.camel = camel
        self.value = value

    def cash_in(self, order: Tuple[str]) -> int:
        """Cash in the bet.

        Args:
            order: order of the camels

        Returns:
            how much does the bet earn or cost
        """
        if self.camel == order[0]:
            return self.value
        elif self.camel == order[1]:
            return 1
        else:
            return -1

    def __repr__(self):
        return f'Etape bet on {self.camel.upper()} for {self.value}'


class OverallBet:

    def __init__(self, camel: str, player: str):
        self.camel = camel
        self.player = player

