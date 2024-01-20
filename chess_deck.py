import typing
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
from subprocess import call

import chess.svg
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate

from diagram import Diagram
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


class SvgPage:
    def __init__(self, width: float, height: float) -> None:
        self.root = ET.XML(f'<svg xmlns="http://www.w3.org/2000/svg" '
                           f'viewBox="0 0 {width} {height}" '
                           f'width="{width}" height="{height}"/>')

    def append(self, element: ET.Element) -> None:
        self.root.append(element)

    def to_svg(self) -> str:
        return ET.tostring(self.root, encoding='unicode')


class SvgSymbol:
    BASE_SIZE = 45

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.scale = 1
        self.rotation = 0
        self.x = self.y = 0

    def to_element(self) -> ET.Element:
        piece_svg = chess.svg.piece(chess.Piece.from_symbol(self.symbol))
        Diagram.register_svg()
        piece_tree = ET.XML(piece_svg)
        ns = {'': 'http://www.w3.org/2000/svg'}
        piece_group = piece_tree.find('g', ns)
        piece_group.set('transform',
                        f'translate({self.x} {self.y}) '
                        f'scale({self.scale}) '
                        f'rotate({self.rotation}) '
                        f'translate({-self.BASE_SIZE/2} {-self.BASE_SIZE/2})')
        return piece_group


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
    ONE_PIP_CODEPOINT = 0x2680

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
        group.append(ET.Element('rect',
                                {'width': str(self.BASE_WIDTH),
                                 'height': str(self.BASE_HEIGHT),
                                 'fill': 'white',
                                 'stroke': 'black',
                                 'stroke-width': '4'}))
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
    vertical_margin = 0.85 * inch
    side_margin = 0.6 * inch

    pdf_path = Path(__file__).parent / 'docs' / 'chess_deck.pdf'
    doc = SimpleDocTemplate(str(pdf_path),
                            title='Chess Deck',
                            author='Don Kirkby',
                            pagesize=page_size,
                            leftMargin=side_margin,
                            rightMargin=side_margin,
                            topMargin=vertical_margin,
                            bottomMargin=vertical_margin)
    diagrams = []
    symbol_pages = [['rnbq', 'pppp'],
                    ['kbnr', 'pppp'],
                    ['PPPP', 'RNBQ'],
                    ['PPPP', 'KBNR']]
    for symbol_page in symbol_pages:
        svg_page = SvgPage(7.5*inch, 9*inch)
        grid = SvgGrid(symbol_page)
        grid.rotation = 90
        grid.x = 7*inch
        grid.scale = 7*inch / grid.base_height
        svg_page.append(grid.to_element())
        diagram = SvgDiagram(svg_page.to_svg()).to_reportlab()
        diagrams.append(diagram)
    doc.build(diagrams)
    print('Done.')
    call(["evince", pdf_path])


if __name__ == '__main__':
    main()
