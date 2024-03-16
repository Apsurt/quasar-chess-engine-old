"""
This module contains the Move and MoveFlags classes.
"""

from dataclasses import dataclass
from .pieces import PieceColor
from .point import Point

@dataclass
class Move:
    """
    The Move class is responsible for storing the moves in the game.
    """
    def __init__(self, color_to_move: PieceColor, source: Point, target: Point) -> None:
        """
        The constructor for the Move class.

        :param color_to_move: Color of the piece making the move.
        :type color_to_move: PieceColor
        :param source: Point where the move starts.
        :type source: Point
        :param target: Point where the move ends.
        :type target: Point
        """
        self.color_to_move = color_to_move
        self.source = source
        self.target = target
        self.moved = None
        self.captured = None
        self.legal = True
        self.flags = MoveFlags()

    def __str__(self) -> str:
        return f"{self.moved} {self.source} -> {self.target}"

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
