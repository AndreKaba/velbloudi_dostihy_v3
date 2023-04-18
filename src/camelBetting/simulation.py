import multiprocessing
import sys
import resource

from camelBetting.entities.board import Board
from camelBetting.entities.move import simulation_moves, Move
from camelBetting.tools import block_stdout, enable_stdout

from collections import defaultdict
import random
from typing import Dict, Tuple

import threading

resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
sys.setrecursionlimit(10 ** 6)


class Simulation:
    def __init__(self, init_board: Board):
        self.init_board = init_board
        self.etape_limit = None

    def simulate_etape(self) -> Dict[Tuple[str], int]:
        board = self.init_board
        outcomes = defaultdict(int)
        block_stdout()
        self._simulate_etape(board, outcomes)
        enable_stdout()
        return outcomes

    def simulate_game(self, etape_limit: int) -> Dict[Tuple[str], int]:
        self.etape_limit = self.init_board.etape + etape_limit
        board = self.init_board
        outcomes = defaultdict(int)
        block_stdout()
        self._simulate_game(board, outcomes)
        enable_stdout()
        return outcomes

    def approximate_game(self, number_of_approximations: int) -> Dict[Tuple[str], int]:
        outcomes = defaultdict(int)
        for i in range(number_of_approximations):
            board = self.init_board
            while not board.game_ended:
                possible_moves = simulation_moves(board)
                move = random.choice(possible_moves)
                board = move.play(True)
                if board.etape_ended:
                    board.reset_etape(simulation=True)
            outcomes[board.current_camel_order] += 1

        return outcomes

    def _simulate_etape(self, board: Board, outcomes: Dict[Tuple[str], int]) -> Dict[Tuple[str], int]:
        possible_moves = simulation_moves(board)

        # for move in possible_moves:
        #     thread = threading.Thread(target=self._play_move, args=(move, outcomes))
        #     thread.daemon = True
        #     thread.start()

        for move in possible_moves:
            board = move.play(True)
            if board.etape_ended:
                outcomes[board.current_camel_order] += 1
            else:
                self._simulate_etape(board, outcomes)
        return outcomes

    def _simulate_game(self, board: Board, outcomes: Dict[Tuple[str], int]) -> Dict[Tuple[str], int]:
        possible_moves = simulation_moves(board)

        for move in possible_moves:
            board = move.play(True)
            if board.etape_ended:
                board.reset_etape(simulation=True)
            if board.game_ended:
                outcomes[board.current_camel_order] += 1
            elif board.etape >= self.etape_limit:
                outcomes['?'] += 1
            else:
                self._simulate_game(board, outcomes)
        return outcomes
