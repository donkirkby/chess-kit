from textwrap import dedent

import chess

from golf import GolfState
from golf_search import SearchManager, SearchNode
from greedy_heuristic import GreedyHeuristic


def assert_valid_solution(solution, start_state):
    state = start_state
    for move_text in solution:
        move = chess.Move.from_uci(move_text)
        legal_moves = list(state.find_moves())
        assert move in legal_moves
        state = state.move(move)
    assert state.is_solved


def test_evaluate():
    start_text = dedent("""\
        . N . N . . B .
        . B . . R . . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQ""")

    start_state = GolfState(start_text)
    parent_node = SearchNode(start_state, depth=2)

    parent_node.evaluate(GreedyHeuristic())

    children = parent_node.find_all_children()
    child = children['d8f8']

    assert child.depth == 3
    assert child.value_count == 1
    assert child.average_value == 7  # 10 - depth of 3


def test_rank_children():
    start_text = dedent("""\
        . N . N . . B .
        . B . . R . . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQ""")

    start_state = GolfState(start_text)
    parent_node = SearchNode(start_state, depth=2)
    parent_node.evaluate(GreedyHeuristic())

    moves, weights = parent_node.rank_children()

    weights_map = dict(zip(moves, weights))

    assert len(weights_map) == len(list(parent_node.find_all_children()))
    assert weights_map['a3b3'] == 1  # 0 - 3 + 4 to raise minimum to 1
    assert weights_map['d8f8'] == 11  # 10 - 3 + 4


def test_solution():
    start_text = dedent("""\
        . N . N . . B .
        . B . . . R . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQ""")
    expected_solution = ['g8g7', 'g7h6']

    start_state = GolfState(start_text)
    manager = SearchManager(start_state, GreedyHeuristic())

    manager.search(start_state, iterations=20)
    solution = manager.get_solution()

    assert solution == expected_solution


def test_solution_with_time_limit():
    start_text = dedent("""\
        . N . N . . B .
        . B . . . R . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQ""")
    expected_solution = ['g8g7', 'g7h6']

    start_state = GolfState(start_text)
    manager = SearchManager(start_state, GreedyHeuristic())

    manager.search(start_state, milliseconds=500)
    solution = manager.get_solution()

    assert solution == expected_solution


def test_long_solution():
    start_text = dedent("""\
        . . . R . . b .
        . Q . . . K . N
        . . . R . . . .
        b . . . . . n .
        N . . . . . . B
        . . . n . . k .
        . B . . q . . r
        . r . . . . . .
        chosen: bb""")

    start_state = GolfState(start_text)
    manager = SearchManager(start_state, GreedyHeuristic())
    expected_solution = 'd3b5 a5c4 g3c3 c3h8 c4e5 g8g7 g7g6 g6e5'.split()
    assert_valid_solution(expected_solution, start_state)
    assert len(expected_solution) == 8

    manager.search(start_state, iterations=600)
    solution = manager.get_solution()

    assert_valid_solution(solution, start_state)
    assert len(solution) == 10  # TODO: Get this down to 8 or fewer.


def test_repr():
    start_text = dedent("""\
        . N . N . . B .
        . B . . . R . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQ""")
    expected_repr = f'SearchNode(GolfState({start_text!r}))'

    node = SearchNode(GolfState(start_text))

    assert repr(node) == expected_repr
