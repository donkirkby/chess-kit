from pathlib import Path
from textwrap import dedent
import xml.etree.ElementTree as ET  # noqa

import chess.svg
import numpy as np
import pytest
from svgwrite import Drawing

from board_parser import parse_board
from chess_deck import SvgCardBack, SvgSymbol, SvgCard
from diagram import Diagram, SUIT_PATHS
from svg_page import SvgPage
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


def test_margin_arrows(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        arrow: e0, d1, grey
        margins: 0, 0, 0, 1
        """)
    expected_text = diagram_text.split('arrow')[0]
    expected_board = parse_board(expected_text)
    expected_svg = chess.svg.board(
        expected_board,
        arrows=[chess.svg.Arrow(-4, 3, color='grey')],
        size=250)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_svg)
    expected_tree.set('width', '250')
    expected_tree.set('height', '278')
    expected_tree.set('viewBox', '0 0 390 433.68')
    expected_diagram = SvgDiagram(ET.tostring(expected_tree,
                                              encoding='unicode'))

    diagram = Diagram(500, 500, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_text(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        text: A2, 1, 2
        text: G3, 7, 3
        """)
    text_args = dict(text_anchor='middle',
                     font_family='Raleway',
                     font_size=25)
    expected_text = diagram_text.split('text')[0]
    expected_board = parse_board(expected_text)
    expected_board_svg = chess.svg.board(
        expected_board,
        size=195)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_board_svg)
    extra = Drawing(size=(300, 240))
    extra.add(extra.text('A2', (37.5, 320), **text_args))
    extra.add(extra.text('G3', (307.5, 275), **text_args))
    expected_tree.extend(extra.get_xml())
    expected_diagram = SvgDiagram(ET.tostring(expected_tree,
                                              encoding='unicode'))
    ET.register_namespace('', '')  # Force registration again.

    diagram = Diagram(390, 195, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_corner_text(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        corner text: X, 4, 1
        arrow: d1, d1, gray
        """)
    text_args = dict(text_anchor='middle',
                     font_family='Raleway',
                     font_size=17)
    expected_text = diagram_text.split('corner')[0]
    expected_board = parse_board(expected_text)
    expected_board_svg = chess.svg.board(
        expected_board,
        arrows=(chess.svg.Arrow(chess.D1, chess.D1, color='gray'),),
        size=195)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_board_svg)
    extra = Drawing(size=(300, 240))
    extra.add(extra.text('X', (157, 345), **text_args))
    expected_tree.extend(extra.get_xml())
    expected_diagram = SvgDiagram(ET.tostring(expected_tree,
                                              encoding='unicode'))
    ET.register_namespace('', '')  # Force registration again.

    diagram = Diagram(390, 195, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . Q . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . p . .
        . . . . . . . .
        . . . . . . . .
        card: Q, 0, 0
        card: back, 6, 5
        """)
    expected_text = diagram_text.split('card')[0]
    expected_board = parse_board(expected_text)
    expected_board_svg = chess.svg.board(
        expected_board,
        size=195)
    page = SvgPage(195, 195)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_board_svg)
    page.append(expected_tree)
    queen_card = SvgCard('Q', has_border=False, has_outline=True)
    queen_card.x = 8
    queen_card.y = 8
    queen_card.scale = 0.25
    page.append(queen_card.to_element())
    card_back = SvgCardBack(has_outline=True)
    card_back.x = 143
    card_back.y = 120.5
    card_back.scale = 0.295
    page.append(card_back.to_element())
    expected_diagram = SvgDiagram(page.to_svg())

    diagram = Diagram(390, 195, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_margins(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        margins: 2, 1
        text: A2, 1, 2
        text: G3, 7, 3
        """)
    text_args = dict(text_anchor='middle',
                     font_family='Raleway',
                     font_size=25)
    expected_text = diagram_text.split('margins')[0]
    expected_board = parse_board(expected_text)
    expected_board_svg = chess.svg.board(
        expected_board,
        size=195)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_board_svg)
    expected_tree.set('width', '285')
    expected_tree.set('height', '240')
    expected_tree.set('viewBox', '-90 -45 570 480')
    extra = Drawing(size=(300, 240))
    extra.add(extra.text('A2', (37.5, 320), **text_args))
    extra.add(extra.text('G3', (307.5, 275), **text_args))
    expected_tree.extend(extra.get_xml())
    expected_diagram = SvgDiagram(ET.tostring(expected_tree,
                                              encoding='unicode'))

    diagram = Diagram(570, 240, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_different_margins(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        margins: 0, 2, 4, 0
        text: A2, 1, 2
        text: G3, 7, 3
        """)
    text_args = dict(text_anchor='middle',
                     font_family='Raleway',
                     font_size=25)
    expected_text = diagram_text.split('margins')[0]
    expected_board = parse_board(expected_text)
    expected_board_svg = chess.svg.board(
        expected_board,
        size=195)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_board_svg)
    expected_tree.set('width', '285')
    expected_tree.set('height', '240')
    expected_tree.set('viewBox', '0 -90 570 480')
    extra = Drawing(size=(300, 240))
    extra.add(extra.text('A2', (37.5, 320), **text_args))
    extra.add(extra.text('G3', (307.5, 275), **text_args))
    expected_tree.extend(extra.get_xml())
    expected_diagram = SvgDiagram(ET.tostring(expected_tree,
                                              encoding='unicode'))

    diagram = Diagram(570, 240, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_rect(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        rect: 2, 6, 5, 7
        """)
    expected_text = diagram_text.split('rect')[0]
    expected_board = parse_board(expected_text)
    expected_board_svg = chess.svg.board(
        expected_board,
        size=195)
    SvgPage.register_svg()
    expected_tree = ET.fromstring(expected_board_svg)
    extra = Drawing(size=(300, 240))
    extra.add(extra.rect((60, 60),
                         (180, 90),
                         fill_opacity=0,
                         stroke='blue',
                         stroke_dasharray='7.5',
                         stroke_width=5))
    expected_tree.extend(extra.get_xml())
    expected_diagram = SvgDiagram(ET.tostring(expected_tree,
                                              encoding='unicode'))

    diagram = Diagram(390, 195, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_unknown(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        . . . k q . . .
        . . . . . . . .
        . . . . . . . .
        . . . . Q . . .
        . . . P . . . .
        . . . . . . . .
        . . . . . . . .
        . . . K . . . .
        bogus: What is this?
        """)

    diagram = Diagram(570, 240, diagram_text)
    with pytest.raises(ValueError, match=r'Unknown diagram command: bogus'):
        diagram.build()


# noinspection DuplicatedCode
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


def test_cards(diagram_differ: DiagramDiffer):
    diagram_text = dedent("""\
        type: cards
        Piece Cards Gap
        P 2H 2D 3H 3D _
        r _ 10S 10C _ 2
        """)
    expected_page = SvgPage(480, 240)
    card_args = dict(text_anchor='end', font_size=50, font_family='FredokaOne')
    title_args = dict(text_anchor='middle', font_size=34, font_family='FredokaOne')

    expected = Drawing(size=(expected_page.width, expected_page.height))
    for i in range(4):
        expected.add(expected.line((0, 80*i), (480, 80*i), stroke='black'))
    for x in [0, 80, 400, 480]:
        expected.add(expected.line((x, 0), (x, 240), stroke='black'))

    expected.add(expected.text('Gap', (440, 60), **title_args))
    expected.add(expected.text('Cards', (240, 60), **title_args))

    title_args['font_size'] = 50
    for x, y, rank, suit in [(80, 140, '2', 'h'),
                             (160, 140, '2', 'd'),
                             (240, 140, '3', 'h'),
                             (320, 140, '3', 'd'),
                             (160, 220, '10', 's'),
                             (240, 220, '10', 'c')]:
        expected.add(expected.text(rank, (x + 43, y), **card_args))
        heart_path = SUIT_PATHS[suit]
        path = expected.path(heart_path)
        if suit in 'hd':
            path.fill('none')
            path.stroke('black', '2px')
        path.translate(x + 45, y - 36)
        path.scale(1.5)
        expected.add(path)
    expected.add(expected.text('2', (440, 220), **title_args))
    expected_page.append(expected.get_xml())
    pawn = SvgSymbol('P')
    pawn.x = 40
    pawn.y = 121
    pawn.scale = 1.1
    expected_page.append(pawn.to_element())
    rook = SvgSymbol('r')
    rook.x = 40
    rook.y = 201
    rook.scale = 1.1
    expected_page.append(rook.to_element())

    expected_diagram = SvgDiagram(expected_page.to_svg())

    diagram = Diagram(960, 270, diagram_text)
    svg_diagram = diagram.build()

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


def test_symbol_rotation(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(400, 200)
    card_symbol = 'N'
    expected_piece = SvgSymbol(card_symbol).to_element()
    expected_piece.set('transform',
                       'translate(200 100) scale(1 1) rotate(45)')
    expected_page.append(expected_piece)
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(400, 200)
    piece = SvgSymbol(card_symbol)
    piece.x = 200
    piece.y = 100
    piece.rotation = 45
    page.append(piece.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


def test_symbol_scale(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(400, 200)
    card_symbol = 'N'
    expected_piece = SvgSymbol(card_symbol).to_element()
    expected_piece.set('transform',
                       'translate(200 100) scale(2)')
    expected_page.append(expected_piece)
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(400, 200)
    piece = SvgSymbol(card_symbol)
    piece.x = 200
    piece.y = 100
    piece.scale = 2
    page.append(piece.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


def test_symbol_white_checker(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(133, 171)
    expected_page.append(ET.Element('circle',
                                    {'cx': '65',
                                     'cy': '85',
                                     'r': '34',
                                     'fill': 'transparent',
                                     'stroke': 'black',
                                     'stroke-width': '3'}))
    expected_page.append(ET.Element('circle',
                                    {'cx': '65',
                                     'cy': '85',
                                     'r': '24',
                                     'fill': 'transparent',
                                     'stroke': 'black',
                                     'stroke-width': '3'}))
    z0 = 65 + 85j
    r1 = 27
    r2 = 31
    ridge_count = 48
    for i in range(ridge_count):
        theta = i / ridge_count * 2 * np.pi
        z1 = r1 * np.exp(1j * theta) + z0
        z2 = r2 * np.exp(1j * theta) + z0
        expected_page.append(ET.Element('line',
                                        {'x1': str(np.real(z1)),
                                         'y1': str(np.imag(z1)),
                                         'x2': str(np.real(z2)),
                                         'y2': str(np.imag(z2)),
                                         'stroke': 'black',
                                         'stroke-width': '2'}))
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(133, 171)
    piece = SvgSymbol('C')
    piece.x = 65
    piece.y = 85
    piece.scale = 2
    page.append(piece.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_symbol_black_checker(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(133, 171)
    expected_page.append(ET.Element('circle',
                                    {'cx': '65',
                                     'cy': '85',
                                     'r': '34',
                                     'fill': 'black',
                                     'stroke': 'black',
                                     'stroke-width': '3'}))
    expected_page.append(ET.Element('circle',
                                    {'cx': '65',
                                     'cy': '85',
                                     'r': '24',
                                     'fill': 'transparent',
                                     'stroke': 'white',
                                     'stroke-width': '3'}))
    z0 = 65 + 85j
    r1 = 27
    r2 = 34
    ridge_count = 48
    for i in range(ridge_count):
        theta = i / ridge_count * 2 * np.pi
        z1 = r1 * np.exp(1j * theta) + z0
        z2 = r2 * np.exp(1j * theta) + z0
        expected_page.append(ET.Element('line',
                                        {'x1': str(np.real(z1)),
                                         'y1': str(np.imag(z1)),
                                         'x2': str(np.real(z2)),
                                         'y2': str(np.imag(z2)),
                                         'stroke': 'white',
                                         'stroke-width': '2'}))
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(133, 171)
    piece = SvgSymbol('c')
    piece.x = 65
    piece.y = 85
    piece.scale = 2
    page.append(piece.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)
