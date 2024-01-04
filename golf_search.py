import logging

import math
import typing
from _weakref import ref
from datetime import datetime
from itertools import count

from golf import GolfState
from heuristic import Heuristic

logger = logging.getLogger(__name__)


class SearchNode:
    # Controls exploration of new nodes vs. exploitation of good nodes.
    exploration_weight = 1.0

    def __init__(self,
                 golf_state: GolfState,
                 parent: typing.Self = None,
                 move_text: str = None,
                 depth: int = 0):
        """ Initialize an instance.

        :param golf_state: the board state that this node represents
        :param parent: the board state that this node came from
        :param move_text: the move to get from parent to this node
        :param depth: the number of moves to get to this node from start state
        """
        self.state_bytes = golf_state.to_bytes()
        self.state_ref = ref(golf_state)
        self.parent = parent
        self.move_text = move_text
        self.depth = depth
        self.children: typing.Dict[str, SearchNode] | None = None
        self.average_value = 0.0
        self.value_count = 0

    def __repr__(self):
        game_state = GolfState(state_bytes=self.state_bytes)
        return f"SearchNode({game_state!r})"

    @property
    def golf_state(self):
        golf_state = self.state_ref()
        if golf_state is not None:
            return golf_state

        # Resurrect state from compressed version
        golf_state = GolfState(state_bytes=self.state_bytes)
        self.state_ref = ref(golf_state)
        return golf_state

    def select_leaf(self):
        if self.value_count <= 1:
            return self
        children = self.find_all_children()
        if not children:
            return self

        best_score = float('-inf')
        best_child = None
        for move_text, child in children.items():
            prior = 1/len(children)
            score = child.average_value + (self.exploration_weight * prior *
                                           math.sqrt(self.value_count) /
                                           (1 + child.value_count))
            if score > best_score:
                best_score = score
                best_child = child
        # if self.depth == 0:
        #     print(f'Selected child {best_child.move_text} with score {best_score}.')
        return best_child.select_leaf()

    def find_all_children(self) -> typing.Dict[str, typing.Self]:
        if self.children is not None:
            return self.children
        children: typing.Dict[str, SearchNode] = {}
        current_state = self.golf_state
        if current_state.is_solved:
            return children
        for move in current_state.find_moves():
            child_state = current_state.move(move)
            children[move.uci()] = SearchNode(child_state, self, move.uci(), self.depth + 1)
        self.children = children
        return children

    def record_value(self, value: float):
        self.average_value = ((self.average_value * self.value_count + value) /
                              (self.value_count + 1))
        self.value_count += 1
        if self.parent:
            self.parent.record_value(value)

    def evaluate(self, heuristic: Heuristic):
        children = self.find_all_children()
        if not children:
            self.record_value(self.average_value)
            return

        for move_text, child in children.items():
            value = heuristic.analyse(child.golf_state, move_text, child.depth)
            child.record_value(value)

    def rank_children(self) -> typing.Tuple[typing.List[str],
                                            typing.List[float]]:
        move_list = []
        weights = []
        for move_text, child in self.find_all_children().items():
            move_list.append(move_text)
            weights.append(child.average_value)
        min_weight = min(weights)
        if min_weight <= 0:
            weights = [weight - min_weight + 1 for weight in weights]
        return move_list, weights


class SearchManager:
    def __init__(self,
                 start_state: GolfState,
                 heuristic: Heuristic,
                 process_count: int = 1):
        self.start_state = start_state
        self.heuristic = heuristic
        self.current_node = self.reset()
        self.process_count = process_count
        self.search_count = 0
        self.total_iterations = 0
        self.total_milliseconds = 0
        self.best_solution_node: SearchNode | None = None

    def find_node(self, game_state: GolfState):
        state_bytes = game_state.to_bytes()
        if not game_state == self.current_node.state_bytes:
            for child in self.current_node.find_all_children().values():
                if state_bytes == child.state_bytes:
                    self.current_node = child
                    break
            else:
                parent = self.current_node.parent
                if parent is not None and state_bytes == parent.state_bytes:
                    self.current_node = parent
                else:
                    self.current_node = SearchNode(game_state)

    def search(self,
               board: GolfState,
               iterations: int | None = None,
               milliseconds: int | None = None):
        start_time = datetime.now()
        self.find_node(board)
        best_solution_depth: int | None = None
        self.best_solution_node = None
        visited = set()
        for iteration in count(1):
            if iteration % 1000 == 0:
                print(f'Visited {len(visited)} nodes.')
            leaf = self.current_node.select_leaf()
            visited.add(leaf.state_bytes)
            if not leaf.find_all_children():
                # Found a solution, is it the best so far?
                if best_solution_depth is None or leaf.depth < best_solution_depth:
                    best_solution_depth = leaf.depth
                    self.best_solution_node = leaf
            leaf.evaluate(self.heuristic)
            if iterations is not None:
                if iteration >= iterations:
                    break
            else:
                assert milliseconds is not None
                spent_seconds = (datetime.now() - start_time).total_seconds()
                if spent_seconds*1000 > milliseconds:
                    break

    def reset(self) -> SearchNode:
        self.current_node = SearchNode(self.start_state)
        return self.current_node

    def get_solution(self) -> typing.List[str]:
        node = self.best_solution_node
        if node is None:
            raise RuntimeError('No solution found.')
        moves = []
        while node.move_text is not None:
            moves.append(node.move_text)
            node = node.parent
        moves.reverse()
        return moves
