import chess

from golf import GolfState, get_neighbour_types
from heuristic import Heuristic


class GreedyHeuristic(Heuristic):
    def analyse(self,
                state: GolfState,
                move_text: str | None,
                depth: int) -> float:
        captured_count = state.taken.total()
        value = captured_count * 100 - depth
        if move_text is not None:
            move = chess.Move.from_uci(move_text)
            moved_piece = state.board.piece_at(move.to_square)
            if moved_piece in state.chosen:
                value += 20
            else:
                for neighbour_type in get_neighbour_types(state.board,
                                                          move.to_square):
                    neighbour = chess.Piece(neighbour_type, moved_piece.color)
                    if neighbour in state.chosen:
                        value += 10
                        break
        return value
