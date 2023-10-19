from pathlib import Path
from textwrap import dedent

import chess.svg
import pytest
from svgwrite import Drawing

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


def test_masquerade(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        type: masquerade
        . K Q R B N combo
        K . . . . . _
        Q . O . . . QQ
        R . . . . . _
        B . . X . . _
        N . . . . . _
        """)
    text_args = dict(text_anchor='middle',
                     font_family='FredokaOne',
                     font_size=25)
    expected = Drawing(size=(300, 240))
    for i in range(7):
        expected.add(expected.line((40*i, 0), (40*i, 240), stroke='black'))
        expected.add(expected.line((0, 40*i), (300, 40*i), stroke='black'))
    expected.add(expected.line((300, 0), (300, 240), stroke='black'))

    for i, c in enumerate('KQRBN'):
        expected.add(expected.text(c, (20, 70+40*i), **text_args))
        expected.add(expected.text(c, (60+40*i, 30), **text_args))
        expected.add(expected.line((250, 72+40*i),
                                   (290, 72+40*i),
                                   stroke='black'))

    expected.add(expected.text('O', (100, 110), **text_args))
    expected.add(expected.text('X', (140, 190), **text_args))
    expected.add(expected.text('QQ', (270, 110), **text_args))

    expected.add(expected.line((0, 0), (40, 40), stroke='black'))
    text_args['font_size'] = 15
    expected.add(expected.text('combo', (270, 30), **text_args))
    text_args['font_size'] = 10
    expected.add(expected.text('mv', (15, 30), **text_args))
    expected.add(expected.text('cap', (27, 15), **text_args))

    expected_diagram = SvgDiagram(expected.tostring())

    diagram = Diagram(600, 600, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


def test_cloak(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        type: cloak
        . K Q R B N
        1 . . . . .
        2 . X . . .
        3 . . O . .
        4 . . . . .
        5 . . . . .
        6 . . . . .
        7 . . . . .
        8 . . . . .
        """)
    text_args = dict(text_anchor='middle',
                     font_family='FredokaOne',
                     font_size=19)
    expected = Drawing(size=(180, 270))
    for i in range(10):
        expected.add(expected.line((0, 30*i), (180, 30*i), stroke='black'))
    for j in range(7):
        expected.add(expected.line((30*j, 0), (30*j, 270), stroke='black'))

    for i, c in enumerate('12345678'):
        expected.add(expected.text(c, (15, 52 + 30*i), **text_args))
    for j, c in enumerate('KQRBN'):
        expected.add(expected.text(c, (45+30*j, 22), **text_args))

    expected.add(expected.text('X', (75, 82), **text_args))
    expected.add(expected.text('O', (105, 112), **text_args))

    expected_diagram = SvgDiagram(expected.tostring())

    diagram = Diagram(600, 270, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)
