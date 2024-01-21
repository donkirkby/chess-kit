import typing
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
from subprocess import run, Popen

from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from diagram import SvgPage, SvgSymbol
from font_set import register_fonts
from publish_rules import create_cc_section
from svg_diagram import SvgDiagram

PIP_PATTERNS = """\
---+
   |
   |
   |
---+
   |
 O |
   |
---+
O  |
   |
  O|
---+
O  |
 O |
  O|
---+
O O|
   |
O O|
---+
O O|
 O |
O O|
---+
O O|
O O|
O O|
---+
"""


class SvgPips:
    def __init__(self, pips: int) -> None:
        self.pips = pips
        self.x = self.y = 0
        self.scale = 1

    def to_element(self) -> ET.Element:
        group = ET.Element('g')
        group.set('transform',
                  f'translate({self.x} {self.y}) scale({self.scale})')
        pips = self.pips
        pip_pattern = PIP_PATTERNS.splitlines()[pips * 4 + 1:pips * 4 + 4]

        for i in range(3):
            for j in range(3):
                if pip_pattern[i][j] == 'O':
                    group.append(ET.Element('circle',
                                            {'fill': 'black',
                                             'cx': str(10*(j-1)),
                                             'cy': str(10*(i-1)),
                                             'r': '3'}))
        return group


class SvgCard:
    BASE_WIDTH = 171
    BASE_HEIGHT = 266
    PIPS = dict(p=0, n=1, b=2, r=3, q=5, k=6)

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.scale = 1
        self.x = self.y = 0
        self.rotation = 0

    def to_element(self) -> ET.Element:
        symbol_size = SvgSymbol.BASE_SIZE / 2
        group = ET.Element('g')
        group.set('transform',
                  f'translate({self.x} {self.y}) '
                  f'scale({self.scale}) '
                  f'rotate({self.rotation})')
        x = y = 0
        rect_width = 171
        rect_height = 266
        for layer in range(4):
            stroke_width = '4' if layer == 0 else '2'
            stroke = '#' + ('bcde'[layer]) * 6
            group.append(ET.Element(
                'rect',
                {'fill': 'white',
                 'x': str(x),
                 'y': str(y),
                 'width': str(rect_width),
                 'height': str(rect_height),
                 'stroke': stroke,
                 'stroke-width': stroke_width}))
            diff = 3 if layer == 0 else 2
            x += diff
            y += diff
            rect_width -= 2*diff
            rect_height -= 2*diff
        pips_count = self.PIPS[self.symbol.lower()]
        if pips_count:
            pips = SvgPips(pips_count)
            pips.x = self.BASE_WIDTH / 2
            pips.y = self.BASE_HEIGHT / 2
            pips.scale = 0.75
            group.append(pips.to_element())
        symbol1 = SvgSymbol(self.symbol)
        symbol1.scale = 0.75
        symbol1.x = symbol_size
        symbol1.y = symbol_size
        group.append(symbol1.to_element())
        symbol2 = deepcopy(symbol1)
        symbol2.rotation = 180
        symbol2.x = self.BASE_WIDTH - symbol_size
        symbol2.y = self.BASE_HEIGHT - symbol_size
        group.append(symbol2.to_element())
        symbol3 = deepcopy(symbol1)
        symbol3.scale = 1.75
        symbol3.x = self.BASE_WIDTH / 2
        symbol3.y = self.BASE_HEIGHT / 2 - symbol_size*2
        group.append(symbol3.to_element())
        symbol4 = deepcopy(symbol3)
        symbol4.y = self.BASE_HEIGHT / 2 + symbol_size*2
        symbol4.rotation = 180
        group.append(symbol4.to_element())
        return group


class SvgGrid:
    def __init__(self, symbols: typing.List[str]) -> None:
        self.symbols = symbols
        self.base_width = SvgCard.BASE_WIDTH * len(symbols[0])
        self.base_height = SvgCard.BASE_HEIGHT * len(symbols)
        self.x = self.y = 0
        self.scale = 1
        self.rotation = 0

    def to_element(self) -> ET.Element:
        group = ET.Element('g')
        group.set('transform',
                  f'translate({self.x} {self.y}) '
                  f'scale({self.scale}) '
                  f'rotate({self.rotation})')
        for i, row in enumerate(self.symbols):
            for j, symbol in enumerate(row):
                card = SvgCard(symbol)
                card.x = j * card.BASE_WIDTH
                card.y = i * card.BASE_HEIGHT
                group.append(card.to_element())
        return group


def main() -> None:
    page_size = pagesizes.letter
    top_margin = 0.85 * inch
    bottom_margin = 0.1 * inch
    side_margin = 0.6 * inch
    register_fonts()
    styles = getSampleStyleSheet()

    pdf_path = Path(__file__).parent / 'docs' / 'chess-deck.pdf'
    doc = SimpleDocTemplate(str(pdf_path),
                            title='Chess Deck',
                            author='Don Kirkby',
                            subject='Playing cards to match the 32 chess pieces',
                            keywords=['chess',
                                      'games',
                                      'card-games',
                                      'board-games',
                                      'puzzles'],
                            creator=PDFInfo.creator,
                            pagesize=page_size,
                            leftMargin=side_margin,
                            rightMargin=side_margin,
                            topMargin=top_margin,
                            bottomMargin=bottom_margin)
    title_style = styles['Title']
    title_style.fontName = 'Heading'
    body_style = styles['Normal']
    body_style.fontName = 'Body'
    centred_style = ParagraphStyle('Centred',
                                   parent=body_style,
                                   alignment=TA_CENTER)
    flowables = [
        Paragraph('Chess Deck', title_style),
        Paragraph('Designed by Don Kirkby. Find game rules at '
                  '<a href="https://donkirkby.github.io/chess-kit/">donkirkby.github.io/chess-kit</a>.',
                  body_style),
        Spacer(0, 0.125*inch)]
    symbol_pages = [['rnbq', 'pppp'],
                    ['kbnr', 'pppp'],
                    ['PPPP', 'RNBQ'],
                    ['PPPP', 'KBNR']]
    for symbol_page in symbol_pages:
        svg_page = SvgPage(7.5 * inch, 9 * inch)
        grid = SvgGrid(symbol_page)
        grid.rotation = 90
        grid.x = 7*inch
        grid.scale = 7*inch / grid.base_height
        svg_page.append(grid.to_element())
        diagram = SvgDiagram(svg_page.to_svg()).to_reportlab()
        flowables.append(diagram)
    flowables.extend(create_cc_section(doc, centred_style))
    doc.build(flowables)
    try:
        run(['pdfsizeopt', '--v=30', pdf_path, pdf_path])
    except FileNotFoundError:
        print('pdfsizeopt not installed, so PDF is not optimized.')
    try:
        Popen(["evince", pdf_path])
    except FileNotFoundError:
        print('PDF viewer evince is not installed.')
    print('Done.')


if __name__ == '__main__':
    main()
