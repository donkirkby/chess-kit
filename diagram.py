import xml.etree.ElementTree as ET  # noqa
from pathlib import Path

import chess.svg
from svgwrite import Drawing

from board_parser import parse_board
from chess_deck import SvgCardBack, SvgCard, SvgSymbol
from svg_diagram import SvgDiagram
from svg_page import SvgPage

SUIT_PATHS = dict(
    c="""m 9.2604166,14.816667 c 0.529167,1.058333 1.8520834,2.645832
        3.1750004,2.645832 2.38125,0 3.439583,-2.116665 3.439583,-4.762499
        0,-2.645833 -1.058333,-5.0270835 -3.439583,-5.0270835 -1.322917,0
        -2.116667,1.3229167 -2.9104174,2.1166667 -0.264583,0.2645838
        -0.529166,0 -0.264583,-0.2645834 C 10.054167,8.7312498
        11.377084,6.6145832 11.377084,4.7624999 11.377084,2.6458333
        10.054167,0 7.9374996,0 5.8208333,0 4.4979166,2.6458333
        4.4979166,4.7624999 c 0,1.8520833 1.3229167,3.9687499
        2.116667,4.7624999 0.264583,0.2645834 0,0.5291672 -0.264584,0.2645834
        C 5.5562499,8.9958332 4.7624999,7.6729165 3.4395833,7.6729165
        1.0583333,7.6729165 0,10.054167 0,12.7 c 0,2.645834 1.0583333,4.7625
        3.4395833,4.7625 1.3229166,0 2.6458333,-1.5875 3.1750003,-2.645833
        0.264583,-0.264583 0.264583,0 0.264583,0.264583 -0.264583,2.116667
        -0.264583,2.645834 -0.529167,4.233334 -0.264583,1.5875
        -1.058333,4.497916 -1.058333,4.497916 1.322917,-0.529167
        3.96875,-0.529167 5.2916674,0 0,0 -0.7937504,-2.910416
        -1.0583344,-4.497916 -0.264583,-1.5875 -0.264583,-2.116667
        -0.529166,-4.233334 0,-0.264583 0,-0.529166 0.264583,-0.264583 z
        """,
    d="""m 7.9631905,1.5214548 c 0,0 1.4246819,3.4346511 3.0868115,5.7244194
        1.662128,2.2897674 4.036599,4.5795328 4.036599,4.5795328 0,0
        -2.374471,2.28977 -4.036599,4.579538 -1.6621296,2.289767
        -3.0868115,5.724419 -3.0868115,5.724419 0,0 -1.4246819,-3.434652
        -3.0868108,-5.724419 -1.6621289,-2.289768 -4.03659883,-4.579538
        -4.03659883,-4.579538 0,0 2.37446993,-2.2897654 4.03659883,-4.5795328
        C 6.5385086,4.9561059 7.9631905,1.5214548 7.9631905,1.5214548 Z
            """,
    h="""m 7.69329,5.0174806 c 0,-2.7038812 -1.395829,-4.4062308
        -3.4189167,-4.4062308 -2.0230879,0 -3.66312517,2.1919309
        -3.66312517,4.8958118 0.008523,0.2339194 0.004444,0.4629457
        0,0.6884736 0,1.7865994 0.65370917,3.519316 1.22104167,5.1406018
        0.5834211,1.66726 1.4246065,3.128588 2.2131382,4.620424
        1.221342,2.310677 3.8920704,6.685843 3.8920704,6.685843 0,0
        2.6707286,-4.375166 3.8920696,-6.685843 0.788532,-1.491836
        1.629718,-2.953164 2.213139,-4.620424 0.567333,-1.6212858
        1.221041,-3.3540024 1.221041,-5.1406018 -0.0069,-0.2385238
        -0.0045,-0.468681 0,-0.6884736 0,-2.7038809 -1.640037,-4.8958118
        -3.663124,-4.8958118 -2.0230887,0 -3.4189173,1.7023496
        -3.4189173,4.4062308 0,0.489581 -0.4884167,0.489581 -0.4884167,0 z
        """,
    s="""m 9.260417,14.816667 c 0.264583,1.058333 1.322917,3.704166
        3.175,3.704166 2.381251,0 3.439581,-2.116666 3.439581,-4.7625
        0,-1.852083 -0.68234,-3.072418 -1.322914,-4.497916
        C 13.870019,7.742574 12.864222,6.387727 11.90625,5.027084
        10.677181,3.281389 7.9375,0 7.9375,0 7.9375,0 5.197819,3.281389
        3.96875,5.027084 3.010779,6.387727 2.004981,7.742574
        1.322917,9.260417 0.682348,10.685915 0,11.90625 0,13.758333
        c 0,2.645834 1.058334,4.7625 3.439584,4.7625 1.852083,0
        2.910416,-2.645833 3.175,-3.704166 0.264583,-0.264584 0.264583,0
        0.264583,0.264583 C 6.614584,17.197917 6.614584,17.727083
        6.35,19.314583 6.085417,20.902083 5.291667,23.8125 5.291667,23.8125
        c 1.322917,-0.529167 3.96875,-0.529167 5.291667,0 0,0
        -0.79375,-2.910417 -1.058334,-4.497917 -0.264583,-1.5875
        -0.264583,-2.116666 -0.529166,-4.233333 0,-0.264583 0,-0.529167
        0.264583,-0.264583 z
        """)


class Diagram:
    CARDS_PATH = Path(__file__).parent / 'English_pattern_playing_cards_deck.svg'
    CARD_BACK_PATH = Path(__file__).parent / 'Atlas_deck_card_back_blue_and_brown.svg'

    def __init__(self,
                 page_width: float,
                 page_height: float,
                 board_state: str,
                 half_width: bool = True):
        self.page_width = page_width
        self.page_height = page_height
        self.board_state = board_state
        self.half_width = half_width

    def build(self) -> SvgDiagram:
        if self.board_state.startswith('type: '):
            return self.build_grid()
        SvgPage.register_svg()
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
        margins = [0, 0, 0, 0]
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
                margins = [float(n) for n in fields[:4]]
                if len(margins) == 2:
                    margins *= 2
            elif command == 'arrow':
                tail = parse_square(fields[0])
                head = parse_square(fields[1])
                colour = fields[2]
                arrows.append(chess.svg.Arrow(tail, head, color=colour))
            elif command == 'card':
                card, x, y = fields
                x = float(x)
                y = float(y)
                if card == 'back':
                    card_svg = SvgCardBack(has_outline=True)
                    card_svg.scale = 0.59
                else:
                    card_svg = SvgCard(card, has_border=False, has_outline=True)
                    card_svg.scale = 0.5
                card_svg.x = 45*x + 16
                card_svg.y = 45*y + 16
                extra_svg.append(card_svg.to_element())
            else:
                raise ValueError(f'Unknown diagram command: {command}.')
        original_view_size = 390  # chess library always uses this size
        if not self.half_width and (margins[0] + margins[2]) < 4:
            margins[2] = 4 - margins[0]
        view_width = original_view_size + (margins[0] + margins[2])*square_size
        view_height = original_view_size + (margins[1] + margins[3])*square_size
        x_aspect = self.page_width/view_width
        if self.half_width:
            x_aspect /= 2
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
        raw_width = self.page_width
        if self.half_width:
            raw_width /= 2
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
            if grid_type == 'cards' and 1 < j < column_count - 1:
                continue
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

        card_args = dict(text_anchor='end',
                         font_family='FredokaOne',
                         font_size=round(cell_size * .63))
        svg_page = SvgPage(width, height)

        for i, row in enumerate(rows):
            if i != 0 and grid_type == 'masquerade':
                dx = round(cell_size*0.25)
                dy = round(cell_size*0.2)
                drawing.add(drawing.line((6*cell_size+dx, cell_size*(i+1) - dy),
                                         (width-dx, cell_size*(i+1) - dy),
                                         stroke='black'))
            y = round(cell_size * .75) + cell_size*i
            if i == 0 and grid_type == 'cards':
                text_args['font_size'] = round(cell_size*.43)
                x = round(cell_size * column_count / 2)
                drawing.add(drawing.text('Cards', (x, y), **text_args))
                x = round(cell_size * (column_count - 0.5))
                drawing.add(drawing.text('Gap', (x, y), **text_args))
                continue
            for j, cell in enumerate(row):
                if cell in '._':
                    continue
                text_args['font_size'] = round(cell_size * .63)
                if j != 6 or grid_type != 'masquerade':
                    x = round(cell_size * (j + 0.5))
                else:
                    x = round(cell_size * (j + 0.75))
                    if i == 0:
                        text_args['font_size'] = round(cell_size*.37)
                if grid_type == 'cards' and j == 0:
                    svg_symbol = SvgSymbol(cell)
                    svg_symbol.x = x
                    svg_symbol.y = y - round(cell_size*0.232)
                    svg_symbol.scale = round(cell_size*0.014, 1)
                    svg_page.append(svg_symbol.to_element())
                elif grid_type != 'cards' or len(cell) < 2:
                    drawing.add(drawing.text(cell, (x, y), **text_args))
                else:
                    x += round(cell_size * 0.04)
                    rank = cell[:-1]
                    suit_letter = cell[-1].lower()
                    text = drawing.text(rank, (x, y), **card_args)
                    drawing.add(text)
                    suit_path = SUIT_PATHS[suit_letter]
                    path = drawing.path(suit_path)
                    if suit_letter in 'hd':
                        path.fill('none')
                        path.stroke('black', round(cell_size * 0.03))
                    path.translate(round(x + cell_size * 0.02),
                                   round(y - cell_size * 0.45))
                    path.scale(round(cell_size * 0.019, 1))
                    drawing.add(path)

        svg_page.append(drawing.get_xml())
        diagram = SvgDiagram(svg_page.to_svg())
        return diagram


def parse_square(text: str) -> int:
    file = ord(text[0].upper()) - 65
    rank = int(text[1:]) - 1
    return rank*8 + file
