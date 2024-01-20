# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy

import chess.svg

from chess_deck import SvgPage, SvgSymbol, SvgCard, SvgGrid, SvgPips
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
def test_pips(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(90, 90)
    expected_page.append(ET.Element('rect',
                                    {'fill': 'cornsilk',
                                     'width': '45',
                                     'height': '45'}))
    expected_page.append(ET.Element('circle',
                                    {'fill': 'black',
                                     'cx': '22.5',
                                     'cy': '22.5',
                                     'r': '3'}))
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(90, 90)
    page.append(ET.Element('rect',
                           {'fill': 'cornsilk',
                            'width': '45',
                            'height': '45'}))
    pips = SvgPips(1)
    pips.x = 22.5
    pips.y = 22.5
    page.append(pips.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_pips_transform(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(190, 190)
    expected_page.append(ET.Element('rect',
                                    {'fill': 'cornsilk',
                                     'x': '100',
                                     'y': '100',
                                     'width': '90',
                                     'height': '90'}))
    expected_page.append(ET.Element('circle',
                                    {'fill': 'black',
                                     'cx': '125',
                                     'cy': '125',
                                     'r': '6'}))
    expected_page.append(ET.Element('circle',
                                    {'fill': 'black',
                                     'cx': '165',
                                     'cy': '165',
                                     'r': '6'}))
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(190, 190)
    page.append(ET.Element('rect',
                           {'fill': 'cornsilk',
                            'x': '100',
                            'y': '100',
                            'width': '90',
                            'height': '90'}))
    pips = SvgPips(2)
    pips.x = 145
    pips.y = 145
    pips.scale = 2
    page.append(pips.to_element())

    svg_diagram = SvgDiagram(page.to_svg())
    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_page.append(ET.Element('rect',
                                    {'width': '171',
                                     'height': '266',
                                     'fill': 'white',
                                     'stroke': 'black',
                                     'stroke-width': '4'}))
    expected_pips = SvgPips(5)
    expected_pips.x = 85.5
    expected_pips.y = 133
    expected_pips.scale = 0.75
    expected_page.append(expected_pips.to_element())
    card_symbol = 'Q'
    expected_piece = SvgSymbol(card_symbol)
    expected_piece.scale = 0.75
    expected_piece.x = 22.5
    expected_piece.y = 22.5
    expected_page.append(expected_piece.to_element())
    expected_piece2 = deepcopy(expected_piece)
    expected_piece2.rotation = 180
    expected_piece2.x = 171 - expected_piece.x
    expected_piece2.y = 266 - expected_piece.y
    expected_page.append(expected_piece2.to_element())
    expected_piece3 = deepcopy(expected_piece)
    expected_piece3.x = 85.5
    expected_piece3.y = 133 - 45
    expected_piece3.scale = 1.75
    expected_page.append(expected_piece3.to_element())
    expected_piece4 = deepcopy(expected_piece3)
    expected_piece4.rotation = 180
    expected_piece4.y = 133 + 45
    expected_page.append(expected_piece4.to_element())
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(171, 266)
    card = SvgCard(card_symbol)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card_transform(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_card1 = SvgCard('Q').to_element()
    expected_card1.set('transform', 'translate(133 0) scale(0.5) rotate(90)')
    expected_page.append(expected_card1)
    expected_card2 = SvgCard('N').to_element()
    expected_card2.set('transform', 'translate(85.5 133) scale(0.5)')
    expected_page.append(expected_card2)
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(171, 266)
    card1 = SvgCard('Q')
    card1.scale = 0.5
    card1.rotation = 90
    card1.x = 133
    page.append(card1.to_element())
    card2 = SvgCard('N')
    card2.scale = 0.5
    card2.x = 85.5
    card2.y = 133
    page.append(card2.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_grid(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(260, 266)
    expected_page.append(ET.Element('rect',
                                    {'width': '260',
                                     'height': '266',
                                     'fill': 'ivory'}))
    expected_card1 = SvgCard('P')
    expected_card1.scale = 0.5
    expected_page.append(expected_card1.to_element())
    expected_card2 = SvgCard('N')
    expected_card2.scale = 0.5
    expected_card2.x = 85.5
    expected_page.append(expected_card2.to_element())
    expected_card3 = SvgCard('B')
    expected_card3.scale = 0.5
    expected_card3.x = 171
    expected_page.append(expected_card3.to_element())
    expected_card4 = SvgCard('R')
    expected_card4.scale = 0.5
    expected_card4.y = 133
    expected_page.append(expected_card4.to_element())
    expected_card5 = SvgCard('Q')
    expected_card5.scale = 0.5
    expected_card5.x = 85.5
    expected_card5.y = 133
    expected_page.append(expected_card5.to_element())
    expected_card6 = SvgCard('K')
    expected_card6.scale = 0.5
    expected_card6.x = 171
    expected_card6.y = 133
    expected_page.append(expected_card6.to_element())
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(260, 266)
    page.append(ET.Element('rect',
                           {'width': '260',
                            'height': '266',
                            'fill': 'ivory'}))
    grid = SvgGrid(['PNB', 'RQK'])
    grid.scale = 266 / grid.base_height
    page.append(grid.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_grid_transform(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(133, 171)
    expected_page.append(ET.Element('rect',
                                    {'width': '260',
                                     'height': '266',
                                     'fill': 'ivory'}))
    expected_card1 = SvgCard('P')
    expected_card1.scale = 0.5
    expected_card1.rotation = 90
    expected_card1.x = 133
    expected_page.append(expected_card1.to_element())
    expected_card2 = SvgCard('N')
    expected_card2.scale = 0.5
    expected_card2.rotation = 90
    expected_card2.x = 133
    expected_card2.y = 85.5
    expected_page.append(expected_card2.to_element())
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(133, 171)
    page.append(ET.Element('rect',
                           {'width': '260',
                            'height': '266',
                            'fill': 'ivory'}))
    grid = SvgGrid(['PN'])
    grid.rotation = 90
    grid.x = 133
    grid.scale = 171 / grid.base_width
    page.append(grid.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)
