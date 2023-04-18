from camelBetting.entities.bet import EtapeBet

from typing import List, Tuple, Union
from copy import copy


CAMELS = ['yellow', 'blue', 'green', 'orange', 'white']
ETAPE_BET_VALUES = [5, 3, 2]


class Board:

    def __init__(self, player_names: List[str]):
        # init dice and etape bets
        self.camels_to_roll = []  # list of camels that have not rolled yet
        self.available_etape_bets = None  # available etape bets for each camel
        # init overall bets
        self.winning_bets = []  # places overall winner bets
        self.losing_bets = []  # places overall losing bets
        # init the field
        self.stones = {i: None for i in range(1, 17)}
        self.fields = {i: [] for i in range(1, 17)}
        self.fields[0] = [camel for camel in CAMELS]
        # init the player banks
        self.player_banks = {player_name: 0 for player_name in player_names}
        self.player_etape_bets = {player_name: [] for player_name in player_names}
        self.player_camel_cards = {player_name: [camel for camel in CAMELS] for player_name in player_names}

        self.end_etape()

    def get_camel_position(self, camel: str) -> Tuple[int, int]:
        """Return the position of a camel on the field.

        Args:
            camel: camel to get position for

        Returns:
            tuple of (field number, index in the field - higher is better)
        """
        for pos, field in self.fields.items():
            field_camels = [x for x in field]
            if camel in field_camels:
                return pos, field_camels.index(camel)
        raise ValueError('Camel not found on the field.')

    @property
    def current_order(self) -> Tuple[str]:
        positions = []
        for camel in CAMELS:
            position = self.get_camel_position(camel)
            positions.append((position[0], position[1], camel))
        return tuple([x[2] for x in sorted(positions, key=lambda x: (-x[0], -x[1]))])

    def end_etape(self):
        order = self.current_order
        self.camels_to_roll = [camel for camel in CAMELS]
        self.available_etape_bets = {camel: [EtapeBet(camel, value) for value in ETAPE_BET_VALUES] for camel in CAMELS}
        for player in self.player_banks.keys():
            for etape_bet in self.player_etape_bets[player]:
                to_cash_in = etape_bet.cash_in(order)
                print(f'Player {player} cashed in {to_cash_in} for {etape_bet}')
                self.player_banks[player] += to_cash_in
            self.player_etape_bets[player] = []

    def copy(self):
        new_board = Board(list(self.player_banks.keys()))
        new_board.camels_to_roll = copy(self.camels_to_roll)
        new_board.available_etape_bets = copy(self.available_etape_bets)
        new_board.winning_bets = copy(self.winning_bets)
        new_board.losing_bets = copy(self.losing_bets)
        new_board.stones = copy(self.stones)
        new_board.fields = copy(self.fields)
        new_board.player_banks = copy(self.player_banks)
        new_board.player_camel_cards = copy(self.player_camel_cards)
        return new_board

    def __repr__(self):
        return f'Current order: ({self.current_order})'
