import typing
from collections import Counter
from textwrap import dedent

import chess

from board_parser import parse_board


class GolfState:
    def __init__(self, text: str):
        board_lines = text.splitlines()
        board_text = '\n'.join(board_lines[:8])
        self.board = parse_board(board_text)
        self.taking = None
        self.taken = Counter()
        self.chosen = Counter()
        for line in board_lines[8:]:
            if line.startswith('chosen:'):
                chosen_text = line[7:].strip()
                self.chosen = Counter(chess.Piece.from_symbol(c)
                                      for c in chosen_text)
            elif line.startswith('taking:'):
                self.taking = chess.parse_square(line[7:].strip())
            elif line.startswith('taken:'):
                taken_text = line[6:].strip()
                self.taken = Counter(chess.Piece.from_symbol(c)
                                     for c in taken_text)
            else:
                label = line.split(':')[0]
                raise ValueError(f'Unknown golf label: {label!r}.')

    def find_moves(self):
        colour_move_counts = Counter()
        for square, piece in self.board.piece_map().items():
            for neighbour_type in get_neighbour_types(self.board, square):
                yield from self.find_moves_by_type(neighbour_type,
                                                   square,
                                                   colour_move_counts)
        for colour in (chess.WHITE, chess.BLACK):
            if colour_move_counts[colour] > 0:
                continue
            for square, piece in self.board.piece_map().items():
                if piece.color != colour:
                    continue
                yield from self.find_moves_by_type(chess.KING,
                                                   square,
                                                   colour_move_counts)

    def find_moves_by_type(self, neighbour_type, square, colour_move_counts):
        board_copy = self.board.copy()
        moving_piece = board_copy.piece_at(square)
        can_capture = moving_piece in self.chosen
        if can_capture and self.taking is not None:
            can_capture = square == self.taking
        if not can_capture:
            target_counts = None
        else:
            target_counts = self.chosen - self.taken
            target_counts[moving_piece] -= 1
        for turn in (chess.WHITE, chess.BLACK):
            fake_moving_piece = chess.Piece(neighbour_type, turn)
            board_copy.set_piece_at(square, fake_moving_piece)
            board_copy.turn = turn
            from_bitboard = 1 << square
            for move in board_copy.generate_pseudo_legal_moves(
                    from_bitboard):
                is_capture = board_copy.is_capture(move)
                if not is_capture:
                    if turn == chess.BLACK:
                        continue
                else:
                    if not can_capture:
                        continue
                    captured_piece = self.board.piece_at(move.to_square)
                    if target_counts[captured_piece] <= 0:
                        continue

                colour_move_counts[moving_piece.color] += 1
                yield move


def get_neighbour_types(board: chess.Board,
                        square: chess.Square) -> typing.Set[chess.PieceType]:
    neighbour_types = set()
    king_board = chess.Board()
    king_board.set_piece_at(square, chess.Piece(chess.KING, chess.WHITE))
    start_piece = board.piece_at(square)
    for neighbour_square in king_board.attacks(square):
        neighbour = board.piece_at(neighbour_square)
        if neighbour is None:
            continue
        if neighbour.color != start_piece.color:
            continue
        neighbour_types.add(neighbour.piece_type)
    return neighbour_types


def main():
    board = parse_board(dedent("""\
        . . B . . . R .
        . . . . . k . .
        . r . n . N . .
        . r . . b . . .
        R . . . . . q .
        . B . n . N . .
        b . . . . . . K
        . . . . . Q . ."""))
    for square, piece in board.piece_map().items():
        print(square, piece)


if __name__ == '__main__':
    main()
