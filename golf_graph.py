import logging
import math
import random
import typing
from collections import defaultdict
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass

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
    new_state_text: str
    heuristic: float = 0  # Drive search using A*, leave at zero for Dyjkstra.


class GolfGraph:
    def __init__(self, process_count: int = 0):
        self.graph: DiGraph | None = None
        self.start_text: str | None = None
        self.process_count = process_count
        self.is_debugging = False
        self.is_solved = False
        self.last = None
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
        self.start_text = start_state.display()
        self.graph.add_node(self.start_text)

        # if self.executor is not None:
        #     walker = self.clone()
        # else:
        #     walker = None

        # len of shortest path known from start to a state.
        g_score = defaultdict(lambda: math.inf)

        start_h = self.calculate_heuristic(start_state)
        g_score[self.start_text] = 0
        pending_nodes = PriorityQueue()
        pending_nodes.add(self.start_text, start_h)
        # requests: typing.Deque[MoveRequest] = deque()
        while pending_nodes and not self.is_solved:
            if size_limit is not None and len(self.graph) >= size_limit:
                raise GraphLimitExceeded(size_limit)
            state_text = pending_nodes.pop()
            state = GolfState(state_text)
            if not self.executor:
                moves = self.find_moves(state)
                self.add_moves(state_text, moves, pending_nodes, g_score)
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
                  start_text: str,
                  moves: typing.Iterable[MoveDescription],
                  pending_nodes: PriorityQueue,
                  g_score: typing.Dict[str, float]):
        state_g_score = g_score[start_text]
        for description in moves:
            new_g_score = state_g_score + 1
            new_state_text = description.new_state_text
            known_g_score = g_score[new_state_text]
            if not self.graph.has_node(new_state_text):
                # new node
                self.graph.add_node(new_state_text)
                is_improved = True
                if self.is_debugging:
                    if description.heuristic == 0:
                        print(new_state_text)
            else:
                is_improved = new_g_score < known_g_score
            if is_improved:
                g_score[new_state_text] = new_g_score
                f = new_g_score + description.heuristic

                pending_nodes.add(new_state_text, f)
            self.graph.add_edge(start_text,
                                new_state_text,
                                move=description.move)

    def generate_moves(self,
                       state: GolfState) -> typing.Iterator[MoveDescription]:
        """ Generate all moves from the board's current state. """
        for move in state.find_moves():
            new_state = state.move(move)
            yield MoveDescription(str(move),
                                  new_state.display(),
                                  self.calculate_heuristic(new_state))
            if new_state.is_solved:
                self.is_solved = True
                self.last = new_state.display()
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
            solution.append(self.graph[source][target]['move'])
        return solution

    def get_solution_nodes(self):
        goal = self.last
        solution_nodes = shortest_path(self.graph, self.start_text, goal)
        return solution_nodes


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    logger.info('Starting.')
    symbols_list = list(GolfState.SYMBOLS)
    longest = 0

    while True:
        random.shuffle(symbols_list)
        chosen = symbols_list[:3]
        state = GolfState.setup().choose(*chosen)
        graph = GolfGraph()
        try:
            graph.walk(state, size_limit=1_000_000)
        except GraphLimitExceeded:
            logger.error('Graph limit exceeded.')
            continue
        solution = graph.get_solution()
        if len(solution) > longest:
            longest = len(solution)
            logger.info('Problem:\n' + state.display())
            logger.info('Solution: ...' + ' ' * 120 + str(solution))


if __name__ == '__main__':
    main()
