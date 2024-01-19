# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from copy import deepcopy

import chess.svg

from diagram import Diagram


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
                        f'translate(-22.5 -22.5)')
        return piece_group


class SvgCard:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.x = self.y = 0
        self.width = 170
        self.height = 220

    def to_element(self) -> ET.Element:
        symbol_size = 22.5
        group = ET.Element('g')
        group.append(ET.Element('rect',
                                {'width': str(self.width),
                                 'height': str(self.height),
                                 'fill': '',
                                 'stroke': 'black',
                                 'stroke-width': '4'}))
        symbol1 = SvgSymbol(self.symbol)
        symbol1.scale = 0.75
        symbol1.x = symbol_size
        symbol1.y = symbol_size
        group.append(symbol1.to_element())
        symbol2 = deepcopy(symbol1)
        symbol2.rotation = 180
        symbol2.x = self.width - symbol_size
        symbol2.y = self.height - symbol_size
        group.append(symbol2.to_element())
        symbol3 = deepcopy(symbol1)
        symbol3.scale = 2
        symbol3.x = self.width / 2
        symbol3.y = self.height / 2 - symbol_size*2
        group.append(symbol3.to_element())
        symbol4 = deepcopy(symbol3)
        symbol4.y = self.height / 2 + symbol_size*2
        symbol4.rotation = 180
        group.append(symbol4.to_element())
        return group
