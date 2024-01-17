import logging
import math
import typing
from collections import defaultdict
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass

import chess
from networkx import DiGraph, shortest_path

from golf import GolfState
from priority import PriorityQueue

logger = logging.getLogger(__name__)


@dataclass
class MoveRequest:
    start_state: str
    future: Future


class GraphLimitExceeded(RuntimeError):
    def __init__(self, limit):
        super(GraphLimitExceeded, self).__init__(
            'Graph size limit of {} exceeded.'.format(limit))
        self.limit = limit


@dataclass(frozen=True)
class MoveDescription:
    move: str
    new_state_bytes: bytes
    heuristic: float = 0  # Drive search using A*, leave at zero for Dyjkstra.


def move_to_bytes(move_text: str) -> bytes:
    move = chess.Move.from_uci(move_text)
    move_int = (move.from_square << 6) + move.to_square
    return int.to_bytes(move_int, 2)


def bytes_to_move(move_bytes: bytes) -> str:
    move_int = int.from_bytes(move_bytes)
    to_square = move_int % 64
    from_square = move_int >> 6
    move = chess.Move(from_square, to_square)
    return move.uci()


class GolfGraph:
    def __init__(self, process_count: int = 0):
        self.graph: DiGraph | None = None
        self.start_bytes: bytes | None = None
        self.process_count = process_count
        self.is_debugging = False
        self.is_solved = False
        self.last_bytes: bytes | None = None
        if process_count > 0:
            self.executor = ProcessPoolExecutor(process_count)
        else:
            self.executor = None

    @staticmethod
    def clone():
        """ Make a smaller copy to pass to subprocesses. """
        clone = GolfGraph()
        return clone

    def walk(self,
             start_state: GolfState,
             size_limit: int = None) -> typing.Set[str]:
        self.graph = DiGraph()
        self.start_bytes = start_state.to_bytes()
        self.graph.add_node(self.start_bytes)

        # if self.executor is not None:
        #     walker = self.clone()
        # else:
        #     walker = None

        # len of shortest path known from start to a state.
        g_score = defaultdict(lambda: math.inf)

        start_h = self.calculate_heuristic(start_state)
        g_score[self.start_bytes] = 0
        pending_nodes = PriorityQueue()
        pending_nodes.add(self.start_bytes, start_h)
        # requests: typing.Deque[MoveRequest] = deque()
        while pending_nodes and not self.is_solved:
            if size_limit is not None and len(self.graph) >= size_limit:
                raise GraphLimitExceeded(size_limit)
            state_bytes = pending_nodes.pop()
            state = GolfState(state_bytes=state_bytes)
            if not self.executor:
                moves = self.find_moves(state)
                self.add_moves(state_bytes, moves, pending_nodes, g_score)
            # else:
            #     request = MoveRequest(
            #         state,
            #         self.executor.submit(walker.find_moves, state, max_pips))
            #     requests.append(request)
            #     while ((not pending_nodes and requests) or
            #            len(requests) > 2*self.process_count):
            #         request = requests.popleft()
            #         state = request.start_state
            #         moves = request.future.result()
            #         self.add_moves(state, moves, pending_nodes, g_score)
        return set(self.graph.nodes())

    def find_moves(self, state: GolfState) -> typing.List[MoveDescription]:
        if state.is_solved:
            return []
        moves = list(self.generate_moves(state))
        return moves

    def add_moves(self,
                  start_bytes: bytes,
                  moves: typing.Iterable[MoveDescription],
                  pending_nodes: PriorityQueue,
                  g_score: typing.Dict[bytes, float]):
        state_g_score = g_score[start_bytes]
        for description in moves:
            new_g_score = state_g_score + 1
            new_state_bytes = description.new_state_bytes
            known_g_score = g_score[new_state_bytes]
            if not self.graph.has_node(new_state_bytes):
                # new node
                self.graph.add_node(new_state_bytes)
                is_improved = True
                if self.is_debugging:
                    if description.heuristic == 0:
                        print(new_state_bytes)
            else:
                is_improved = new_g_score < known_g_score
            if is_improved:
                g_score[new_state_bytes] = new_g_score
                f = new_g_score + description.heuristic

                pending_nodes.add(new_state_bytes, f)
            move_bytes = move_to_bytes(description.move)
            self.graph.add_edge(start_bytes,
                                new_state_bytes,
                                move_bytes=move_bytes)

    def generate_moves(self,
                       state: GolfState) -> typing.Iterator[MoveDescription]:
        """ Generate all moves from the board's current state. """
        for move in state.find_moves():
            new_state = state.move(move)
            yield MoveDescription(str(move),
                                  new_state.to_bytes(),
                                  self.calculate_heuristic(new_state))
            if new_state.is_solved:
                self.is_solved = True
                self.last_bytes = new_state.to_bytes()
                return

    @staticmethod
    def calculate_heuristic(state: GolfState) -> int:
        return sum((state.chosen - state.taken).values())

    def get_solution(self) -> typing.List[str]:
        """ Find a solution from the graph of moves.

        @return: a list of strings describing each move. Each string has the
        from and to square coordinates of the move.
        """
        solution = []
        solution_nodes = self.get_solution_nodes()
        for i in range(len(solution_nodes)-1):
            source, target = solution_nodes[i:i+2]
            move_bytes = self.graph[source][target]['move_bytes']
            move = bytes_to_move(move_bytes)
            solution.append(move)
        return solution

    def get_solution_nodes(self):
        goal = self.last_bytes
        solution_nodes = shortest_path(self.graph, self.start_bytes, goal)
        return solution_nodes
