from textwrap import dedent

import pytest
from chess import Board

from board_parser import parse_board


@pytest.mark.parametrize('fen', ['qk6/8/8/8/8/8/8/QK6 w - - 0 1',
                                 'qkk5/8/8/8/8/8/8/QKK5 w - - 0 1'])
def test_parse_board(fen: str):
    board1 = Board(fen)
    board_text = str(board1)
    board2 = parse_board(board_text)
    fen2 = board2.fen()

    assert fen2 == fen


def test_trailing_newline():
    board_text = dedent("""\
        . . q k r . . .
        . . p p p . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . P P P . . .
        . . Q K R . . .
        """)
    board = parse_board(board_text)
    board_text2 = str(board)

    assert board_text2 == board_text.strip()
