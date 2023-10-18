from io import BytesIO
from pathlib import Path
from textwrap import dedent

import chess.svg
import pytest

from board_parser import parse_board
from diagram import Diagram
from diagram_differ import DiagramDiffer
from svg_diagram import SvgDiagram


@pytest.fixture(scope='session')
def session_diagram_differ():
    """ Track all images compared in a session. """
    diffs_path = Path(__file__).parent / 'image_diffs'
    differ = DiagramDiffer(diffs_path)
    yield differ
    differ.remove_common_prefix()


@pytest.fixture
def diagram_differ(request, session_diagram_differ):
    """ Pass the current request to the session image differ. """
    session_diagram_differ.request = request
    yield session_diagram_differ


def test_basic(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K Q . . .
        """)
    expected_board = parse_board(diagram_text)
    expected_svg = chess.svg.board(expected_board, size=250)
    expected_diagram = SvgDiagram(expected_svg)

    diagram = Diagram(500, 500, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


def test_arrows(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        arrow: e1, e5, white
        arrow: e5, d4, grey
        """)
    expected_text = diagram_text.split('arrow')[0]
    expected_board = parse_board(expected_text)
    expected_svg = chess.svg.board(
        expected_board,
        arrows=[chess.svg.Arrow(chess.E1, chess.E5, color='white'),
                chess.svg.Arrow(chess.E5, chess.D4, color='grey')],
        size=250)
    expected_diagram = SvgDiagram(expected_svg)

    diagram = Diagram(500, 500, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)
