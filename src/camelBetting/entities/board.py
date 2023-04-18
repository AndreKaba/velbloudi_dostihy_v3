"""Module containing the definition of the Board class."""
from camelBetting.entities.bet import EtapeBet, OverallBet, overall_bet_values, ETAPE_BET_VALUES
from camelBetting.entities.stone import Stone

from typing import List, Tuple, Union, Dict
from copy import copy

CAMELS = ['yellow', 'blue', 'green', 'orange', 'white']


class Board:
    """Board class."""

    def __init__(self, player_names: List[str], simulation: bool = False):
        """Board constructor.

        Args:
            player_names: list of player names
        """
        self.etape = 0  # etape number
        self.etape_starter = -1  # player who starts the etape
        # init dice and etape bets
        self.camels_to_roll: List[str] = []  # list of camels that have not rolled yet
        self.available_etape_bets: Dict[str, List[EtapeBet]] = {}  # available etape bets for each camel
        # init overall bets
        self.winning_bets: List[OverallBet] = []  # places overall winner bets
        self.losing_bets: List[OverallBet] = []  # places overall losing bets
        # init the field
        self.stones: Dict[int, Stone] = {}
        self.camel_positions: Dict[str, Tuple[int, int]] = {camel: (0, 0) for camel in CAMELS}
        # init the player banks
        self.players = player_names
        self.player_banks: Dict[str, int] = {player_name: 0 for player_name in player_names}
        self.player_etape_bets: Dict[str, List[EtapeBet]] = {player_name: [] for player_name in player_names}
        self.player_camel_cards: Dict[str, List[str]] = \
            {player_name: [camel for camel in CAMELS] for player_name in player_names}
        self._current_player_index = -1

        self.reset_etape(simulation)

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
        if self._current_player_index >= len(self.players):
            self._current_player_index = 0

    def move_camel(self, camel: str, field: int, on_top: bool):
        """Move a camel to a field.

        Args:
            camel: camel to move
            field: field to move to
            on_top: whether to place the camel on top or bottom of the field
        """
        self._remove_camel(camel)
        self._place_camel(camel, field, on_top)

    def _remove_camel(self, camel: str):
        """Remove a camel from the field."""
        field = self.camel_positions[camel][0]
        self.camel_positions[camel] = (-1, -1)
        if field == 0:
            return
        field_camels = [(camel, f, i) for camel, (f, i) in self.camel_positions.items() if f == field]
        field_camels = sorted(field_camels, key=lambda x: x[2])
        for new_i, (camel, f, i) in enumerate(field_camels):
            self.camel_positions[camel] = (f, new_i)

    def _place_camel(self, camel: str, field: int, on_top: bool):
        """Place camel on top or bottom of field."""
        camels_on_field = [(camel, f, i) for camel, (f, i) in self.camel_positions.items() if f == field]
        if len(camels_on_field) == 0:
            self.camel_positions[camel] = (field, 0)
        if on_top:
            maxim = max([x[2] for x in camels_on_field] + [-1])
            self.camel_positions[camel] = (field, maxim + 1)
        else:
            camels_on_field.append((camel, field, -1))
            camels_on_field = sorted(camels_on_field, key=lambda x: x[2])
            for new_i, (camel, f, i) in enumerate(camels_on_field):
                self.camel_positions[camel] = (f, new_i)

    @property
    def current_camel_order(self) -> Tuple[str]:
        """Current order of the camels.

        Returns:
            tuple of camel colors in the current order
        """
        tmp = [(camel, f, i) for camel, (f, i) in self.camel_positions.items()]
        tmp = sorted(tmp, key=lambda x: (-x[1], -x[2]))
        return tuple([camel for (camel, f, i) in tmp])

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
        return any([f > 16 for camel, (f, i) in self.camel_positions.items()])

    def reset_etape(self, simulation: bool = False):
        """End the etape."""
        order = self.current_camel_order
        self.camels_to_roll = [camel for camel in CAMELS]
        if not simulation:
            self.available_etape_bets = {camel:
                                             [EtapeBet(camel, value) for value in ETAPE_BET_VALUES] for camel in CAMELS}
            for player in self.player_banks.keys():
                for etape_bet in self.player_etape_bets[player]:
                    to_cash_in = etape_bet.cash_in(order)
                    print(f'Player {player} cashed in {to_cash_in} for {etape_bet}')
                    self.player_banks[player] += to_cash_in
                self.player_etape_bets[player] = []

        self.etape += 1
        self.etape_starter += 1
        if self.etape_starter >= len(self.players):
            self.etape_starter = 0
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

    def copy(self, simulation: bool = False):
        """Get a copy of the board.

        Args:
            simulation: whether the copy is used in a simulation

        Returns:
            copy of the board
        """
        new_board = Board(list(self.player_banks.keys()), simulation)
        new_board.etape = self.etape
        new_board.etape_starter = self.etape_starter
        new_board.camels_to_roll = copy(self.camels_to_roll)
        new_board.stones = {i: copy(stone) for i, stone in self.stones.items()}
        new_board.camel_positions = copy(self.camel_positions)
        new_board._current_player_index = self._current_player_index
        if not simulation:
            new_board.available_etape_bets = copy(self.available_etape_bets)
            new_board.winning_bets = copy(self.winning_bets)
            new_board.losing_bets = copy(self.losing_bets)
            new_board.player_banks = {player_name: copy(player_bank) for player_name, player_bank
                                      in self.player_banks.items()}
            new_board.player_camel_cards = copy(self.player_camel_cards)
            new_board.player_etape_bets = {player_name: copy(player_bets) for player_name, player_bets
                                           in self.player_etape_bets.items()}
        return new_board

    def __repr__(self):
        return f'Current order: ({self.current_camel_order})'
