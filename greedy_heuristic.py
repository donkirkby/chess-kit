from math import exp

import chess

from golf import GolfState, get_neighbour_types
from heuristic import Heuristic


class GreedyHeuristic(Heuristic):
    def analyse(self,
                state: GolfState,
                move_text: str | None,
                depth: int) -> float:
        max_captures = state.chosen.total() - 1
        captured_count = state.taken.total()
        capture_bonus = 100
        move_chosen_bonus = 20
        neighbour_chosen_bonus = 10
        max_raw_value = (capture_bonus * max_captures +
                         move_chosen_bonus +
                         8 * neighbour_chosen_bonus)
        value = captured_count * capture_bonus - depth
        if move_text is not None:
            move = chess.Move.from_uci(move_text)
            moved_piece = state.board.piece_at(move.to_square)
            if moved_piece in state.chosen:
                value += move_chosen_bonus
            for neighbour_type in get_neighbour_types(state.board,
                                                      move.to_square):
                neighbour = chess.Piece(neighbour_type, moved_piece.color)
                if neighbour in state.chosen:
                    value += neighbour_chosen_bonus
                    break
        return exp(value - max_raw_value)
