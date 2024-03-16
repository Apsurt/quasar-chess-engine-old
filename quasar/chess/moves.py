"""
This module contains the Move and MoveFlags classes.
"""

from dataclasses import dataclass
from .pieces import PieceName, PieceColor, Piece
from .point import Point

@dataclass
class Move:
    """
    The Move class is responsible for storing the moves in the game.
    """
    def __init__(self, color_to_move: PieceColor, source: Point, target: Point) -> None:
        """
        The constructor for the Move class.

        :param color_to_move: current color to move
        :type color_to_move: PieceColor
        :param source: tile to move from
        :type source: Point
        :param target: tile to move to
        :type target: Point
        """
        none_piece = Piece(PieceName.NONE, Point(0,0), PieceColor.NONE)
        self.color_to_move: PieceColor = color_to_move
        self.source: Point = source
        self.target: Point = target
        self.moved: Piece = none_piece
        self.captured: Piece = none_piece
        self.legal: bool = True
        self.flags: MoveFlags = MoveFlags()

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
