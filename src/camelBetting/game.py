"""Module containing the game logic - player turns, moves etc."""
from camelBetting.entities.board import Board
from camelBetting.entities.player import Player, EvilNpc, RandomNpc
from camelBetting.entities.move import possible_game_moves

from typing import Tuple, List, Dict, Generator


OVERALL_BET_VALUES = [8, 5, 3, 2]


class Game:
    """The Game class."""

    def __init__(self, players: List[Player]):
        self.board: Board = Board([player.name for player in players])
        self.players: Dict[str, Player] = {player.name: player for player in players}

    def play(self):
        """Play the game."""
        while not self.board.game_ended:
            player = self.players[self.board.current_player]
            possible_moves = possible_game_moves(self.board, player)
            move = player.choose_move(possible_moves, self.board)
            self.board = move.play()
            if self.board.etape_ended:
                self.board.reset_etape()
