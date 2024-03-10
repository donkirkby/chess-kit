import math
import typing
# noinspection PyPep8Naming
from copy import deepcopy
from xml.etree import ElementTree as ET  # noqa

import chess.svg
import numpy as np

from svg_page import SvgPage, SvgGroup

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

    def __init__(self,
                 symbol: str,
                 has_border: bool = True,
                 has_outline: bool = False) -> None:
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
        self.has_outline = has_outline

    def to_element(self) -> ET.Element:
        symbol_size = SvgSymbol.BASE_SIZE / 2
        group = super().to_element()
        x = y = 0
        rect_width = self.rect_width
        rect_height = self.rect_height
        if self.has_outline:
            group.append(ET.Element('rect',
                                    attrib={'x': str(x),
                                            'y': str(y),
                                            'rx': str(rect_width*0.045),
                                            'width': str(rect_width),
                                            'height': str(rect_height),
                                            'stroke': 'black',
                                            'stroke-width': str(rect_width*0.01),
                                            'fill': 'white'}))
        elif not self.has_border:
            group.append(ET.Element('rect',
                                    attrib={'x': str(x),
                                            'y': str(y),
                                            'width': str(rect_width),
                                            'height': str(rect_height),
                                            'fill': 'white'}))
        else:
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
        text_args = {'text-anchor': 'middle',
                     'font-family': 'FredokaOne',
                     'font-size': '35',
                     'y': '17.5'}
        text = ET.Element('text', attrib=text_args)
        text.text = self.symbol.upper()
        text.attrib['transform'] = 'translate(22.5 17.5)'
        group.append(text)
        text = deepcopy(text)
        text.attrib['transform'] = (
            f'translate({self.rect_width - 22.5} {self.rect_height - 17.5}) '
            f'rotate(180)')
        group.append(text)
        symbol1 = SvgSymbol(self.symbol)
        symbol1.scale = 1.75
        symbol1.x = self.BASE_WIDTH / 2
        symbol1.y = self.BASE_HEIGHT / 2 - symbol_size * 2
        group.append(symbol1.to_element())
        symbol2 = deepcopy(symbol1)
        symbol2.y = self.BASE_HEIGHT / 2 + symbol_size * 2
        symbol2.rotation = 180
        group.append(symbol2.to_element())
        return group


class SvgCardBack(SvgCard):
    BASE_WIDTH = 150
    BASE_HEIGHT = 225

    def __init__(self, has_outline: bool = False):
        super().__init__('p')
        self.has_outline = has_outline

    def to_element(self) -> ET.Element:
        group = super().to_element()
        group.clear()
        board = ET.Element('g')
        body_attribs = dict(width=str(self.rect_width),
                            height=str(self.rect_height),
                            fill='white')
        if self.has_outline:
            body_attribs['rx'] = str(self.rect_width * 0.045)
            body_attribs['stroke'] = 'black'
            body_attribs['stroke-width'] = str(self.rect_width * 0.01)
        board.append(ET.Element('rect', attrib=body_attribs))
        group.append(board)
        board.set('transform',
                  f'translate({self.x} {self.y}) '
                  f'scale({self.scale}) ')

        columns, rows = 8, 13
        gutter = self.rect_width * 0.07
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


class SvgSymbol(SvgGroup):
    BASE_SIZE = 45

    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol

    def to_element(self) -> ET.Element:
        if self.symbol.upper() == 'C':
            return self.checker_element()
        piece_svg = chess.svg.piece(chess.Piece.from_symbol(self.symbol))
        SvgPage.register_svg()
        piece_tree = ET.XML(piece_svg)
        ns = {'': 'http://www.w3.org/2000/svg'}
        piece_group = piece_tree.find('g', ns)
        x_offset = -self.BASE_SIZE / 2
        if self.symbol.upper() == 'Q':
            x_offset += 0.2
        elif self.symbol.upper() == 'K':
            x_offset += 0.5
        piece_group.set('transform',
                        f'translate({x_offset} {-self.BASE_SIZE / 2})')
        parent_group = super().to_element()
        parent_group.append(piece_group)
        return parent_group

    def checker_element(self) -> ET.Element:
        group = super().to_element()
        r1 = 13.5
        r2 = 15.5
        if self.symbol == 'C':
            fill = 'transparent'
            stroke = 'black'
        else:
            fill = 'black'
            stroke = 'white'
            r2 += 1.5
        group.append(ET.Element('circle',
                                {'r': '17',
                                 'fill': fill,
                                 'stroke': 'black',
                                 'stroke-width': '1.5'}))
        group.append(ET.Element('circle',
                                {'r': '12',
                                 'fill': 'transparent',
                                 'stroke': stroke,
                                 'stroke-width': '1.5'}))
        ridge_count = 48
        for i in range(ridge_count):
            theta = i / ridge_count * 2 * np.pi
            z1 = r1 * np.exp(1j * theta)
            z2 = r2 * np.exp(1j * theta)
            group.append(ET.Element('line',
                                    {'x1': str(np.real(z1)),
                                     'y1': str(np.imag(z1)),
                                     'x2': str(np.real(z2)),
                                     'y2': str(np.imag(z2)),
                                     'stroke': stroke,
                                     'stroke-width': '1'}))

        return group
