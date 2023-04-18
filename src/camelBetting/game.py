from camelBetting.entities.board import Board
from camelBetting.entities.player import Player

from typing import Tuple, List, Dict, Generator


OVERALL_BET_VALUES = [8, 5, 3, 2]


class Game:

    def __init__(self, players: List[Player]):
        self.etape = 1
        self.board = Board()

        pass





