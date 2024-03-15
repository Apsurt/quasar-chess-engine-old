"""
This module contains the MoveValidator class, which is responsible for validating moves.
"""

from .moves import Move
from .board import Board

class Validator:
    """
    This class is responsible for validating moves.
    """
    def __call__(self, move: Move, board: Board) -> Move:
        """
        This method performs all the logic to categorize move as legal or illegal.

        :param move: Move to be validated.
        :type move: Move
        :param board: Board on which the move is to be played.
        :type board: Board
        :return: Validated move.
        :rtype: Move
        """

if __name__ == "__main__":
    pass
