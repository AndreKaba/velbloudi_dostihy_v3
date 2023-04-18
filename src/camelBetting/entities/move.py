"""Module containing the definition of various moves."""
from camelBetting.entities.board import Board, CAMELS
from camelBetting.entities.stone import Stone
from camelBetting.entities.bet import OverallBet, OVERALL_BET_VALUES


from typing import Union, Dict, Tuple, List
import random


class MoveNotAvailable(Exception):
    """Exception to raise when the move is not available."""
    pass


class NotPlayersTurn(Exception):
    pass


class Move:
    """Base Move class to inherit from."""

    def __init__(self, board: Board, player: str):
        """Move constructor.

        Args:
            board: current board
            player: player who is making the move
        """
        self.board = board
        self.player = player
        if self.board.current_player != self.player:
            raise NotPlayersTurn()

    def expected_value(self, outcomes: Dict[Tuple[str], int]) -> float:
        """Expected value of the move."""
        raise NotImplementedError()

    @property
    def available(self) -> bool:
        """Whether the move is available."""
        raise NotImplementedError()

    def _realize_move(self) -> None:
        """Realize the move."""
        raise NotImplementedError()

    def play(self, simulation: bool = False) -> Board:
        """Play the move.

        Args:
            simulation: whether the move is being played in a simulation

        Returns:
            board after the move is played
        """
        self.board = self.board.copy(simulation=simulation)
        self._realize_move()
        self.board.next_player()
        return self.board

    @property
    def shortcut(self) -> str:
        raise NotImplementedError()


class DiceRoll(Move):
    """Dice roll move."""

    def __init__(
            self, board: Board, player: str, camel: Union[str, None] = None, dice: Union[int, None] = None
    ) -> None:
        """Dice roll constructor.

        Args:
            board: the game board
            player: the player who is making the move
            camel: the camel to roll for
            dice: the number of dice to roll
        """
        super().__init__(board, player)
        self.is_random = camel is None or dice is None
        if camel is None:
            self.camel = random.choice(self.board.camels_to_roll)
        else:
            self.camel = camel
        if dice is None:
            self.dice = random.choice([1, 2, 3])
        else:
            if not 1 <= dice <= 3:
                raise ValueError(f'Invalid number of dice: {dice}')
            self.dice = dice

    @property
    def available(self) -> bool:
        return self.camel in self.board.camels_to_roll

    def expected_value(self, outcomes: Dict[Tuple[str], int]) -> float:
        return 1

    def _realize_move(self) -> None:
        if not self.available:
            raise MoveNotAvailable()
        self.board.camels_to_roll.pop(self.board.camels_to_roll.index(self.camel))
        field, index = self.board.camel_positions[self.camel]
        new_field = field + self.dice
        travelling_party = [(self.camel, field, index)]
        if field != 0:
            for camel in CAMELS:
                if camel == self.camel:
                    continue
                f, i = self.board.camel_positions[camel]
                if field == f and i > index:
                    travelling_party.append((camel, f, i))
            travelling_party.sort(key=lambda x: x[2])

        if new_field not in self.board.stones:
            on_top = True
        else:
            stone = self.board.stones[new_field]
            print(f'{stone.player}\'s stone was stepped on by {len(travelling_party)} camels.')
            self.board.player_banks[stone.player] += len(travelling_party)
            new_field = new_field + stone.value
            if stone.value < 0:
                on_top = False
            else:
                on_top = True

        for camel, _, _ in travelling_party:
            self.board.move_camel(camel, new_field, on_top)

    def __repr__(self):
        return f'{self.player} rolled {self.dice} for {self.camel.upper()}'

    @property
    def shortcut(self) -> str:
        if self.is_random:
            return 'r'
        return f'r{self.camel.lower()[0]}{self.dice}'


class StonePut(Move):
    """Stone put move."""

    def __init__(self, board: Board, player: str, field_position: int, positive: bool):
        """Stone put move constructor.

        Args:
            board: the game board
            player: the player who is making the move
            field_position: the position of the field to put the stone on
            positive: whether the stone is positive or negative
        """
        super().__init__(board, player)
        self.field_position = field_position
        self.positive = positive

    @property
    def available(self) -> bool:
        return not any([
            self.board.stones.get(self.field_position) is not None,
            self.board.stones.get(self.field_position + 1) is not None,
            self.board.stones.get(self.field_position - 1) is not None,
            self.field_position <= 1,
            self.field_position > 16
        ])

    def expected_value(self, outcomes: Dict[Tuple[str], int]) -> float:
        return 0

    def _realize_move(self) -> None:
        if not self.available:
            raise MoveNotAvailable()
        for i, stone_pos in self.board.stones.items():
            if stone_pos is not None and stone_pos.player == self.player:
                self.board.stones.pop(i)
                break
        self.board.stones[self.field_position] = Stone(self.player, self.positive)

    def __repr__(self):
        return f'{self.player} put stone on field {self.field_position} with value {"+1" if self.positive else "-1"}'

    @property
    def shortcut(self) -> str:
        return f's{"p" if self.positive else "m"}{self.field_position}'


class BetEtapeWinner(Move):

    def __init__(self, board: Board, player: str, camel: str):
        super().__init__(board, player)
        self.camel = camel
        if self.available:
            self.value = self.board.available_etape_bets[self.camel][0].value
        else:
            self.value = 0

    @property
    def available(self) -> bool:
        return len(self.board.available_etape_bets[self.camel]) > 0

    def expected_value(self, outcomes: Dict[Tuple[str], int]) -> float:
        if not self.available:
            raise MoveNotAvailable()
        overall = sum([value for value in outcomes.values()])
        first = sum([value for outcome, value in outcomes.items() if outcome[0] == self.camel])
        second = sum([value for outcome, value in outcomes.items() if outcome[1] == self.camel])

        return (first * self.value + second) / overall

    def __repr__(self):
        return f'{self.player} bet on etape winner {self.camel.upper()} for {self.value}.'

    def _realize_move(self) -> None:
        if not self.available:
            raise MoveNotAvailable()
        bet = self.board.available_etape_bets[self.camel].pop(0)
        self.board.player_etape_bets[self.player].append(bet)

    @property
    def shortcut(self) -> str:
        return f'e{self.camel.lower()[0]}'


class BetOverall(Move):

    def __init__(self, board: Board, player: str, camel: str, winner: bool):
        super().__init__(board, player)
        self.camel = camel
        self.winner = winner

    @property
    def available(self) -> bool:
        return self.camel in self.board.player_camel_cards[self.player]

    def expected_value(self, outcomes: Dict[Tuple[str], int]) -> float:
        return self._min_expected_value(outcomes)

    def _min_expected_value(self, outcomes: Dict[Tuple[str], int]) -> float:
        """Minimal expected value for the move based on how many blind bets were placed on winner/loser."""
        if self.winner:
            bets_placed = len(self.board.winning_bets)
            place = 0
        else:
            bets_placed = len(self.board.losing_bets)
            place = -1
        if bets_placed > len(OVERALL_BET_VALUES):
            minimal_value = 1
        else:
            minimal_value = OVERALL_BET_VALUES[bets_placed]

        overall = sum(outcomes.values())
        placed = sum([value for outcome, value in outcomes.items() if outcome[place] == self.camel])
        return (placed * minimal_value - (overall - placed) * 1) / overall

    def _realize_move(self) -> None:
        if not self.available:
            raise MoveNotAvailable()
        self.board.player_camel_cards[self.camel].pop(self.board.player_camel_cards[self.player].index(self.camel))
        bet = OverallBet(self.camel, self.player)
        if self.winner:
            self.board.winning_bets.append(bet)
        else:
            self.board.losing_bets.append(bet)

    def __repr__(self):
        if self.winner:
            return f'{self.player} bet on overall winner.'
        else:
            return f'{self.player} bet on overall loser.'

    @property
    def shortcut(self) -> str:
        return f'o{self.camel.lower()[0]}{"w" if self.winner else "l"}'


def simulation_moves(board: Board) -> List[Move]:
    moves = []
    player = board.current_player
    for camel in board.camels_to_roll:
        for i in [1, 2, 3]:
            moves.append(DiceRoll(board, player, camel, i))

    return moves

