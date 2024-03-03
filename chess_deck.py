import math
import typing
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
from subprocess import run, Popen

import numpy as np
from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from diagram import SvgPage, SvgSymbol, SvgGroup
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
O O|
OOO|
O O|
---+
OOO|
O O|
OOO|
---+
OOO|
OOO|
OOO|
---+
"""


class SvgPips(SvgGroup):
    def __init__(self, pips: int) -> None:
        super().__init__()
        self.pips = pips

    def to_element(self) -> ET.Element:
        group = super().to_element()
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


class SvgCard(SvgGroup):
    BASE_WIDTH = 171
    BASE_HEIGHT = 266
    PIPS = dict(p=0, n=1, b=2, r=3, q=5, k=6)

    def __init__(self, symbol: str, has_border: bool = True) -> None:
        super().__init__()
        if len(symbol) == 1:
            self.symbol = symbol
            self.pips = self.PIPS[symbol.lower()]
        else:
            self.symbol = symbol[0]
            self.pips = int(symbol[1:])
        self.rect_width = self.BASE_WIDTH
        self.rect_height = self.BASE_HEIGHT
        self.has_border = has_border

    def to_element(self) -> ET.Element:
        symbol_size = SvgSymbol.BASE_SIZE / 2
        group = super().to_element()
        x = y = 0
        rect_width = self.rect_width
        rect_height = self.rect_height
        if self.has_border:
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
        if self.pips:
            pips = SvgPips(self.pips)
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


class SvgCardBack(SvgCard):
    BASE_WIDTH = 150
    BASE_HEIGHT = 225

    def __init__(self):
        super().__init__('p')

    def to_element(self) -> ET.Element:
        group = super().to_element()
        group.clear()
        board = ET.Element('g')
        group.append(board)
        board.set('transform',
                  f'translate({self.x} {self.y}) '
                  f'scale({self.scale}) ')

        columns, rows = 8, 13
        gutter = self.rect_width * 0.1
        size = (self.rect_width - 2*gutter) / columns
        xc = (self.rect_width + (columns % 2) * size) / 2
        yc = (self.rect_height + (rows % 2) * size) / 2
        border = ET.Element('rect',
                            dict(x=str(xc - columns // 2 * size),
                                 y=str(yc - (rows + 1) // 2 * size),
                                 width=str(columns * size),
                                 height=str(rows * size),
                                 rx=str(size / 3),
                                 fill='transparent',
                                 stroke='black'))
        clip_id = 'border-clip'
        clip_path = ET.Element('clipPath',
                               dict(id=clip_id))
        clip_path.append(deepcopy(border))
        board.append(clip_path)
        board.append(border)
        steps = 50
        for i in range(-rows//2, -rows//2 + rows):
            for j in range(-columns//2, -columns//2 + columns):
                if i % 2 != j % 2:
                    continue
                x0 = j * size + xc
                y0 = i * size + yc
                points = []
                for k in range(steps):
                    x1, y1 = self.convert_coordinates(x0 + k * size / steps,
                                                      y0)
                    points.append(f'{x1},{y1}')
                for k in range(steps):
                    x1, y1 = self.convert_coordinates(x0 + size,
                                                      y0 + k * size / steps)
                    points.append(f'{x1},{y1}')
                for k in range(steps):
                    x1, y1 = self.convert_coordinates(x0 + (steps - k) * size / steps,
                                                      y0 + size)
                    points.append(f'{x1},{y1}')
                for k in range(steps):
                    x1, y1 = self.convert_coordinates(x0,
                                                      y0 + (steps - k) * size / steps)
                    points.append(f'{x1},{y1}')
                board.append(ET.Element('polygon',
                                        {'points': ' '.join(points),
                                         'fill': 'black',
                                         'clip-path': f'url(#{clip_id})'}))
        return group

    def convert_coordinates(self,
                            x: float,
                            y: float) -> typing.Tuple[float, float]:
        x0 = self.rect_width / 2
        y0 = self.rect_height / 2
        z = x - x0 + 1j*(y - y0)  # convert to complex number
        theta = np.angle(z)
        r = np.abs(z)
        theta += self.sigmoid((r-self.rect_width/4)*0.25) * np.pi
        z2 = r * np.exp(1j*theta)
        x2 = np.real(z2) + x0
        y2 = np.imag(z2) + y0
        return x2, y2

    @staticmethod
    def sigmoid(x: float):
        return 1 / (1 + math.exp(-x))


class SvgGrid(SvgGroup):
    def __init__(self, symbols: typing.List[str]) -> None:
        super().__init__()
        self.symbols = symbols
        self.base_width = SvgCard.BASE_WIDTH * len(symbols[0])
        self.base_height = SvgCard.BASE_HEIGHT * len(symbols)

    def to_element(self) -> ET.Element:
        group = super().to_element()
        for i, row in enumerate(self.symbols):
            for j, symbol in enumerate(row):
                card = SvgCard(symbol)
                card.x = j * card.BASE_WIDTH
                card.y = i * card.BASE_HEIGHT
                group.append(card.to_element())
        return group


def generate_images():
    output_width = 750
    output_height = 1125
    image_folder = Path(__file__).parent / 'deck'
    image_folder.mkdir(exist_ok=True)
    page = SvgPage(output_width, output_height)
    page.append(ET.Element('rect', dict(fill='white',
                                        width=str(output_width),
                                        height=str(output_height))))
    card_back = SvgCardBack()
    card_back.scale = page.height / card_back.rect_height
    page.append(card_back.to_element())
    diagram = SvgDiagram(page.to_svg())
    diagram.to_cairo(image_folder / 'back.png',
                     output_width=output_width,
                     output_height=output_height)
    for symbol in 'K Q R B N P k q r b n p C4 C7 C8 C9 c4 c7 c8 c9'.split():
        filename = image_folder / f'card-{symbol}.png'
        page = SvgPage(output_width, output_height)
        page.append(ET.Element('rect', dict(fill='white',
                                            width=str(output_width),
                                            height=str(output_height))))
        card = SvgCard(symbol, has_border=False)
        bleed = 0.05
        y_margin = page.height * bleed
        card.scale = (page.height - 2 * y_margin) / card.rect_height
        card.x = (page.width - card.rect_width * card.scale) / 2
        card.y = (page.height - card.rect_height * card.scale) / 2
        page.append(card.to_element())
        diagram = SvgDiagram(page.to_svg())
        diagram.to_cairo(filename,
                         output_width=output_width,
                         output_height=output_height)


def main() -> None:
    generate_images()
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
    are_checkers_included = False
    if are_checkers_included:
        symbol_pages.append([['C4', 'C7', 'C8', 'C9'], ['c4', 'c7', 'c8', 'c9']])
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
