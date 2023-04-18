"""Module containing various tests for the game entities."""
from camelBetting.entities.board import Board
from camelBetting.entities.move import DiceRoll, StonePut
from camelBetting.simulation import Simulation

import cProfile


def test_board_moves():
    init_board = Board(['a', 'b'])
    move = StonePut(init_board, 'a', 2, False)
    board = move.play()
    move = DiceRoll(board, 'b', 'yellow', 2)
    board = move.play()
    move = DiceRoll(board, 'a', 'blue', 1)
    board = move.play()
    move = DiceRoll(board, 'b', 'green', 2)
    board = move.play()

    assert board.player_banks['a'] == 2
    assert board.player_banks['b'] == 0
    assert board.fields[1] == ['green', 'yellow', 'blue']
    print(board)


def test_simulation():
    board = Board(['a', 'b'])
    simulation = Simulation(board)
    outcomes = simulation.simulate_etape()
    print(outcomes)


def main():
    # test_board_moves()
    # test_simulation()
    cProfile.run('test_simulation()')


if __name__ == '__main__':
    main()