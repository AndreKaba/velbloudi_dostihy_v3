import multiprocessing

from camelBetting.entities.board import Board
from camelBetting.entities.move import simulation_moves, Move

from collections import defaultdict
from typing import Dict, Tuple

import threading


class Simulation:
    def __init__(self, init_board: Board):
        self.init_board = init_board

    def _play_move(self, move: Move, outcomes: Dict[Tuple[str], int]):
        board = move.play()
        if board.etape_ended:
            outcomes[board.current_camel_order] += 1
        else:
            self.simulate_etape(board, outcomes)

    def simulate_etape(self, board: Board = None, outcomes: Dict[Tuple[str], int] = None) -> Dict[Tuple[str], int]:
        if board is None:
            board = self.init_board
        if outcomes is None:
            outcomes = defaultdict(int)

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
                self.simulate_etape(board, outcomes)

        return outcomes


