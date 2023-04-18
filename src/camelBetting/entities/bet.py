from typing import Tuple


class EtapeBet:

    def __init__(self, camel: str, value: int):
        self.camel = camel
        self.value = value

    def cash_in(self, order: Tuple[str]) -> int:
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

