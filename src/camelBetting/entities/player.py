from camelBetting.entities.move import Move

from typing import List, Tuple


class Player:

    def __init__(self, name: str):
        self.name = name

    def realize_move(self, moves: List[Move]) -> Move:
        raise NotImplementedError()