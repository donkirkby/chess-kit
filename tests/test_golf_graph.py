from textwrap import dedent

from golf import GolfState
from golf_graph import GolfGraph, move_to_bytes, bytes_to_move


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
    expected_solution = ['g8g6', 'g6h6']

    start_state = GolfState(start_text)
    graph = GolfGraph()

    graph.walk(start_state)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_move_to_bytes_conversion():
    move_text = 'a3d6'
    move_bytes = move_to_bytes(move_text)
    move_text2 = bytes_to_move(move_bytes)

    assert move_text2 == move_text
