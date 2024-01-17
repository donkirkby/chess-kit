import logging

import math
import random
import typing
from _weakref import ref
from collections import Counter
from datetime import datetime
from itertools import count
from math import exp

from golf import GolfState
from greedy_heuristic import GreedyHeuristic
from heuristic import Heuristic

logger = logging.getLogger(__name__)


class NoSolutionError(Exception):
    pass


class SearchNode:
    # Controls exploration of new nodes vs. exploitation of good nodes.
    exploration_weight = 0.25

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

        total_child_values = sum(child.average_value
                                 for child in children.values())
        if total_child_values == 0:
            # Scores are all so bad that they round down to zero.
            return self
        best_score = float('-inf')
        best_child = None
        all_scores = []
        for move_text, child in children.items():
            prior = child.average_value / total_child_values
            score = child.average_value + (self.exploration_weight * prior *
                                           math.sqrt(self.value_count) /
                                           (1 + child.value_count))
            all_scores.append((move_text, score))
            if score > best_score:
                best_score = score
                best_child = child
        # if self.depth == 0:
        #     all_scores.sort()
        #     for move_text, score in all_scores:
        #         print(f'{move_text}: {score:0.6f}')
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

        max_value = 0
        for move_text, child in children.items():
            value = heuristic.analyse(child.golf_state,
                                      move_text,
                                      child.depth)
            child.average_value = value
            child.value_count = 1
            max_value = max(max_value, value)
        self.record_value(max_value)

    def rank_children(self) -> typing.Tuple[typing.List[str],
                                            typing.List[float]]:
        move_list = []
        weights = []
        for move_text, child in self.find_all_children().items():
            move_list.append(move_text)
            weights.append(child.average_value)
        return move_list, weights

    def remove_child(self, to_remove: typing.Self) -> None:
        for move_text, child in self.find_all_children().items():
            if child.state_bytes == to_remove.state_bytes:
                del self.children[move_text]
                return


class SearchManager:
    def __init__(self,
                 start_state: GolfState,
                 heuristic: Heuristic,
                 process_count: int = 1):
        self.start_state = start_state
        self.heuristic = heuristic
        self.current_node = self.reset()
        self.visited_nodes = {self.start_state.to_bytes(): self.current_node}
        self.process_count = process_count
        self.search_count = 0
        self.total_iterations = 0
        self.total_milliseconds = 0
        self.best_solution_node: SearchNode | None = None

    def find_node(self, game_state: GolfState):
        state_bytes = game_state.to_bytes()
        if state_bytes == self.current_node.state_bytes:
            return
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
        max_depth = 0
        for iteration in count(1):
            leaf = self.current_node.select_leaf()
            if leaf.depth > max_depth:
                logger.info('Max depth: %d', max_depth)
                max_depth = leaf.depth
                # print(f'{max_depth=}')
            duplicate_node = self.visited_nodes.get(leaf.state_bytes)
            if duplicate_node is None:
                self.visited_nodes[leaf.state_bytes] = leaf
            else:
                if leaf.parent is None:
                    pass
                elif duplicate_node.depth <= leaf.depth:
                    # print(f'=== remove leaf ===\n'
                    #       f'{leaf.golf_state.display()}\n'
                    #       f'from parent id {id(leaf.parent)}\n'
                    #       f'{leaf.parent.golf_state.display()}')
                    leaf.parent.remove_child(leaf)
                    continue  # Already evaluated duplicate node.
                else:
                    # print(f'=== remove visited ===\n'
                    #       f'{duplicate_node.golf_state.display()}\n'
                    #       f'from parent id {id(duplicate_node.parent)}\n'
                    #       f'{duplicate_node.parent.golf_state.display()}')
                    self.visited_nodes[leaf.state_bytes] = leaf
                    duplicate_node.parent.remove_child(duplicate_node)
            if leaf.golf_state.is_solved:
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
            raise NoSolutionError('No solution found.')
        moves = []
        node2 = node
        while node2 is not None:
            print('='*10, node2.move_text)
            print(node2.golf_state.display())
            node2 = node2.parent
        while node.move_text is not None:
            moves.append(node.move_text)
            node = node.parent
        moves.reverse()
        return moves


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    logger.info('Starting.')

    deal_count = 3
    totals_frequency = Counter()
    longest = 0
    most_iterations = 0
    try:
        for game_num in range(100):
            deck = []
            state = GolfState.setup()
            total_moves = 0

            for _ in range(9):
                if len(deck) < deal_count:
                    deck = list(GolfState.SYMBOLS)
                    random.shuffle(deck)
                chosen = deck[:deal_count]
                deck = deck[deal_count:]
                state = state.choose(*chosen)
                manager = SearchManager(state, GreedyHeuristic())
                iterations = 0
                while True:
                    batch_iterations = 1000
                    try:
                        manager.search(state, batch_iterations)
                    except Exception:
                        logger.exception(
                            f'Search failed on board:\n{state.display()}')
                        raise
                    iterations += batch_iterations
                    try:
                        solution = manager.get_solution()
                        break
                    except NoSolutionError:
                        pass  # Keep searching...
                    if iterations > most_iterations:
                        logger.info('Most iterations found: %d', iterations)
                should_log = False
                if iterations > most_iterations:
                    most_iterations = iterations
                    logger.info('Most iterations found: %d', iterations)
                    should_log = True
                if len(solution) > longest:
                    longest = len(solution)
                    logger.info('Longest solution: %s%d.',
                                ' ' * 120,
                                longest)
                    should_log = True
                if should_log:
                    logger.info('Problem:\n' + state.display())
                    logger.info('Solution: ...' + ' ' * 120 + str(solution))
                total_moves += len(solution)
                state = manager.best_solution_node.golf_state
                new_state = state.drop()
                piece_counts = Counter(new_state.board.piece_map().values())
                most_common = piece_counts.most_common()[0]
                if most_common[1] > 2:
                    logger.error(f'Too many {most_common[0]}:\n'
                                 f'{state.display()}\n{new_state.display()}')
                    exit()
                state = new_state
            else:
                totals_frequency[total_moves] += 1
                logger.info('Game %d, total moves: %d.',
                            game_num,
                            total_moves)
    finally:
        if len(totals_frequency) > 0:
            min_total = min(totals_frequency)
            max_total = max(totals_frequency)
            logger.info('Totals frequency:')
            for total in range(min_total, max_total + 1):
                logger.info(f'{total}: {totals_frequency[total]}')


if __name__ == '__main__':
    main()
