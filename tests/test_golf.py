from collections import Counter
from textwrap import dedent

import chess
import pytest

from board_parser import parse_board
from golf import get_neighbour_types, GolfState


def test_get_neighbour_types():
    board = parse_board(dedent("""\
        . . B . . . R .
        . . . . . . . .
        . r . n . Q . .
        . r . . b k . .
        R . . . . . q .
        . B . n . N . .
        b . . . . . . K
        . . . . . N . ."""))
    expected_neighbour_types = {chess.KNIGHT, chess.KING}

    neighbour_types = get_neighbour_types(board, chess.E5)

    assert board.piece_at(chess.E5) == chess.Piece(chess.BISHOP, chess.BLACK)
    assert neighbour_types == expected_neighbour_types


def test_new_golf_state():
    start_text = dedent("""\
        . . B . . . R .
        . . . . . . . .
        . r . n . Q . .
        . r . . b k . .
        R . . . . . q .
        . B . n . N . .
        b . . . . . . K
        . . . . . N . .
        chosen: Bbq""")
    expected_board = parse_board(start_text.split('chosen')[0])

    state = GolfState(start_text)

    assert state.board == expected_board
    assert state.taking is None
    assert state.taken == Counter()
    assert state.chosen == Counter([chess.Piece(chess.BISHOP, chess.WHITE),
                                    chess.Piece(chess.BISHOP, chess.BLACK),
                                    chess.Piece(chess.QUEEN, chess.BLACK)])


def test_captured_golf_state():
    start_text = dedent("""\
        . . B . . . R .
        . . . . . . . .
        . r . n . Q . .
        . r . . b k . .
        R . . . . . q .
        . . . n . N . .
        B . . . . . . K
        . . . . . N . .
        chosen: Bbq
        taking: a2
        taken: b""")

    state = GolfState(start_text)

    assert state.taking == chess.A2
    assert state.taken == Counter([chess.Piece(chess.BISHOP, chess.BLACK)])
    assert state.chosen == Counter([chess.Piece(chess.BISHOP, chess.WHITE),
                                    chess.Piece(chess.BISHOP, chess.BLACK),
                                    chess.Piece(chess.QUEEN, chess.BLACK)])


def test_bogus_golf_state():
    start_text = dedent("""\
        . . B . . . R .
        . . . . . . . .
        . r . n . Q . .
        . r . . b k . .
        R . . . . . q .
        . . . n . N . .
        B . . . . . . K
        . . . . . N . .
        bogus: Bbq""")

    with pytest.raises(ValueError, match=r"Unknown golf label: 'bogus'."):
        GolfState(start_text)


def test_find_moves_not_chosen_taker():
    state = GolfState(dedent("""\
        n k . . . . R N
        . . . B r . n .
        . . q . . B . .
        . . . . . . . b
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        chosen: Bb"""))

    expected_moves = {chess.Move(chess.A8, chess.A7),  # knight uses king
                      chess.Move(chess.A8, chess.B7),
                      chess.Move(chess.B8, chess.A6),  # king uses knight
                      chess.Move(chess.G8, chess.H6),  # rook uses knight
                      chess.Move(chess.H8, chess.H7),  # knight uses rook
                      chess.Move(chess.H8, chess.H6)}

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves


# noinspection DuplicatedCode
def test_find_moves_not_chosen_taken():
    state = GolfState(dedent("""\
        . . . . . . R B
        . . . . . b . .
        . . . . . . . .
        . . . . . . . n
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        chosen: Bb"""))

    expected_moves = {chess.Move(chess.H8, chess.H7),  # bishop uses rook
                      chess.Move(chess.H8, chess.H6),
                      chess.Move(chess.G8, chess.H7)}  # rook uses bishop

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves


# noinspection DuplicatedCode
def test_find_moves_both_chosen():
    state = GolfState(dedent("""\
        . . . . . . R B
        . . . . . n . .
        . . . . . . . .
        . . . . . . . b
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        chosen: Bb"""))

    expected_moves = {chess.Move(chess.H8, chess.H7),  # bishop uses rook
                      chess.Move(chess.H8, chess.H6),
                      chess.Move(chess.H8, chess.H5),
                      chess.Move(chess.G8, chess.H7)}  # rook uses bishop

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves


# noinspection DuplicatedCode
def test_find_moves_same_type_not_allowed():
    state = GolfState(dedent("""\
        . . . . . . R B
        . . . . . b . .
        . . . . . . . .
        . . . . . . . B
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        chosen: Bb"""))

    expected_moves = {chess.Move(chess.H8, chess.H7),  # bishop uses rook
                      chess.Move(chess.H8, chess.H6),
                      chess.Move(chess.G8, chess.H7)}  # rook uses bishop

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves


# noinspection DuplicatedCode
def test_find_moves_same_type_allowed():
    state = GolfState(dedent("""\
        . . . . . . R B
        . . . . . b . .
        . . . . . . . .
        . . . . . . . B
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        chosen: BB"""))

    expected_moves = {chess.Move(chess.H8, chess.H7),  # bishop uses rook
                      chess.Move(chess.H8, chess.H6),
                      chess.Move(chess.H8, chess.H5),
                      chess.Move(chess.G8, chess.H7)}  # rook uses bishop

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves


# noinspection DuplicatedCode
def test_find_moves_single_piece_may_capture():
    state = GolfState(dedent("""\
        B R . . . . R B
        n . q . . k . n
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        chosen: Bbn
        taking: a8
        taken: b"""))

    expected_moves = {chess.Move(chess.A8, chess.A7)}  # bishop uses rook

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves


# noinspection DuplicatedCode
def test_find_moves():
    state = GolfState(dedent("""\
        B R . . . . . .
        r . . . . . . .
        . . . k . . . .
        . . . . . . . .
        . . . . . q . .
        . . . . K . . .
        . . . . . . b .
        . . . . Q . . n
        chosen: Bbr
        taking: a8
        taken: r"""))

    expected_moves = {chess.Move(chess.B8, chess.C7),  # rook uses bishop
                      chess.Move(chess.G2, chess.H4)}  # bishop uses knight

    moves = list(state.find_moves())

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves
