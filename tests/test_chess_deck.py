# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy

import chess.svg

from chess_deck import SvgPage, SvgSymbol, SvgCard
from diagram import Diagram
from diagram_differ import DiagramDiffer
from svg_diagram import SvgDiagram

# noinspection PyUnresolvedReferences
from test_diagram import diagram_differ, session_diagram_differ


# noinspection DuplicatedCode
def test_svg_page(diagram_differ: DiagramDiffer):
    expected_svg = ("""
        <svg xmlns="http://www.w3.org/2000/svg" 
             viewBox="0 0 400 200"
             width="400" height="200">
             <rect x="100" y="50" width="200" height="100"/>
        </svg>""")
    expected_diagram = SvgDiagram(expected_svg)

    page = SvgPage(400, 200)
    page.append(ET.Element('rect',
                           {'x': '100',
                            'y': '50',
                            'width': '200',
                            'height': '100'}))

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_piece_translate(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(400, 200)
    expected_page.append(ET.Element('rect',
                                    {'x': '150',
                                     'y': '50',
                                     'width': '100',
                                     'height': '100'}))
    card_symbol = 'N'
    piece_svg = chess.svg.piece(chess.Piece.from_symbol(card_symbol))
    Diagram.register_svg()
    piece_tree = ET.XML(piece_svg)
    ns = {'': 'http://www.w3.org/2000/svg'}
    piece_group = piece_tree.find('g', ns)
    piece_group.set('transform',
                    'translate(200 100) scale(1 1) translate(-22.5 -22.5)')
    expected_page.append(piece_group)
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(400, 200)
    page.append(ET.Element('rect',
                           {'x': '150',
                            'y': '50',
                            'width': '100',
                            'height': '100'}))
    piece = SvgSymbol(card_symbol)
    piece.x = 200
    piece.y = 100
    page.append(piece.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_symbol_rotation(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(400, 200)
    card_symbol = 'N'
    expected_piece = SvgSymbol(card_symbol).to_element()
    expected_piece.set('transform',
                       'translate(200 100) scale(1 1) rotate(45) translate(-22.5 -22.5)')
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


# noinspection DuplicatedCode
def test_symbol_scale(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(400, 200)
    card_symbol = 'N'
    expected_piece = SvgSymbol(card_symbol).to_element()
    expected_piece.set('transform',
                       'translate(200 100) scale(2) translate(-22.5 -22.5)')
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


# noinspection DuplicatedCode
def test(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(170, 220)
    expected_page.append(ET.Element('rect',
                                    {'width': '170',
                                     'height': '220',
                                     'fill': '',
                                     'stroke': 'black',
                                     'stroke-width': '4'}))
    card_symbol = 'Q'
    expected_piece = SvgSymbol(card_symbol)
    expected_piece.scale = 0.75
    expected_piece.x = 22.5
    expected_piece.y = 22.5
    expected_page.append(expected_piece.to_element())
    expected_piece2 = deepcopy(expected_piece)
    expected_piece2.rotation = 180
    expected_piece2.x = 170 - expected_piece.x
    expected_piece2.y = 220 - expected_piece.y
    expected_page.append(expected_piece2.to_element())
    expected_piece3 = deepcopy(expected_piece)
    expected_piece3.x = 85
    expected_piece3.y = 110 - 45
    expected_piece3.scale = 2
    expected_page.append(expected_piece3.to_element())
    expected_piece4 = deepcopy(expected_piece3)
    expected_piece4.rotation = 180
    expected_piece4.y = 110 + 45
    expected_page.append(expected_piece4.to_element())
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(170, 220)
    card = SvgCard(card_symbol)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)
