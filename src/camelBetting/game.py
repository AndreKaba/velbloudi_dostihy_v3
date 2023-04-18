"""Module containing the game logic - player turns, moves etc."""
from camelBetting.entities.board import Board
from camelBetting.entities.player import Player

from typing import Tuple, List, Dict, Generator


OVERALL_BET_VALUES = [8, 5, 3, 2]


class Game:
    """The Game class."""

    def __init__(self, players: List[Player]):
        self.board = Board([player.name for player in players])

        pass





