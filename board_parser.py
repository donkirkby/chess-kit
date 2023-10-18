from itertools import groupby

from chess import Board


def parse_board(board_text: str) -> Board:
    condensed = board_text.strip().replace(' ', '')
    chunks = []
    for c, span in groupby(condensed):
        span_text = ''.join(span)
        if c == '.':
            chunks.append(str(len(span_text)))
        elif c == '\n':
            chunks.append('/')
        else:
            chunks.append(span_text)

    fen = ''.join(chunks)
    return Board(fen)
