"""Module containing various tests for the game entities."""
from camelBetting.entities.board import Board
from camelBetting.entities.move import DiceRoll, StonePut
from camelBetting.simulation import Simulation

import cProfile


def test_board_moves():
    pl = 'a'
    init_board = Board([pl])
    move = StonePut(init_board, pl, 2, False)
    board = move.play()
    move = DiceRoll(board, pl, 'yellow', 2)
    board = move.play()
    move = DiceRoll(board, pl, 'blue', 1)
    board = move.play()
    move = DiceRoll(board, pl, 'green', 2)
    board = move.play()
    move = DiceRoll(board, pl, 'orange', 3)
    board = move.play()
    move = DiceRoll(board, pl, 'white', 1)
    board = move.play()
    assert board.etape_ended
    board.reset_etape()
    move = DiceRoll(board, pl, 'yellow', 1)
    board = move.play()

    assert board.camel_positions['yellow'] == (1, 2)
    assert board.camel_positions['orange'] == (3, 0)
    assert board.camel_positions['green'] == (1, 3)
    assert board.camel_positions['blue'] == (1, 1)
    assert board.camel_positions['white'] == (1, 0)

    print(board)


def test_simulation():
    board = Board(['a', 'b'])
    move = StonePut(board, 'a', 2, False)
    board = move.play()
    simulation = Simulation(board)
    outcomes = simulation.simulate_etape()
    assert board.player_banks['a'] == 0
    print(outcomes)


def main():
    # test_board_moves()
    # # test_simulation()
    cProfile.run('test_simulation()')


if __name__ == '__main__':
    main()
