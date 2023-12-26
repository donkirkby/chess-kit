from textwrap import dedent

from golf import GolfState
from golf_graph import GolfGraph


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
