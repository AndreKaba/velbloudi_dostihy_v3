"""Module for the Stone class."""


class Stone:
    """The Stone class."""

    def __init__(self, player: str, positive: bool):
        """Stone constructor.

        Args:
            player: player who put the stone
            positive: whether the stone is positive or negative
        """
        self.player = player
        if positive:
            self.value = 1
        else:
            self.value = -1

    def __repr__(self):
        return f'Stone of {self.player} with value {self.value}'
