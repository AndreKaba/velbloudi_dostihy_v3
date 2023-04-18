"""Module containing the definition of the Board class."""
from camelBetting.entities.bet import EtapeBet, OverallBet, overall_bet_values, ETAPE_BET_VALUES
from camelBetting.entities.stone import Stone

from typing import List, Tuple, Union, Dict
from copy import copy


CAMELS = ['yellow', 'blue', 'green', 'orange', 'white']


class Board:
    """Board class."""

    def __init__(self, player_names: List[str]):
        """Board constructor.

        Args:
            player_names: list of player names
        """
        self.etape = 0  # etape number
        self.etape_starter = 0  # player who starts the etape
        # init dice and etape bets
        self.camels_to_roll: List[str] = []  # list of camels that have not rolled yet
        self.available_etape_bets: Dict[str, List[EtapeBet]] = {}  # available etape bets for each camel
        # init overall bets
        self.winning_bets: List[OverallBet] = []  # places overall winner bets
        self.losing_bets: List[OverallBet] = []  # places overall losing bets
        # init the field
        self.stones: Dict[int, Union[None, Stone]] = {i: None for i in range(1, 17)}
        self.fields: Dict[int, List[str]] = {i: [] for i in range(1, 20)}
        self.fields[0] = [camel for camel in CAMELS]
        # init the player banks
        self.players = player_names
        self.player_banks: Dict[str, int] = {player_name: 0 for player_name in player_names}
        self.player_etape_bets: Dict[str, List[EtapeBet]] = {player_name: [] for player_name in player_names}
        self.player_camel_cards: Dict[str, List[str]] = \
            {player_name: [camel for camel in CAMELS] for player_name in player_names}
        self._current_player_index = 0

        self.reset_etape()

    @property
    def current_player(self) -> str:
        """Get the players whose turn it is.

        Returns:
            name of the current player
        """
        return self.players[self._current_player_index]

    def next_player(self) -> None:
        """Move to the next player."""
        self._current_player_index += 1
        self._current_player_index %= len(self.players)

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
    def current_camel_order(self) -> Tuple[str]:
        """Current order of the camels.

        Returns:
            tuple of camel colors in the current order
        """
        positions = []
        for camel in CAMELS:
            position = self.get_camel_position(camel)
            positions.append((position[0], position[1], camel))
        return tuple([x[2] for x in sorted(positions, key=lambda x: (-x[0], -x[1]))])

    @property
    def current_player_order(self) -> Tuple[Tuple[str, int]]:
        """Current order of the players.

        Returns:
            tuple of player names in the current order
        """
        players = [(player_name, player_bank) for player_name, player_bank in self.player_banks.items()]
        players = tuple(sorted(players, key=lambda x: x[1], reverse=True))
        return players

    @property
    def etape_ended(self) -> bool:
        """Whether the etape has ended."""
        return len(self.camels_to_roll) == 0 or self.game_ended

    @property
    def game_ended(self) -> bool:
        """Whether the game has ended."""
        return any([len(field) > 0 for i, field in self.fields.items() if i > 16])

    def reset_etape(self):
        """End the etape."""
        order = self.current_camel_order
        self.camels_to_roll = [camel for camel in CAMELS]
        self.available_etape_bets = {camel: [EtapeBet(camel, value) for value in ETAPE_BET_VALUES] for camel in CAMELS}
        for player in self.player_banks.keys():
            for etape_bet in self.player_etape_bets[player]:
                to_cash_in = etape_bet.cash_in(order)
                print(f'Player {player} cashed in {to_cash_in} for {etape_bet}')
                self.player_banks[player] += to_cash_in
            self.player_etape_bets[player] = []

        self.etape += 1
        self.etape_starter += 1
        self.etape_starter %= len(self.players)
        self._current_player_index = self.etape_starter

    def cash_is_overalls(self):
        """Cash in the overall bets."""
        order = self.current_camel_order
        bet_queues = [self.losing_bets, self.winning_bets]
        for bet_queue in bet_queues:
            for bet in bet_queue:
                bet_values = overall_bet_values()
                if bet.camel == order[0]:
                    value = next(bet_values)
                    print(f'Player {bet.player} won {value} for {bet}')
                    self.player_banks[bet.player] += value
                else:
                    print(f'Player {bet.player} lost {bet} (-1)')
                    self.player_banks[bet.player] += -1

    def copy(self):
        """Get a copy of the board.

        Returns:
            copy of the board
        """
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
        return f'Current order: ({self.current_camel_order})'
