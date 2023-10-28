import xml.etree.ElementTree as ET  # noqa

import chess.svg
from svgwrite import Drawing

from board_parser import parse_board
from svg_diagram import SvgDiagram


class Diagram:
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
        text_elements = Drawing()
        text_args = dict(text_anchor='middle',
                         font_family='Raleway',
                         font_size=round(0.55*square_size))
        margins = (0, 0)
        for line in lines[8:]:
            command, body = line.split(':', maxsplit=1)
            fields = [field.strip() for field in body.split(',')]
            if command == 'text':
                x = round(x0 + float(fields[1]) * square_size, 1)
                y = round(y0 - float(fields[2]) * square_size, 1)
                # fields[0] = str(y)
                text_elements.add(text_elements.text(fields[0],
                                                     (x, y),
                                                     **text_args))
            elif command == 'margins':
                margins = tuple(float(n) for n in fields[:2])
            else:
                tail = getattr(chess, fields[0].upper())
                head = getattr(chess, fields[1].upper())
                colour = fields[2]
                arrows.append(chess.svg.Arrow(tail, head, color=colour))
        original_view_size = 390  # chess library always uses this size
        view_width = original_view_size + 2*margins[0]*square_size
        view_height = original_view_size + 2*margins[1]*square_size
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
        board_tree.extend(text_elements.get_xml())

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
