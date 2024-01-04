from abc import ABCMeta, abstractmethod

from golf import GolfState


class Heuristic(metaclass=ABCMeta):
    @abstractmethod
    def analyse(self,
                state: GolfState,
                move_text: str,
                depth: int) -> float:
        """ Analyse the value of a board position and predict a move.

        :param state: the current state of the board
        :param move_text: the move that got to this state
        :param depth: the depth of the state in the search tree
        :return: the estimated value of the board for the active player
        """
