from math import exp
from textwrap import dedent

import chess
from pytest import approx

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
    max_raw_value = 100 + 20 + 8*10  # Bonuses for capture, chosen, + neighbours
    assert child.average_value == exp((10-3) - max_raw_value)


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
    assert weights_map['a3b3'] == approx(exp(0 - 3 - 17))
    assert weights_map['d8f8'] == approx(exp(10 - 3 - 17))


def test_remove_child():
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
    children = parent_node.find_all_children()
    child_count_before = len(children)
    child_node = children['b7d6']

    parent_node.remove_child(child_node)

    child_count_after = len(parent_node.find_all_children())

    assert child_count_after == child_count_before - 1


def test_remove_unknown_child():
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
    children = parent_node.find_all_children()
    child_count_before = len(children)

    parent_node.remove_child(parent_node)

    child_count_after = len(parent_node.find_all_children())

    assert child_count_after == child_count_before


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

    manager.search(start_state, iterations=2000)
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

    manager.search(start_state, milliseconds=6_000)
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
    expected_solution = 'd3b5 a5c6 c6e7 g3g4 g5f6 e7g8'.split()
    assert_valid_solution(expected_solution, start_state)
    assert len(expected_solution) == 6

    manager.search(start_state, iterations=1_000)
    solution = manager.get_solution()

    assert_valid_solution(solution, start_state)
    assert len(solution) == 6


def test_multiple_search_batches():
    start_text = dedent("""\
        . . . r . . . .
        . Q . B . . . .
        . . K . n . . .
        . . q . n . . B
        . . . . . . . .
        . . N R N R . b
        . . b . . . . .
        . k . . . r . .
        chosen: kn""")

    start_state = GolfState(start_text)
    manager = SearchManager(start_state, GreedyHeuristic())

    manager.search(start_state, iterations=100)
    assert manager.best_solution_node is None
    manager.search(start_state, iterations=100)
    assert manager.best_solution_node is not None


def test_long_solution2():
    start_text = dedent("""\
        . . . . . . K r
        . . . . R . n .
        . . . . q . . B
        . . b . n . . .
        r . . . . . . .
        . . k . N . . b
        . . . . Q . . B
        . N . . . R . .
        chosen: kr""")

    start_state = GolfState(start_text)
    expected_solution = 'e5d4 c3a4'.split()
    assert_valid_solution(expected_solution, start_state)
    assert len(expected_solution) == 2
    manager = SearchManager(start_state, GreedyHeuristic())

    # TODO: Why does it take so many iterations to find a short solution?
    manager.search(start_state, iterations=100_000)
    solution = manager.get_solution()

    assert_valid_solution(solution, start_state)
    assert len(solution) == 2


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
