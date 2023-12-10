import copy
import xml.etree.ElementTree as ET  # noqa
from pathlib import Path

import chess.svg
from svgwrite import Drawing

from board_parser import parse_board
from svg_diagram import SvgDiagram


class Diagram:
    CARDS_PATH = Path(__file__).parent / 'English_pattern_playing_cards_deck.svg'
    CARD_BACK_PATH = Path(__file__).parent / 'Atlas_deck_card_back_blue_and_brown.svg'

    @staticmethod
    def register_svg():
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

    def __init__(self,
                 page_width: float,
                 page_height: float,
                 board_state: str):
        self.page_width = page_width
        self.page_height = page_height
        self.board_state = board_state

    def build(self) -> SvgDiagram:
        if self.board_state.startswith('type: '):
            return self.build_grid()
        self.register_svg()
        lines = self.board_state.splitlines()
        board = parse_board('\n'.join(lines[:8]))
        arrows = []
        square_size = 45
        x0 = 15 - 0.5*square_size
        y0 = 9.112 * square_size
        drawing = Drawing()
        extra_svg = []
        text_args = dict(text_anchor='middle',
                         font_family='Raleway',
                         font_size=round(0.55*square_size))
        corner_text_args = dict(text_anchor='middle',
                                font_family='Raleway',
                                font_size=round(0.375*square_size))
        _, card_map = ET.XMLID(self.CARDS_PATH.read_text())
        _, card_backs = ET.XMLID(self.CARD_BACK_PATH.read_text())
        card_back_svg = card_backs['card-back']
        margins = (0, 0, 0, 0)
        for line in lines[8:]:
            command, body = line.split(':', maxsplit=1)
            fields = [field.strip() for field in body.split(',')]
            if command == 'text':
                x = round(x0 + float(fields[1]) * square_size, 1)
                y = round(y0 - float(fields[2]) * square_size, 1)
                extra_svg.append(drawing.text(fields[0],
                                              (x, y),
                                              **text_args))
            elif command == 'corner text':
                x = round(x0 + (float(fields[1]) - 0.344) * square_size, 1)
                y = round(y0 - (float(fields[2]) + 0.445) * square_size, 1)
                extra_svg.append(drawing.text(fields[0],
                                              (x, y),
                                              **corner_text_args))
            elif command == 'rect':
                x1, y1, x2, y2 = [float(field) for field in fields]
                left = round(15 + (x1-1)*square_size, 1)
                top = round(15 + (8 - y2) * square_size, 1)
                width = round((x2-x1+1)*square_size, 1)
                height = round((y2-y1+1)*square_size, 1)
                extra_svg.append(drawing.rect((left, top),
                                              (width, height),
                                              fill_opacity=0,
                                              stroke='blue',
                                              stroke_width=5,
                                              stroke_dasharray='7.5'))
            elif command == 'margins':
                margins = tuple(float(n) for n in fields[:4])
                if len(margins) == 2:
                    margins *= 2
            elif command == 'arrow':
                tail = getattr(chess, fields[0].upper())
                head = getattr(chess, fields[1].upper())
                colour = fields[2]
                arrows.append(chess.svg.Arrow(tail, head, color=colour))
            elif command == 'card':
                card, x, y = fields
                x = float(x)
                y = float(y)
                if card == 'back':
                    card_svg = card_back_svg
                else:
                    card_svg = card_map[f'card-{card}']
                # copy, then modify
                card_svg = copy.deepcopy(card_svg)
                x = 180*x + 60
                y = 180*y - 453
                card_svg.attrib['transform'] = f'scale(0.25), translate({x}, {y})'
                extra_svg.append(card_svg)
            else:
                raise ValueError(f'Unknown diagram command: {command}.')
        original_view_size = 390  # chess library always uses this size
        view_width = original_view_size + (margins[0] + margins[2])*square_size
        view_height = original_view_size + (margins[1] + margins[3])*square_size
        x_aspect = self.page_width/2/view_width
        y_aspect = self.page_height/view_height
        aspect = min(x_aspect, y_aspect)
        image_width = view_width * aspect
        image_height = view_height * aspect
        board_size = round(original_view_size * aspect)
        view_box = (f'{-square_size*margins[0]} {-square_size*margins[1]} '
                    f'{view_width} {view_height}')
        svg_text = chess.svg.board(board, size=board_size, arrows=arrows)
        board_tree = ET.fromstring(svg_text)
        board_tree.set('viewBox', view_box)
        board_tree.set('width', str(image_width))
        board_tree.set('height', str(image_height))
        extra_elements = []
        for extra in extra_svg:
            if not isinstance(extra, ET.Element):
                extra = extra.get_xml()
            extra_elements.append(extra)
        board_tree.extend(extra_elements)

        diagram = SvgDiagram(ET.tostring(board_tree, encoding='unicode'))
        return diagram

    def build_grid(self):
        lines = self.board_state.splitlines()
        header = lines.pop(0)
        rows = [line.split() for line in lines]
        column_count = max(len(row) for row in rows)
        grid_type = header.split(':', maxsplit=1)[1].strip()
        raw_width = self.page_width / 2
        if grid_type == 'masquerade':
            cell_width = round(raw_width / (column_count + 0.5))
        else:
            cell_width = round(raw_width / column_count)
        cell_height = round(self.page_height / len(rows))
        cell_size = min(cell_width, cell_height)
        width = cell_size * column_count
        if grid_type == 'masquerade':
            width += round(cell_size / 2)
        height = cell_size * len(rows)
        drawing = Drawing(size=(width, height))
        text_args = dict(text_anchor='middle',
                         font_family='FredokaOne',
                         font_size=round(cell_size*.25))
        for j in range(column_count):
            drawing.add(drawing.line((cell_size * j, 0),
                                     (cell_size * j, height),
                                     stroke='black'))
        drawing.add(drawing.line((width, 0), (width, height), stroke='black'))
        for i in range(len(rows) + 1):
            drawing.add(drawing.line((0, cell_size * i),
                                     (width, cell_size * i),
                                     stroke='black'))
        if grid_type == 'masquerade':
            drawing.add(drawing.line((0, 0), (cell_size, cell_size), stroke='black'))
            x = round(cell_size*.37)
            y = round(cell_size*.75)
            drawing.add(drawing.text('mv', (x, y), **text_args))
            x = round(cell_size*.67)
            y = round(cell_size*.37)
            drawing.add(drawing.text('cap', (x, y), **text_args))

        for i, row in enumerate(rows):
            if i != 0 and grid_type == 'masquerade':
                dx = round(cell_size*0.25)
                dy = round(cell_size*0.2)
                drawing.add(drawing.line((6*cell_size+dx, cell_size*(i+1) - dy),
                                         (width-dx, cell_size*(i+1) - dy),
                                         stroke='black'))
            for j, cell in enumerate(row):
                if cell in '._':
                    continue
                text_args['font_size'] = round(cell_size * .63)
                y = round(cell_size * .75) + cell_size*i
                if j != 6 or grid_type != 'masquerade':
                    x = round(cell_size * (j + 0.5))
                else:
                    x = round(cell_size * (j + 0.75))
                    if i == 0:
                        text_args['font_size'] = round(cell_size*.37)
                drawing.add(drawing.text(cell, (x, y), **text_args))

        diagram = SvgDiagram(drawing.tostring())
        return diagram
