import typing
from collections import Counter
from copy import copy
import random

import chess

from board_parser import parse_board


class GolfState:
    SYMBOLS = 'NNBBRRQKnnbbrrqk'

    @classmethod
    def setup(cls, rng: random.Random = None):
        if rng is None:
            rng = random
        symbols_list = list(cls.SYMBOLS)
        gaps = {'n': 1, 'b': 2, 'r': 3, 'q': 5, 'k': 6}
        rng.shuffle(symbols_list)
        board = chess.Board.empty()
        square = -1
        for symbol in symbols_list:
            square += gaps[symbol.lower()] + 1
            board.set_piece_at(square, chess.Piece.from_symbol(symbol))
        board.apply_transform(chess.flip_vertical)
        board_text = str(board)
        return GolfState(board_text)

    def __init__(self, text: str = None, state_bytes: bytes = None) -> None:
        self.taking = None
        self.taken = Counter()
        self.chosen = Counter()
        if state_bytes is not None:
            board = chess.Board.empty()
            state_int = int.from_bytes(state_bytes)
            ignored_positions = []
            for counter in (self.taken, self.chosen):
                element_count = state_int % 16
                state_int >>= 4
                for _ in range(element_count):
                    piece_index = state_int % 16
                    if counter is self.taken:
                        ignored_positions.append(piece_index)
                    state_int >>= 4
                    symbol = self.SYMBOLS[piece_index]
                    piece = chess.Piece.from_symbol(symbol)
                    counter[piece] += 1
            if self.taken.total():
                self.taking = state_int % 64
                state_int >>= 6
            for i, symbol in enumerate(reversed(self.SYMBOLS)):
                if (len(self.SYMBOLS) - i - 1) not in ignored_positions:
                    square = state_int % 64
                    board.set_piece_at(square, chess.Piece.from_symbol(symbol))
                state_int >>= 6
            self.board = board
        else:
            board_lines = text.splitlines()
            board_text = '\n'.join(board_lines[:8])
            self.board = parse_board(board_text)
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

    def __repr__(self):
        display = self.display()
        return f'GolfState({display!r})'

    def display(self):
        sections = [str(self.board)]
        if self.chosen:
            sections.append('chosen: ' +
                            ''.join(sorted(str(piece)
                                           for piece in self.chosen.elements())))
        if self.taking is not None:
            sections.append('taking: ' + chess.SQUARE_NAMES[self.taking])
        if self.taken:
            sections.append('taken: ' +
                            ''.join(sorted(str(piece)
                                           for piece in self.taken.elements())))
        return '\n'.join(sections)

    def to_bytes(self) -> bytes:
        positions: typing.List[int | None] = [None] * 16
        for square, piece in self.board.piece_map().items():
            index = self.SYMBOLS.index(piece.symbol())
            if positions[index] is not None:
                index += 1
            positions[index] = square
        state_int = 0
        for position in positions:
            if position is None:
                position = 0
            state_int = (state_int << 6) + position
        bits_needed = 16*6
        if self.taking is not None:
            state_int = (state_int << 6) + self.taking
            bits_needed += 6
        for counter in (self.chosen, self.taken):
            used_indexes = set()
            for piece in counter.elements():
                piece_index = self.SYMBOLS.rindex(piece.symbol())
                if piece_index in used_indexes:
                    piece_index -= 1
                state_int = (state_int << 4) + piece_index
                used_indexes.add(piece_index)
                bits_needed += 4
            state_int = (state_int << 4) + counter.total()
            bits_needed += 4

        return int.to_bytes(state_int, (bits_needed + 7) // 8)

    @property
    def is_solved(self):
        return sum((self.chosen - self.taken).values()) <= 1

    def choose(self, *symbols):
        new_state = copy(self)
        new_state.chosen = Counter(chess.Piece.from_symbol(symbol)
                                   for symbol in symbols)
        return new_state

    def find_moves(self) -> typing.Iterator[chess.Move]:
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

    def find_moves_by_type(self,
                           neighbour_type,
                           square,
                           colour_move_counts) -> typing.Iterator[chess.Move]:
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

    def move(self, move: chess.Move) -> typing.Self:
        new_state = copy(self)
        new_board = self.board.copy()
        new_taken = self.taken.copy()
        taken_piece = new_board.piece_at(move.to_square)
        moving_piece = new_board.piece_at(move.from_square)
        new_board.set_piece_at(move.from_square, None)
        new_board.set_piece_at(move.to_square, moving_piece)

        if taken_piece is not None:
            new_taken[taken_piece] += 1
            new_state.taking = move.to_square
        elif self.taking == move.from_square:
            new_state.taking = move.to_square
        new_state.board = new_board
        new_state.taken = new_taken
        return new_state

    def drop(self, rng=None) -> typing.Self:
        if rng is None:
            rng = random
        new_state = copy(self)
        new_state.board = self.board.copy()
        new_state.taken = Counter()
        new_state.taking = None
        new_state.chosen = Counter()
        to_drop = list(self.taken.elements())
        occupied = chess.SquareSet(self.board.occupied)
        empty_spaces = chess.SquareSet(chess.BB_ALL) - occupied
        targets = rng.sample(list(empty_spaces), len(to_drop))
        for piece, target in zip(to_drop, targets):
            new_state.board.set_piece_at(target, piece)
        return new_state


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
