import chess.svg
from svgwrite import Drawing

from board_parser import parse_board
from svg_diagram import SvgDiagram


class Diagram:
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
        lines = self.board_state.splitlines()
        board = parse_board('\n'.join(lines[:8]))
        arrows = []
        for line in lines[8:]:
            command, body = line.split(':', maxsplit=1)
            fields = [field.strip() for field in body.split(',')]
            tail = getattr(chess, fields[0].upper())
            head = getattr(chess, fields[1].upper())
            colour = fields[2]
            arrows.append(chess.svg.Arrow(tail, head, color=colour))
        size = round(min(self.page_width/2, self.page_height))
        svg_text = chess.svg.board(board, size=size, arrows=arrows)

        diagram = SvgDiagram(svg_text)
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
