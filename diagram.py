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
        if self.board_state.startswith('type: masquerade'):
            return self.build_masquerade()
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

    def build_masquerade(self):
        raw_width = round(min(self.page_width / 2, self.page_height))
        cell_size = round(raw_width / 7.5)
        width = round(cell_size * 7.5)
        height = cell_size * 6
        drawing = Drawing(size=(width, height))
        text_args = dict(text_anchor='middle',
                         font_family='FredokaOne',
                         font_size=round(cell_size*.25))
        for i in range(7):
            drawing.add(drawing.line((cell_size * i, 0),
                                     (cell_size * i, height),
                                     stroke='black'))
            drawing.add(drawing.line((0, cell_size * i),
                                     (width, cell_size * i),
                                     stroke='black'))
        drawing.add(drawing.line((width, 0), (width, height), stroke='black'))
        drawing.add(drawing.line((0, 0), (cell_size, cell_size), stroke='black'))
        x = round(cell_size*.37)
        y = round(cell_size*.75)
        drawing.add(drawing.text('mv', (x, y), **text_args))
        x = round(cell_size*.67)
        y = round(cell_size*.37)
        drawing.add(drawing.text('cap', (x, y), **text_args))

        for i, line in enumerate(self.board_state.splitlines()[1:]):
            if i != 0:
                dx = round(cell_size*0.25)
                dy = round(cell_size*0.2)
                drawing.add(drawing.line((6*cell_size+dx, cell_size*(i+1) - dy),
                                         (width-dx, cell_size*(i+1) - dy),
                                         stroke='black'))
            for j, cell in enumerate(line.split()):
                if cell in '._':
                    continue
                text_args['font_size'] = round(cell_size * .63)
                y = round(cell_size * .75) + cell_size*i
                if j != 6:
                    x = round(cell_size * (j + 0.5))
                else:
                    x = round(cell_size * (j + 0.75))
                    if i == 0:
                        text_args['font_size'] = round(cell_size*.37)
                drawing.add(drawing.text(cell, (x, y), **text_args))

        diagram = SvgDiagram(drawing.tostring())
        return diagram
