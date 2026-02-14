# noinspection PyPep8Naming
import xml.etree.ElementTree as ET

from diagram_differ import DiagramDiffer
from letter_board import SvgSquare, SvgLetter, SvgPlank, SvgSheet
from svg_diagram import SvgDiagram
from svg_page import SvgPage


def test_dark_letter(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(150, 150)
    expected_page.append(ET.Element('rect', {
        'fill': 'white',
        'width': '150',
        'height': '150',
        'stroke': 'black'}))
    expected_page.append_text('A', {
        'x': '75',
        'y': '110',
        'text-anchor': 'middle',
        'font-family': 'FredokaOne',
        'font-size': '100'})

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(150, 150)
    page.append(ET.Element('rect', {
        'fill': 'white',
        'width': '150',
        'height': '150',
        'stroke': 'black'}))
    letter = SvgLetter(letter='A', shade=0)
    letter.x = 75
    letter.y = 75
    page.append(letter.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal_diagrams(svg_diagram, expected_diagram)


def test_light_letter(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(150, 150)
    expected_page.append(ET.Element('rect', {
        'fill': 'black',
        'width': '150',
        'height': '150',
        'stroke': 'black'}))
    expected_page.append_text('A', {
        'x': '75',
        'y': '110',
        'text-anchor': 'middle',
        'font-family': 'FredokaOne',
        'font-size': '100',
        'fill': 'white'})

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(150, 150)
    page.append(ET.Element('rect', {
        'fill': 'black',
        'width': '150',
        'height': '150',
        'stroke': 'black'}))
    letter = SvgLetter(letter='A', shade=255)
    letter.x = 75
    letter.y = 75
    page.append(letter.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal_diagrams(svg_diagram, expected_diagram)


def test_light_square(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(150, 150)
    expected_page.append(ET.Element('rect',
                                    {'fill': '#a0a0a0',
                                     'width': '150',
                                     'height': '150',
                                     'stroke': '#808080',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': '#c0c0c0',
                                     'x': '2',
                                     'y': '2',
                                     'width': '146',
                                     'height': '146',
                                     'stroke': '#a0a0a0',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': '#e0e0e0',
                                     'x': '4',
                                     'y': '4',
                                     'width': '142',
                                     'height': '142',
                                     'stroke': '#c0c0c0',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'white',
                                     'x': '6',
                                     'y': '6',
                                     'width': '138',
                                     'height': '138',
                                     'stroke': '#e0e0e0',
                                     'stroke-width': '2'}))
    top_letter = SvgLetter(letter='B', shade=0)
    top_letter.x = 30
    top_letter.y = 35
    top_letter.scale = 0.5
    top_letter.rotation = 180
    expected_page.append(top_letter.to_element())
    bottom_letter = SvgLetter(letter='B', shade=0)
    bottom_letter.x = 120
    bottom_letter.y = 115
    bottom_letter.scale = 0.5
    expected_page.append(bottom_letter.to_element())

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(150, 150)
    square = SvgSquare(letter='B', shade=255)
    page.append(square.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal_diagrams(svg_diagram, expected_diagram)


def test_dark_square(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(150, 150)
    expected_page.append(ET.Element('rect',
                                    {'fill': '#606060',
                                     'width': '150',
                                     'height': '150',
                                     'stroke': '#808080',
                                     'stroke-width': '4'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': '#404040',
                                     'x': '2',
                                     'y': '2',
                                     'width': '146',
                                     'height': '146',
                                     'stroke': '#606060',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': '#202020',
                                     'x': '4',
                                     'y': '4',
                                     'width': '142',
                                     'height': '142',
                                     'stroke': '#404040',
                                     'stroke-width': '2'}))
    expected_page.append(ET.Element('rect',
                                    {'fill': 'black',
                                     'x': '6',
                                     'y': '6',
                                     'width': '138',
                                     'height': '138',
                                     'stroke': '#202020',
                                     'stroke-width': '2'}))
    top_letter = SvgLetter(letter='B', shade=255)
    top_letter.x = 30
    top_letter.y = 35
    top_letter.scale = 0.5
    top_letter.rotation = 180
    expected_page.append(top_letter.to_element())
    bottom_letter = SvgLetter(letter='B', shade=255)
    bottom_letter.x = 120
    bottom_letter.y = 115
    bottom_letter.scale = 0.5
    expected_page.append(bottom_letter.to_element())

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(150, 150)
    square = SvgSquare(letter='B', shade=0)
    page.append(square.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal_diagrams(svg_diagram, expected_diagram)


def test_light_plank(diagram_differ: DiagramDiffer):
    expected_page = SvgPage(450, 150)
    expected_page.append(SvgSquare(letter='A', shade=0).to_element())
    letter_b = SvgSquare(letter='B', shade=255)
    letter_b.x = 150
    expected_page.append(letter_b.to_element())
    letter_c = SvgSquare(letter='C', shade=0)
    letter_c.x = 300
    expected_page.append(letter_c.to_element())

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(450, 150)
    plank = SvgPlank(letters='ABC', shade=0)
    page.append(plank.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal_diagrams(svg_diagram, expected_diagram)


def test_light_sheet(diagram_differ: DiagramDiffer):
    scale = 270 / 450
    expected_page = SvgPage(270, 270)
    plank1 = SvgPlank(letters='ABC', shade=0)
    plank1.scale = scale
    expected_page.append(plank1.to_element())
    plank2 = SvgPlank(letters='DEF', shade=255)
    plank2.scale = scale
    plank2.y = 90
    expected_page.append(plank2.to_element())
    plank3 = SvgPlank(letters='GHI', shade=0)
    plank3.scale = scale
    plank3.y = 180
    expected_page.append(plank3.to_element())

    expected_diagram = SvgDiagram(expected_page.to_svg())

    page = SvgPage(270, 270)
    sheet = SvgSheet(letters='ABC\nDEF\nGHI', shade=0)
    sheet.scale = scale
    page.append(sheet.to_element())
    svg_diagram = SvgDiagram(page.to_svg())

    diagram_differ.assert_equal_diagrams(svg_diagram, expected_diagram)
