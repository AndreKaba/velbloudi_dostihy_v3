from camelBetting.entities.board import Board
from camelBetting.entities.stone import Stone

from typing import Union


class Move:

    def __init__(self, board: Board, player: str):
        self.board = board
        self.player = player

    def expected_value(self) -> float:
        raise NotImplementedError()

    @property
    def available(self) -> bool:
        raise NotImplementedError()

    def _realize_move(self) -> None:
        raise NotImplementedError()

    def play(self) -> Board:
        self.board = self.board.copy()
        self._realize_move()
        return self.board


class DiceRoll(Move):

    def __init__(self, board: Board, player: str, camel: str = None, dice: int = None):
        super().__init__(board, player)
        random = camel is None or dice is None
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

    def expected_value(self) -> float:
        return 1

    def _realize_move(self) -> None:
        self.board.camels_to_roll.pop(self.board.camels_to_roll.index(self.camel))
        field, index = self.board.get_camel_position(self.camel)
        if field == 0:  # pop camel alone if camel is in the initial position
            travelling_party = [self.board.fields[field].pop(index)]
        else:  # take whole travelling party
            travelling_party, self.board.fields[field] = \
                self.board.fields[field][index:], self.board.fields[field][:index]

        new_field = field + self.dice
        if self.board.stones[new_field] is None:
            self.board.fields[new_field] += travelling_party
        else:
            stone = self.board.stones[new_field]
            print(f'{stone.player}\'s stone was stepped on by {len(travelling_party)} camels.')
            self.board.player_banks[stone.player] += len(travelling_party)
            new_field = new_field + stone.value
            if stone.value < 0:
                travelling_party = list(reversed(travelling_party))
                self.board.fields[new_field] = [*travelling_party, *self.board.fields[new_field]]
            else:
                self.board.fields[new_field] += travelling_party


class StonePut(Move):

    def __init__(self, board: Board, player: str, field_position: int, positive: bool):
        super().__init__(board, player)
        self.field_position = field_position
        self.positive = positive

    @property
    def available(self) -> bool:
        return all([
            self.board.stones[self.field_position] is None,
            self.board.stones[self.field_position + 1] is None,
            self.board.stones[self.field_position - 1] is None,
            self.field_position > 1,
            self.field_position <= 16,
        ])

    def expected_value(self) -> float:
        return 0

    def _realize_move(self) -> None:
        for i, stone_pos in self.board.stones.items():
            if stone_pos is not None and stone_pos.player == self.player:
                self.board.stones[i] = None
                break
        self.board.stones[self.field_position] = Stone(self.player, self.positive)



