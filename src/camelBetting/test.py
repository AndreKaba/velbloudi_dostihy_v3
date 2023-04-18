"""Module containing various tests for the game entities."""
from camelBetting.entities.board import Board
from camelBetting.entities.move import DiceRoll, StonePut
from camelBetting.simulation import Simulation

import time
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
    for i, camel in enumerate(board.camel_positions.keys()):
        board.camel_positions[camel] = (10, i)
    simulation = Simulation(board)
    outcomes = simulation.simulate_game(2)
    # outcomes = simulation.simulate_etape()
    assert board.player_banks['a'] == 0
    print(outcomes)
    print(sum(outcomes.values()))


def test_approximation():
    board = Board(['a', 'b'])
    for i, camel in enumerate(board.camel_positions.keys()):
        board.camel_positions[camel] = (10, i)
    simulation = Simulation(board)
    outcomes = simulation.approximate_game(5000)
    overall = sum(outcomes.values())
    winners = {camel: sum([n for outcome, n in outcomes.items() if outcome[0] == camel])/overall for camel in board.camel_positions.keys()}
    winners = tuple(sorted(winners.items(), key=lambda x: x[1], reverse=True))
    losers = {camel: sum([n for outcome, n in outcomes.items() if outcome[-1] == camel])/overall for camel in board.camel_positions.keys()}
    losers = tuple(sorted(losers.items(), key=lambda x: x[1], reverse=True))
    print(winners)
    print(losers)
    # print(winners)
    # outcomes = simulation.simulate_etape()
    # print(outcomes)
    # print(sum(outcomes.values()))



def main():
    s = time.time()
    # test_board_moves()
    # test_simulation()
    test_approximation()
    # cProfile.run('test_simulation()')
    print(time.time() - s)


if __name__ == '__main__':
    main()
