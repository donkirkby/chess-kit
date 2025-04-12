# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy
from textwrap import dedent

import chess.svg

from chess_deck import (SvgCard, SvgGrid, SvgPips, SvgCardBack, SvgSymbol,
                        LETTER_PATHS, BAR_PATH, SvgAid, parse_player_aids)
from svg_page import SvgPage
from diagram_differ import DiagramDiffer
from svg_diagram import SvgDiagram


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
    SvgPage.register_svg()
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
                                    {'fill': 'white',
                                     'width': '171',
                                     'height': '266',
                                     'stroke': '#bbbbbb',
                                     'stroke-width': '4'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '3',
                                     'y': '3',
                                     'width': '165',
                                     'height': '260',
                                     'stroke': '#cccccc',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '5',
                                     'y': '5',
                                     'width': '161',
                                     'height': '256',
                                     'stroke': '#dddddd',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '7',
                                     'y': '7',
                                     'width': '157',
                                     'height': '252',
                                     'stroke': '#eeeeee',
                                     'stroke-width': '2'}))
    expected_pips = SvgPips(5)
    expected_pips.x = 85.5
    expected_pips.y = 133
    expected_pips.scale = 0.75
    expected_page.append(expected_pips.to_element())
    card_symbol = 'Q'
    expected_piece1 = SvgSymbol(card_symbol)
    expected_piece1.x = 85.5
    expected_piece1.y = 133 - 45
    expected_piece1.scale = 1.75
    expected_page.append(expected_piece1.to_element())
    expected_piece2 = deepcopy(expected_piece1)
    expected_piece2.rotation = 180
    expected_piece2.y = 133 + 45
    expected_page.append(expected_piece2.to_element())

    letter_path = ET.Element('path',
                             attrib=dict(d=LETTER_PATHS['q'],
                                         transform='scale(0.85)'))
    expected_page.append(letter_path)
    letter_path = deepcopy(letter_path)
    letter_path.attrib['transform'] = f'translate(171 266) rotate(180) scale(0.85)'
    expected_page.append(letter_path)

    bar_path = deepcopy(letter_path)
    bar_path.attrib['transform'] = 'scale(0.85)'
    bar_path.attrib['d'] = BAR_PATH
    bar_path.attrib['fill'] = 'transparent'
    bar_path.attrib['stroke'] = 'black'
    bar_path.attrib['stroke-width'] = '2'
    expected_page.append(bar_path)

    bar_path = deepcopy(bar_path)
    bar_path.attrib['transform'] = letter_path.attrib['transform']
    expected_page.append(bar_path)

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
def test_card_no_border(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_page.append(ET.Element('rect',
                                    attrib={'fill': 'white',
                                            'width': '171',
                                            'height': '266'}))
    expected_pips = SvgPips(5)
    expected_pips.x = 85.5
    expected_pips.y = 133
    expected_pips.scale = 0.75
    expected_page.append(expected_pips.to_element())
    card_symbol = 'Q'
    expected_piece1 = SvgSymbol(card_symbol)
    expected_piece1.x = 85.5
    expected_piece1.y = 133 - 45
    expected_piece1.scale = 1.75
    expected_page.append(expected_piece1.to_element())
    expected_piece2 = deepcopy(expected_piece1)
    expected_piece2.rotation = 180
    expected_piece2.y = 133 + 45
    expected_page.append(expected_piece2.to_element())

    letter_path = ET.Element('path',
                             attrib=dict(d=LETTER_PATHS['q'],
                                         transform='scale(0.85)'))
    expected_page.append(letter_path)
    letter_path = deepcopy(letter_path)
    letter_path.attrib['transform'] = f'translate(171 266) rotate(180) scale(0.85)'
    expected_page.append(letter_path)

    bar_path = deepcopy(letter_path)
    bar_path.attrib['transform'] = 'scale(0.85)'
    bar_path.attrib['d'] = BAR_PATH
    bar_path.attrib['fill'] = 'transparent'
    bar_path.attrib['stroke'] = 'black'
    bar_path.attrib['stroke-width'] = '2'
    expected_page.append(bar_path)

    bar_path = deepcopy(bar_path)
    bar_path.attrib['transform'] = letter_path.attrib['transform']
    expected_page.append(bar_path)

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(171, 266)
    card = SvgCard(card_symbol, has_border=False)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card_outline(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_page.append(ET.Element('rect',
                                    attrib={'fill': 'white',
                                            'width': '171',
                                            'height': '266',
                                            'rx': '7.7',
                                            'stroke': 'black',
                                            'stroke-width': '1.7'}))
    expected_pips = SvgPips(5)
    expected_pips.x = 85.5
    expected_pips.y = 133
    expected_pips.scale = 0.75
    expected_page.append(expected_pips.to_element())
    card_symbol = 'Q'
    expected_piece1 = SvgSymbol(card_symbol)
    expected_piece1.x = 85.5
    expected_piece1.y = 133 - 45
    expected_piece1.scale = 1.75
    expected_page.append(expected_piece1.to_element())
    expected_piece2 = deepcopy(expected_piece1)
    expected_piece2.rotation = 180
    expected_piece2.y = 133 + 45
    expected_page.append(expected_piece2.to_element())

    letter_path = ET.Element('path',
                             attrib=dict(d=LETTER_PATHS['q'],
                                         transform='scale(0.85)'))
    expected_page.append(letter_path)
    letter_path = deepcopy(letter_path)
    letter_path.attrib['transform'] = f'translate(171 266) rotate(180) scale(0.85)'
    expected_page.append(letter_path)

    bar_path = deepcopy(letter_path)
    bar_path.attrib['transform'] = 'scale(0.85)'
    bar_path.attrib['d'] = BAR_PATH
    bar_path.attrib['fill'] = 'transparent'
    bar_path.attrib['stroke'] = 'black'
    bar_path.attrib['stroke-width'] = '2'
    expected_page.append(bar_path)

    bar_path = deepcopy(bar_path)
    bar_path.attrib['transform'] = letter_path.attrib['transform']
    expected_page.append(bar_path)

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(171, 266)
    card = SvgCard(card_symbol, has_border=False, has_outline=True)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card_checker(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_page.append(ET.Element('rect',
                                    attrib={'width': '171',
                                            'height': '266',
                                            'fill': 'white'}))
    expected_pips = SvgPips(9)
    expected_pips.x = 85.5
    expected_pips.y = 133
    expected_pips.scale = 0.75
    expected_page.append(expected_pips.to_element())
    expected_piece1 = SvgSymbol('C')
    expected_piece1.x = 85.5
    expected_piece1.y = 133 - 45
    expected_piece1.scale = 1.75
    expected_page.append(expected_piece1.to_element())
    expected_piece2 = deepcopy(expected_piece1)
    expected_piece2.rotation = 180
    expected_piece2.y = 133 + 45
    expected_page.append(expected_piece2.to_element())

    letter_path = ET.Element('path',
                             attrib=dict(d=LETTER_PATHS['c'],
                                         transform='scale(0.85)'))
    expected_page.append(letter_path)
    letter_path = deepcopy(letter_path)
    letter_path.attrib['transform'] = f'translate(171 266) rotate(180) scale(0.85)'
    expected_page.append(letter_path)

    bar_path = deepcopy(letter_path)
    bar_path.attrib['transform'] = 'scale(0.85)'
    bar_path.attrib['d'] = BAR_PATH
    bar_path.attrib['fill'] = 'transparent'
    bar_path.attrib['stroke'] = 'black'
    bar_path.attrib['stroke-width'] = '2'
    expected_page.append(bar_path)

    bar_path = deepcopy(bar_path)
    bar_path.attrib['transform'] = letter_path.attrib['transform']
    expected_page.append(bar_path)

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(171, 266)
    card = SvgCard('C9', has_border=False)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card_back(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(150, 225)
    expected_back = SvgCardBack()
    expected_page.append(expected_back.to_element())
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(150, 225)
    card = SvgCardBack()
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_card_back_outline(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(150, 225)
    expected_back = SvgCardBack(has_outline=True)
    expected_page.append(expected_back.to_element())
    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(150, 225)
    card = SvgCardBack(has_outline=True)
    page.append(card.to_element())
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


def test_parse_player_aids():
    markdown = dedent("""\
        ## Game 1
        Some text.
        
        Some more text.
        
        ## Game 2
        Other text
        on multiple lines.
        
        Last text.
        """)

    parsed_aids = parse_player_aids(markdown)

    assert len(parsed_aids) == 2
    game2_name, game2_states = parsed_aids[1]
    assert game2_name == 'Game 2'
    assert len(game2_states) == 2
    assert game2_states[0].text == 'Other text on multiple lines.'
    assert game2_states[1].text == 'Last text.'


# noinspection DuplicatedCode
def test_player_aid(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'width': '171',
                                     'height': '266',
                                     'stroke': '#bbbbbb',
                                     'stroke-width': '4'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'width': '171',
                                     'height': '266',
                                     'stroke': '#bbbbbb',
                                     'stroke-width': '4'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '3',
                                     'y': '3',
                                     'width': '165',
                                     'height': '260',
                                     'stroke': '#cccccc',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '5',
                                     'y': '5',
                                     'width': '161',
                                     'height': '256',
                                     'stroke': '#dddddd',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '7',
                                     'y': '7',
                                     'width': '157',
                                     'height': '252',
                                     'stroke': '#eeeeee',
                                     'stroke-width': '2'}))
    expected_page.append_text('Two Move Chess',
                              {
                                  'x': '85.5',
                                  'y': '32',
                                  'text-anchor': 'middle',
                                  'font-family': 'FredokaOne',
                                  'font-size': '16'})
    expected_page.append_text('1. Both choose 2 cards.',
                              {
                                  'x': '15',
                                  'y': '55',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('2. Reveal, drop duplicates.',
                              {
                                  'x': '15',
                                  'y': '73',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('3. Play cards, in order:',
                              {
                                  'x': '15',
                                  'y': '91',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('N, B, R, Q, K.',
                              {
                                  'x': '26',
                                  'y': '103',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('One card? Play it twice.',
                              {
                                  'x': '15',
                                  'y': '127',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('Pawns move once.',
                              {
                                  'x': '15',
                                  'y': '151',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_diagram = SvgDiagram(expected_page.to_svg())

    markdown = dedent("""\
        ## Two Move Chess
        1. Both choose 2 cards.
        2. Reveal, drop duplicates.
        3. Play cards, in order:
            N, B, R, Q, K.
        
        One card? Play it twice.
        
        Pawns move once.
        """)
    parsed_aids = parse_player_aids(markdown)
    game_name, markdown_states = parsed_aids[0]
    page = SvgPage(171, 266)
    card = SvgAid(game_name, markdown_states)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)


# noinspection DuplicatedCode
def test_player_aid_diagram(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(171, 266)
    expected_page.append(
        SvgAid('Example', []).to_element())
    expected_page.append_text('Some text before.',
                              {
                                  'x': '15',
                                  'y': '55',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    square_dark = chess.svg.DEFAULT_COLORS['square dark']
    square_light = chess.svg.DEFAULT_COLORS['square light']
    expected_page.append(ET.Element('rect',
                                    {'x': '55.5',
                                     'y': '60',
                                     'width': '60',
                                     'height': '60',
                                     'fill': square_light}))
    expected_page.append(ET.Element('rect',
                                    {'x': '85.5',
                                     'y': '60',
                                     'width': '30',
                                     'height': '30',
                                     'fill': square_dark}))
    expected_page.append(ET.Element('rect',
                                    {'x': '55.5',
                                     'y': '90',
                                     'width': '30',
                                     'height': '30',
                                     'fill': square_dark}))
    expected_page.append(ET.Element('rect',
                                    {'x': '55.5',
                                     'y': '60',
                                     'width': '60',
                                     'height': '60',
                                     'fill': 'transparent',
                                     'stroke': 'black',
                                     'stroke-width': '2'}))
    black_queen = SvgSymbol('q')
    black_queen.x = 70.5
    black_queen.y = 75
    black_queen.scale = 0.65
    expected_page.append(black_queen.to_element())
    white_queen = SvgSymbol('Q')
    white_queen.x = 70.5
    white_queen.y = 105
    white_queen.scale = 0.65
    expected_page.append(white_queen.to_element())
    black_king = SvgSymbol('k')
    black_king.x = 100.5
    black_king.y = 75
    black_king.scale = 0.65
    expected_page.append(black_king.to_element())
    white_king = SvgSymbol('K')
    white_king.x = 100.5
    white_king.y = 105
    white_king.scale = 0.65
    expected_page.append(white_king.to_element())
    expected_page.append_text('1',
                              {
                                  'x': '130.5',
                                  'y': '105',
                                  'dominant-baseline': 'middle',
                                  'text-anchor': 'middle',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('2',
                              {
                                  'x': '130.5',
                                  'y': '75',
                                  'dominant-baseline': 'middle',
                                  'text-anchor': 'middle',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('3',
                              {
                                  'x': '40.5',
                                  'y': '105',
                                  'dominant-baseline': 'middle',
                                  'text-anchor': 'middle',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('4',
                              {
                                  'x': '40.5',
                                  'y': '75',
                                  'dominant-baseline': 'middle',
                                  'text-anchor': 'middle',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_page.append_text('Some text after.',
                              {
                                  'x': '15',
                                  'y': '139',
                                  'font-family': 'Raleway',
                                  'font-size': '11'})
    expected_diagram = SvgDiagram(expected_page.to_svg())

    markdown = dedent("""\
        ## Example
        Some text before.

        4 q k 2
        3 Q K 1
        
        Some text after.
        """)
    parsed_aids = parse_player_aids(markdown)
    game_name, markdown_states = parsed_aids[0]
    page = SvgPage(171, 266)
    card = SvgAid(game_name, markdown_states)
    page.append(card.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal(svg_diagram, expected_diagram)
