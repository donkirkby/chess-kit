import chess.svg

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
