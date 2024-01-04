from textwrap import dedent

from golf import GolfState
from greedy_heuristic import GreedyHeuristic


def test_move_chosen():
    state = GolfState(dedent("""\
        . N . N . . . B
        . B . . . R . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQq"""))
    heuristic = GreedyHeuristic()
    move_text = 'g8h8'
    depth = 1
    expected_value = 19  # 20 for moving chosen piece - 1 for depth

    value = heuristic.analyse(state, move_text, depth)
    assert value == expected_value


def test_capture():
    state = GolfState(dedent("""\
        . N . N . . . .
        . B . . . R . .
        . R . . . . . B
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQq
        taking: h6
        taken: Q"""))
    heuristic = GreedyHeuristic()
    move_text = 'g6h6'
    depth = 1
    expected_value = 119  # 100 for capture + 20 for moving chosen - 1 for depth

    value = heuristic.analyse(state, move_text, depth)
    assert value == expected_value


def test():
    state = GolfState(dedent("""\
        . N . N . . R B
        . B . . . . . .
        . R . . . . . Q
        . . . . . . k .
        n . n . . b . .
        b . . . r . . .
        r . . . . . q .
        . . . . . K . .
        chosen: BQq"""))
    heuristic = GreedyHeuristic()
    move_text = 'e7g8'
    depth = 1
    expected_value = 9  # 10 for moving next to chosen piece - 1 for depth

    value = heuristic.analyse(state, move_text, depth)
    assert value == expected_value
