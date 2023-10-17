from functools import partial
import math


def draw_diagram(turtle,
                 state,
                 cell_size=DEFAULT_CELL_SIZE,
                 solution=False,
                 show_path=False,
                 board_class=Board):
    marks = {'>': partial(draw_arrow, turtle, cell_size),
             '^': partial(draw_arrow, turtle, cell_size, 90),
             '<': partial(draw_arrow, turtle, cell_size, 180),
             'v': partial(draw_arrow, turtle, cell_size, 270),
             '+': partial(draw_cross, turtle, cell_size, 0),
             '*': partial(draw_cross, turtle, cell_size, 45)}
    pos = turtle.pos()
    sections = state.split('\n---\n')
    lines = sections[0].splitlines()
    turtle.up()
    turtle.forward(cell_size*0.5)
    turtle.right(90)
    turtle.forward(cell_size*len(lines)*0.5)
    turtle.left(90)
    origin = turtle.pos()
    board = board_class.create(state)
    draw_board(turtle, board, cell_size)
    turtle.up()
    turtle.pencolor('white')
    for y, line in enumerate(reversed(lines)):
        for x, c in enumerate(line):
            if (x+y) % 2:
                mark = marks.get(c)
                if mark is not None:
                    mark()
                    turtle.up()
            turtle.forward(cell_size*.5)
        turtle.back(cell_size*len(line)*.5)
        turtle.left(90)
        turtle.forward(cell_size*.5)
        turtle.right(90)
    turtle.setpos(pos)
    draw_dominosa_hints(turtle, board, cell_size)
    draw_dice(turtle, board, cell_size)
    draw_arrows(turtle, board, cell_size)
    if show_path:
        draw_paths(turtle, board, cell_size)
    if solution:
        border = 1
        offset = [border, border]
        board = Board.create(state, border=border)
        for cell in board.findMatches():
            turtle.setpos(origin)
            draw_match(turtle,
                       cell_size,
                       offset,
                       cell)
        graph = CaptureBoardGraph()
        graph.walk(board)
        solution = graph.get_solution(return_partial=True)
        step_count = max(len(solution)-1, 1)
        for move_num, move in enumerate(solution, 1):
            domino_name = move[:2]
            for domino in board.dominoes:
                if domino.get_name() == domino_name:
                    dx, dy = Domino.get_direction(move[-1])
                    turtle.setpos(origin)
                    draw_move(turtle,
                              cell_size,
                              offset,
                              domino,
                              dx,
                              dy,
                              move_num,
                              step_count)
                    old_offset = offset[:]
                    state = graph.move(domino, dx, dy, offset)
                    new_board = Board.create(state, border=border)
                    captures = set(board.dominoes)
                    captures.difference_update(new_board.dominoes)
                    captures.discard(domino)
                    for capture in captures:
                        turtle.setpos(origin)
                        draw_capture_circle(turtle,
                                            cell_size,
                                            old_offset,
                                            capture,
                                            move_num)
                    offset[0] += border
                    offset[1] += border
                    board = new_board
                    break
        # Mark uncaptured dominoes
        for domino in board.dominoes:
            turtle.setpos(origin)
            draw_capture_circle(turtle, cell_size, offset, domino)
        turtle.setpos(pos)


def draw_dominosa_hints(turtle, board, cell_size):
    if not hasattr(board, 'get_pair_state'):
        return
    old_color = turtle.pencolor()
    old_size = turtle.pensize()
    turtle.pencolor('black')
    turtle.pensize(cell_size*0.05)
    turtle.up()

    # Draw splits between cells in the same row.
    for x in range(1, board.width):
        turtle.forward(cell_size)
        turtle.right(90)
        for y in reversed(range(board.height)):
            pair_state = board.get_pair_state(x-1, y, x, y)
            if pair_state != PairState.SPLIT:
                turtle.forward(cell_size)
            else:
                draw_split(turtle, cell_size)
        turtle.back(cell_size*board.height)
        turtle.left(90)
    turtle.back(cell_size*(board.width-1))

    # Draw splits between cells in the same column.
    turtle.right(90)
    for y in reversed(range(1, board.height)):
        turtle.forward(cell_size)
        turtle.left(90)
        for x in range(board.width):
            try:
                pair_state = board.get_pair_state(x, y-1, x, y)
            except KeyError:
                pair_state = PairState.UNDECIDED
            if pair_state != PairState.SPLIT:
                turtle.forward(cell_size)
            else:
                draw_split(turtle, cell_size)
        turtle.back(cell_size * board.width)
        turtle.right(90)
    turtle.back(cell_size*board.width)

    turtle.pencolor(old_color)
    turtle.pensize(old_size)


def draw_split(turtle, cell_size):
    turtle.forward(0.15 * cell_size)
    turtle.down()
    turtle.forward(0.7 * cell_size)
    turtle.up()
    turtle.forward(0.15 * cell_size)


def draw_joined_block(turtle, width, height):
    turtle.down()
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()


def draw_dice(turtle: Turtle, board: Board, cell_size: int):
    dice_set = board.dice_set
    if dice_set is None:
        return
    turtle.color('black', 'white')
    turtle.right(90)
    turtle.forward(int(cell_size * (board.height-0.5)))
    turtle.left(90)
    turtle.forward(cell_size/2)
    die_size = cell_size * 0.6
    for y in range(board.height):
        for x in range(board.width):
            die_pips = dice_set[x, y]
            if die_pips is not None:
                draw_die_outline(turtle, die_size)
                cell = board[x][y]
                if cell is None or cell.domino is None:
                    dy = 0
                else:
                    dx, dy = cell.domino.direction
                if dy:
                    turtle.left(90)
                draw_pips(turtle, die_pips, die_size)
                if dy:
                    turtle.right(90)
            turtle.forward(cell_size)
        turtle.back(cell_size*board.width)
        turtle.left(90)
        turtle.forward(cell_size)
        turtle.right(90)
    turtle.right(90)
    turtle.forward(cell_size / 2)
    turtle.left(90)
    turtle.back(cell_size / 2)


def draw_arrows(turtle: Turtle, board: Board, cell_size: int):
    arrows = board.arrows
    if arrows is None:
        return
    start_pos = turtle.pos()
    turtle.up()
    line_width = cell_size * 0.05
    outline_width = cell_size * 0.07
    turtle.right(90)
    turtle.forward(cell_size * (board.height - 0.5))
    turtle.left(90)
    turtle.forward(cell_size / 2)
    x0, y0 = turtle.pos()

    for arrow in arrows.positions:
        for colour, width in (('white', outline_width),
                              ('grey50', line_width)):
            turtle.color(colour)
            x2, y2 = arrow[0]
            x = x0 + x2*cell_size
            y = y0 + y2*cell_size
            turtle.goto(x, y)
            turtle.down()
            # noinspection PyTypeChecker
            turtle.width(width)
            for x2, y2 in arrow[1:-1]:
                x = x0 + x2*cell_size
                y = y0 + y2*cell_size
                turtle.goto(x, y)
            x2, y2 = arrow[-1]
            x = x0 + x2*cell_size
            y = y0 + y2*cell_size
            turtle.setheading(turtle.towards(x, y))
            distance = max(abs(x - turtle.xcor()), abs(y - turtle.ycor()))
            turtle.forward(distance - line_width)
            turtle.up()
            turtle.forward(width + (width-line_width)/2)
            turtle.right(150)
            turtle.width(cell_size//100)
            turtle.down()
            turtle.begin_fill()
            for _ in range(3):
                turtle.forward(width*3)
                turtle.right(120)
            turtle.end_fill()
            turtle.up()
            turtle.goto(x0, y0)
            turtle.setheading(0)
    turtle.goto(start_pos)


def draw_demo(turtle):
    width = turtle.getscreen().window_width()
    height = turtle.getscreen().window_height()
    cell_size = min(width/8.2, height/7.2)
    turtle.up()
    turtle.back(cell_size*4)
    turtle.left(90)
    turtle.forward(cell_size*3.5)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor('ivory')
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(cell_size*8)
        turtle.right(90)
        turtle.forward(cell_size*7)
        turtle.right(90)
    turtle.end_fill()
    turtle.fillcolor('black')

    demo_state = """\
5 5 5 5 6 6 6 6
- - - - - - - -
1 2 3 4 4 3 2 1

1|2 3     0
    v     *
    4 5+6 6

2|2
---
(0,4)F,(4,1)G
"""
    mountain_state = """\
0|1 2|1 0|4

2 1|5 4|1 4
-         -
0 0|6 4|2 4

0|3 3|3 4|5

1 2 3|6 5|5
- -
3 2 1|6 5|6
"""
    dominosa_state = """\
0 1 2 3
  -
4 5 6 0

1|2 3 4
"""

    demo_type = 'demo'
    if demo_type == 'mountains':
        draw_diagram(turtle, mountain_state, cell_size, show_path=True)
    elif demo_type == 'dominosa':
        draw_diagram(turtle, dominosa_state, cell_size)
    else:
        draw_fuji(turtle, 8, cell_size)
        draw_diagram(turtle, demo_state, cell_size, solution=False)


if __name__ == '__live_coding__':
    from turtle import Turtle
    t = Turtle()
    draw_demo(t)
