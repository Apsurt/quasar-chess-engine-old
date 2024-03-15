"""
This module contains the Move and MoveFlags classes.
"""

from dataclasses import dataclass
from .point import Point

@dataclass
class Move:
    """
    The Move class is responsible for storing the moves in the game.
    """
    def __init__(self, source: Point, target: Point) -> None:
        """
        The constructor for the Move class.

        :param source: Point where the move starts.
        :type source: Point
        :param target: Point where the move ends.
        :type target: Point
        """
        self.source = source
        self.target = target
        self.moved = None
        self.captured = None
        self.legal = True
        self.flags = MoveFlags()

@dataclass
class MoveFlags:
    """
    The MoveFlags class is responsible for storing the flags for a move.
    """
    def __init__(self) -> None:
        """
        The constructor for the MoveFlags class.
        """
        self.promotion = False
        self.castling = False
        self.en_passant = False
        self.check = False
        self.checkmate = False
        self.stalemate = False
