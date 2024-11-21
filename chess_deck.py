import math
import typing
# noinspection PyPep8Naming
from copy import deepcopy
from xml.etree import ElementTree as ET  # noqa

import chess.svg
import numpy as np

from book_parser import parse, ParsingState
from svg_page import SvgPage, SvgGroup, SQUARE_LIGHT, SQUARE_DARK

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
LETTER_SCALE = 0.85

# Converted in Inkscape from 111pt Fredoka One font to path objects.
LETTER_PATHS = dict(
    k='m 27.3,26.1 q 5.99227,5.757284 8.49885,8.655509 1.29245,1.449112 '
      '1.29245,2.467407 0,0.97913 -1.56661,2.349912 -1.56661,1.331617 '
      '-2.5849,1.331617 -0.97913,0 -2.38908,-1.644938 l -8.61634,-9.830465 '
      'v 7.637214 q 0,0.939964 -0.0783,1.370782 -0.0392,0.430817 '
      '-0.35249,1.018295 -0.548314,1.05746 -3.054886,1.05746 -2.741564,0 '
      '-3.211547,-1.488277 -0.234991,-0.626644 -0.234991,-1.997426 '
      'v -21.77585 q 0,-0.9008 0.03916,-1.3316172 0.07833,-0.4699824 '
      '0.391652,-1.0574604 0.548313,-1.0574603 3.054886,-1.0574603 2.741561,0 '
      '3.250711,1.4491123 0.19583,0.6658084 0.19583,2.0365906 v 7.480553 '
      'q 5.32646,-5.992276 8.61634,-9.8304652 1.37078,-1.6057731 '
      '2.38908,-1.6057731 1.01829,0 2.5849,1.3707819 1.56661,1.3316168 '
      '1.56661,2.3499124 0,0.97913 -1.17496,2.349912 -2.27158,2.624068 '
      '-7.04973,7.206396 z',
    q='m 37.4,32.2 q 1.8016,1.214121 2.5849,1.762434 1.40995,1.057461 '
      '1.40995,2.036591 0,0.939964 -1.17496,2.663233 -1.17495,1.723269 '
      '-2.38907,1.723269 -0.74414,0 -2.27159,-1.057461 -0.19582,-0.117495 '
      '-1.09662,-0.744138 -0.9008,-0.626643 -1.40995,-0.939965 '
      '-3.64236,2.819894 -8.18553,2.819894 -6.070601,0 -10.261278,-4.308172 '
      '-4.151511,-4.308172 -4.151511,-10.261282 0,-3.250711 1.174956,-6.070606 '
      '1.174956,-2.859059 3.133216,-4.778154 1.95826,-1.919095 '
      '4.503998,-3.01572 2.545739,-1.096626 5.248139,-1.096626 5.79645,0 '
      '10.06545,4.190676 4.26901,4.190677 4.26901,10.613769 0,3.250712 '
      '-1.44911,6.462258 z m -20,-6.5 q 0,3.485703 '
      '2.232417,5.678954 2.271582,2.154086 5.052312,2.154086 2.78073,0 '
      '5.01314,-2.114921 2.23242,-2.114921 2.23242,-5.678954 0,-3.564033 '
      '-2.27158,-5.718119 -2.23242,-2.154086 -5.01315,-2.154086 -2.78073,0 '
      '-5.013142,2.193251 -2.232417,2.154086 -2.232417,5.639789 z',
    r='m 37,34.9 q 0.58748,1.40995 0.58748,2.03659 0,1.48828 '
      '-2.42824,2.50658 -1.25329,0.54831 -2.03659,0.54831 -0.74414,0 '
      '-1.25329,-0.35249 -0.46998,-0.39165 -0.70497,-0.7833 -0.39165,-0.74414 '
      '-3.05489,-7.0889 l -1.21412,0.0783 h -4.93481 v 4.42566 q 0,0.9008 '
      '-0.0783,1.37079 -0.0392,0.43081 -0.35249,1.01829 -0.548312,1.05746 '
      '-3.054885,1.05746 -2.741564,0 -3.211546,-1.44911 -0.234991,-0.66581 '
      '-0.234991,-2.03659 v -21.73 q 0,-0.9008 0.03916,-1.331617 '
      '0.07833,-0.469982 0.391652,-1.05746 0.548312,-1.057461 '
      '3.054885,-1.057461 h 8.45968 q 3.44654,0 6.69725,2.506573 '
      '1.56661,1.214121 2.58491,3.289877 1.01829,2.075755 1.01829,4.621493 '
      '0,4.425671 -2.93739,7.284731 0.86164,2.07575 2.66323,6.14893 z '
      'm -15.03943,-9.98712 h 5.01314 q 1.13579,0 2.27158,-0.861638 '
      '1.1358,-0.861634 1.1358,-2.584903 0,-1.723269 -1.1358,-2.584903 '
      '-1.13579,-0.900799 -2.34991,-0.900799 h -4.93481 z',
    b='m 35.4,24.9 q 2.31075,2.74156 2.31075,6.14893 -0.0783,3.91652 '
      '-2.7024,6.57976 -2.5849,2.62406 -6.3056,2.62406 h -10.3 '
      'q -2.741564,0 -3.211546,-1.48827 -0.234992,-0.66581 -0.234992,-2.03659 '
      'v -21.73669 q 0,-0.93996 0.03917,-1.37078 0.07833,-0.43082 '
      '0.391652,-1.0183 0.548312,-1.05746 3.054885,-1.05746 h 9.86963 '
      'q 3.6032,0 6.03144,2.50658 2.54574,2.54573 2.54574,6.10977 0,2.5849 '
      '-1.48828,4.73899 z m -4.62149,5.75728 q 0,-0.93996 -0.23499,-1.48828 '
      '-0.19583,-0.54831 -0.70498,-0.7833 -0.7833,-0.31332 -2.19325,-0.31332 '
      '-1.40995,0 -2.11492,-0.54832 -0.70497,-0.54831 -0.70497,-2.23241 '
      '0,-1.72327 0.70497,-2.27158 0.74414,-0.54832 2.42824,-0.54832 1.56661,0 '
      '1.87993,-0.82247 0.1175,-0.43081 0.1175,-1.40994 0,-0.97913 '
      '-0.66581,-1.37078 -0.62664,-0.39166 -1.91909,-0.39166 h -5.48313 '
      'v 14.84361 h 6.42309 q 2.46741,0 2.46741,-2.66323 z',
    n='m 31.8,11.98 q 0.39165,-0.70497 1.13579,-0.93997 0.74414,-0.23499 '
      '1.84076,-0.23499 1.13579,0 1.8016,0.19583 0.70498,0.19582 '
      '1.0183,0.46998 0.35248,0.27416 0.50914,0.82247 0.235,0.62664 '
      '0.235,1.99743 v 21.73668 q 0,0.93997 -0.0783,1.37078 -0.0392,0.43082 '
      '-0.35249,1.0183 -0.54831,1.05746 -3.05489,1.05746 -1.52744,0 '
      '-2.11492,-0.23499 -0.58748,-0.23499 -0.97913,-0.74414 '
      '-8.81217,-11.74956 -11.592897,-15.35276 v 12.88535 q 0,0.93997 '
      '-0.07833,1.37078 -0.03917,0.43082 -0.352487,1.0183 -0.548313,1.05746 '
      '-3.054885,1.05746 -2.428243,0 -2.976556,-1.05746 -0.313321,-0.58748 '
      '-0.391652,-1.05746 -0.03916,-0.46998 -0.03916,-1.37078 v -21.85419 '
      'q 0,-1.48827 0.352487,-2.15408 0.391652,-0.70497 1.135791,-0.93997 '
      '0.744139,-0.23499 1.919095,-0.23499 1.174956,0 1.840764,0.23499 '
      '0.704974,0.19583 0.97913,0.46999 0.156661,0.11749 0.9008,1.01829 '
      '8.263855,11.24041 11.044585,14.84361 v -13.23784 q 0,-1.48827 '
      '0.35249,-2.15408 z',
    p='m 35.7,16.8 q 1.01829,2.07575 1.01829,4.62149 0,2.54574 '
      '-1.01829,4.62149 -1.0183,2.03659 -2.62407,3.25071 -3.25071,2.50658 '
      '-6.73642,2.50658 h -4.89565 v 4.42567 q 0,0.90079 -0.0783,1.37078 '
      '-0.0392,0.43081 -0.35248,1.01829 -0.548317,1.05746 -3.05489,1.05746 '
      '-2.741564,0 -3.211546,-1.44911 -0.234991,-0.66581 -0.234991,-2.03659 '
      'v -21.73 q 0,-0.9008 0.03916,-1.33161 0.07833,-0.46998 '
      '0.391652,-1.05746 0.548312,-1.05746 3.054885,-1.05746 h 8.381355 '
      'q 3.44654,0 6.69725,2.50657 1.60577,1.21412 2.62407,3.28988 z '
      'm -9.32132,8.06803 q 1.17495,0 2.31074,-0.86164 1.1358,-0.86163 '
      '1.1358,-2.5849 0,-1.72327 -1.1358,-2.5849 -1.13579,-0.9008 '
      '-2.34991,-0.9008 h -4.89565 v 6.93224 z',
    c='m 33,33 0.70497,-0.50915 q 1.33162,-0.7833 1.87993,-0.7833 1.21412,0 '
      '2.62407,2.19325 0.86163,1.37078 0.86163,2.19325 0,0.82247 '
      '-0.54831,1.37078 -0.50915,0.54831 -1.21412,0.97913 -0.70497,0.43082 '
      '-1.37078,0.82247 -0.62665,0.39165 -2.62407,1.01829 -1.99743,0.62665 '
      '-3.87736,0.62665 -1.84076,0 -3.75985,-0.46999 -1.87993,-0.50914 '
      '-3.91652,-1.64493 -1.997429,-1.17496 -3.603202,-2.8199 '
      '-1.605774,-1.6841 -2.663234,-4.269 -1.018295,-2.62407 '
      '-1.018295,-5.67896 0,-3.05488 1.018295,-5.52229 1.018295,-2.50657 '
      '2.584903,-4.11235 1.605773,-1.64494 3.642364,-2.74156 3.838189,-2.11492 '
      '7.715539,-2.11492 1.84077,0 3.7207,0.58748 1.91909,0.54831 '
      '2.89822,1.13579 l 0.93997,0.54831 q 0.70497,0.43082 1.09662,0.70497 '
      '1.0183,0.82247 1.0183,1.87993 0,1.0183 -0.82247,2.15409 '
      '-1.52744,2.11492 -2.74156,2.11492 -0.70498,0 -1.99743,-0.86164 '
      '-1.64494,-1.33161 -4.3865,-1.33161 -2.54574,0 -5.01315,1.76243 '
      '-1.17495,0.86164 -1.95826,2.42824 -0.783301,1.56661 -0.783301,3.56404 '
      '0,1.95826 0.783301,3.52487 0.78331,1.5666 1.99743,2.4674 '
      '2.38908,1.72327 4.97398,1.72327 1.21412,0 2.27158,-0.31332 '
      '1.09663,-0.31332 1.56661,-0.62664 z')
BAR_PATH = ('m 12.5,50 q -1.879598,0 -2.192865,-1.13559 '
            '-0.195791,-0.587375 -0.195791,-1.566332 0,-0.978958 '
            '0.156633,-1.566332 0.195792,-0.587375 0.587375,-0.822324 '
            '0.665691,-0.313267 1.683806,-0.313267 h 26.353535 '
            'q 1.879599,0 2.192865,1.174749 0.19579,0.587375 0.19579,1.527174 '
            '0,0.978957 -0.19579,1.566332 -0.156633,0.587374 '
            '-0.548216,0.822324 -0.587375,0.313266 -1.683807,0.313266 z')


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
        self.fill = 'white'

    def to_element(self) -> ET.Element:
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
                                            'fill': self.fill}))
        elif not self.has_border:
            group.append(ET.Element('rect',
                                    attrib={'x': str(x),
                                            'y': str(y),
                                            'width': str(rect_width),
                                            'height': str(rect_height),
                                            'fill': self.fill}))
        else:
            for layer in range(4):
                stroke_width = '4' if layer == 0 else '2'
                stroke = '#' + ('bcde'[layer]) * 6
                group.append(ET.Element(
                    'rect',
                    {'fill': self.fill,
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
        self.add_symbols(group)
        return group

    def add_symbols(self, group: ET.Element) -> None:
        if self.pips:
            pips = SvgPips(self.pips)
            pips.x = self.BASE_WIDTH / 2
            pips.y = self.BASE_HEIGHT / 2
            pips.scale = 0.75
            group.append(pips.to_element())
        lower_symbol = self.symbol.lower()
        path_points = LETTER_PATHS[lower_symbol]
        letter_path = ET.Element('path', dict(d=path_points))
        letter_path.attrib['transform'] = f'scale({LETTER_SCALE})'
        group.append(letter_path)
        bar_path = deepcopy(letter_path)
        bar_path.attrib['d'] = BAR_PATH
        if lower_symbol != self.symbol:
            bar_path.attrib['fill'] = 'transparent'
        bar_path.attrib['stroke'] = 'black'
        bar_path.attrib['stroke-width'] = str(self.rect_width * 0.0117)
        group.append(bar_path)
        letter_path = deepcopy(letter_path)
        letter_path.attrib['transform'] = (
            f'translate({self.rect_width} {self.rect_height}) '
            f'rotate(180) '
            f'scale({LETTER_SCALE}) ')
        group.append(letter_path)
        bar_path = deepcopy(bar_path)
        bar_path.attrib['transform'] = letter_path.attrib['transform']
        group.append(bar_path)
        symbol_size = SvgSymbol.BASE_SIZE / 2
        symbol1 = SvgSymbol(self.symbol)
        symbol1.scale = 1.75
        symbol1.x = self.BASE_WIDTH / 2
        symbol1.y = self.BASE_HEIGHT / 2 - symbol_size * 2
        group.append(symbol1.to_element())
        symbol2 = deepcopy(symbol1)
        symbol2.y = self.BASE_HEIGHT / 2 + symbol_size * 2
        symbol2.rotation = 180
        group.append(symbol2.to_element())


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
                                 fill=SQUARE_LIGHT,
                                 stroke='black'))
        board.append(border)
        steps = 50
        for i in range(-rows//2, -rows//2 + rows):
            for j in range(-columns//2, -columns//2 + columns):
                if i % 2 != j % 2:
                    continue
                x0 = j * size + xc
                y0 = i * size + yc
                if j == columns//2 - 1 and i == -rows//2:
                    x1, y1 = self.convert_coordinates(x0, y0)
                    board.append(ET.Element(
                        'path',
                        {
                            'd': f'M {x1},{y1} '
                                 f'l {-size * 2 / 3},0 '
                                 f'a {size / 3} {size / 3} 0 0 1 '
                                 f'{-size / 3},{-size / 3} '
                                 f'l 0,{-size * 2 / 3}, '
                                 f'l {size},0',
                            'fill': SQUARE_DARK}))
                    continue
                if j == columns//2 - 1 and i == -rows//2 + rows - 1:
                    x1, y1 = self.convert_coordinates(x0, y0)
                    board.append(ET.Element(
                        'path',
                        {
                            'd': f'M {x1},{y1} '
                                 f'l {-size},0 '
                                 f'l 0,{-size * 2 / 3}, '
                                 f'a {size / 3} {size / 3} 0 0 1 '
                                 f'{size / 3},{-size / 3} '
                                 f'l {size * 2 / 3},0',
                            'fill': SQUARE_DARK}))
                    continue
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
                                         'fill': SQUARE_DARK}))
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


class SvgCheckers(SvgCard):
    def __init__(self, white_count: str, black_count: str) -> None:
        super().__init__(symbol='p', has_border=False, has_outline=True)
        self.white_count = white_count
        self.black_count = black_count
        self.fill = '#ffce9e'
    
    def add_symbols(self, group: ET.Element) -> None:
        circle = ET.SubElement(group,
                               'circle',
                               attrib={'cx': '88',
                                       'cy': '88',
                                       'r': '40.5',
                                       'fill': 'none',
                                       'stroke': 'black',
                                       'stroke-width': '9'})
        circle2 = deepcopy(circle)
        circle2.set('cy', '178')
        circle2.set('stroke', 'white')
        group.append(circle2)
        count = ET.SubElement(group,
                              'text',
                              attrib={'x': '88',
                                      'y': '190',
                                      'text-anchor': 'middle',
                                      'font-family': 'Raleway',
                                      'font-size': '50'})
        count.text = self.white_count
        count2 = deepcopy(count)
        count2.set('y', '100')
        count2.text = self.black_count
        group.append(count2)


class SvgAid(SvgCard):
    def __init__(self,
                 game_name: str,
                 markdown_states: list[ParsingState],
                 has_border: bool = True) -> None:
        super().__init__(symbol='p', has_border=has_border, has_outline=False)
        self.game_name = game_name
        self.markdown_states = markdown_states

    def to_element(self) -> ET.Element:
        if self.game_name == 'Blank':
            return ET.Element('g')
        return super().to_element()

    def add_symbols(self, group: ET.Element) -> None:
        title = ET.Element('text',
                           attrib={'x': '85.5',
                                   'y': '32',
                                   'text-anchor': 'middle',
                                   'font-family': 'FredokaOne',
                                   'font-size': '16'})
        title.text = self.game_name
        group.append(title)

        y = 55
        x = 15
        line_height = 12
        text_attrib = {'font-family': 'Raleway',
                       'font-size': '11'}
        for state in self.markdown_states:
            if state.raw_text == '4 q k 2\n3 Q K 1\n\n':
                self.add_diagram(group, y-line_height*2.583)
                y += line_height*4
                continue
            lines = state.raw_text.split('\n')
            for line_text in lines:
                stripped_line = line_text.lstrip(' ')
                indent = (len(line_text) - len(stripped_line)) * 3
                text_attrib['x'] = str(x + indent)
                text_attrib['y'] = str(y)
                line = ET.Element('text',
                                  attrib=text_attrib)
                line.text = stripped_line
                group.append(line)
                y += line_height

    @staticmethod
    def add_diagram(group: ET.Element, y: float) -> None:
        square_dark = chess.svg.DEFAULT_COLORS['square dark']
        square_light = chess.svg.DEFAULT_COLORS['square light']
        group.append(ET.Element('rect',
                                {
                                    'x': '55.5',
                                    'y': str(y),
                                    'width': '60',
                                    'height': '60',
                                    'fill': square_light}))
        group.append(ET.Element('rect',
                                {
                                    'x': '85.5',
                                    'y': str(y),
                                    'width': '30',
                                    'height': '30',
                                    'fill': square_dark}))
        group.append(ET.Element('rect',
                                {
                                    'x': '55.5',
                                    'y': str(y+30),
                                    'width': '30',
                                    'height': '30',
                                    'fill': square_dark}))
        group.append(ET.Element('rect',
                                {
                                    'x': '55.5',
                                    'y': str(y),
                                    'width': '60',
                                    'height': '60',
                                    'fill': 'transparent',
                                    'stroke': 'black',
                                    'stroke-width': '2'}))
        for i, letter in enumerate('qkQK'):
            symbol = SvgSymbol(letter)
            symbol.x = 70.5 + 30 * (i % 2)
            symbol.y = 75 + 30 * (i // 2)
            symbol.scale = 0.65
            group.append(symbol.to_element())
        for i, turn_str in enumerate('4231'):
            turn_text = ET.Element('text',
                                   {
                                       'x': str(40.5 + 90 * (i % 2)),
                                       'y': str(75 + 30 * (i // 2)),
                                       'dominant-baseline': 'middle',
                                       'text-anchor': 'middle',
                                       'font-family': 'Raleway',
                                       'font-size': '11'})
            turn_text.text = turn_str
            group.append(turn_text)


class SvgGrid(SvgGroup):
    def __init__(
            self,
            symbols: list[str] | list[list[str]] | list[list[SvgCard]]) -> None:
        super().__init__()
        self.symbols = symbols
        self.base_width = SvgCard.BASE_WIDTH * len(symbols[0])
        self.base_height = SvgCard.BASE_HEIGHT * len(symbols)

    def to_element(self) -> ET.Element:
        group = super().to_element()
        for i, row in enumerate(self.symbols):
            for j, symbol in enumerate(row):
                if isinstance(symbol, SvgCard):
                    card = symbol
                else:
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


def parse_player_aids(markdown):
    states = parse(markdown)
    player_aids = []
    end = len(states)
    for start, state in reversed(list(enumerate(states))):
        if state.style.startswith('Heading'):
            game_name = state.text
            aid_states = states[start+1:end]
            player_aids.append((game_name, aid_states))
            end = start
    player_aids.reverse()
    return player_aids
