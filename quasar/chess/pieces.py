"""
This module contains the Piece class,
which is responsible for managing the state of the pieces.
"""

from typing import Generator
from enum import Enum
import numpy as np
from quasar.logger import logger
from .point import Point

class PieceColor(Enum):
    """
    Enumerated type that represents piece color.
    Available types: NONE, WHITE, BLACK
    """
    NONE = 0
    WHITE = 1
    BLACK = -1

class PieceName(Enum):
    """
    Enumerated type that represents piece name.
    Available types: NONE, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
    """
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Piece:
    """
    Piece class that represents a chess piece.
    """
    def __init__(self,
                 name: PieceName,
                 position: Point,
                 color: PieceColor) -> None:
        """
        Piece constructor.

        :param _id: Piece identifier
        :type _id: int
        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :raises TypeError: when position is not of Point type
        """
        self.unique_id = np.random.randint(0, 1000000000)
        self.name = name
        self.color = color
        logger.debug("Creating %s %s with id: %s at %s",
                     self.color.name.lower(),
                     self.name.name.lower(),
                     self.unique_id,
                     position.__repr__())
        if not isinstance(position, Point):
            raise TypeError(f"Position has to be of type point, got {type(position)} instead")
        self.position = position
        self.moved = False
        self.sliding = False
        self.offsets = []

    def is_none(self) -> bool:
        """
        Checks if the piece is none.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.NONE

    def is_pawn(self) -> bool:
        """
        Checks if the piece is a pawn.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.PAWN

    def is_knight(self) -> bool:
        """
        Checks if the piece is a knight.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.KNIGHT

    def is_bishop(self) -> bool:
        """
        Checks if the piece is a bishop.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.BISHOP

    def is_rook(self) -> bool:
        """
        Checks if the piece is a rook.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.ROOK

    def is_queen(self) -> bool:
        """
        Checks if the piece is a queen.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.QUEEN

    def is_king(self) -> bool:
        """
        Checks if the piece is a king.

        :return: True or False
        :rtype: bool
        """
        return self.name == PieceName.KING

    def is_white(self) -> bool:
        """
        Checks if the piece is white.

        :return: True or False
        :rtype: bool
        """
        return self.color == PieceColor.WHITE

    def is_black(self) -> bool:
        """
        Checks if the piece is black.

        :return: True or False
        :rtype: bool
        """
        return self.color == PieceColor.BLACK
    
    def is_sliding(self) -> bool:
        """
        Checks if the piece is sliding.

        :return: True or False
        :rtype: bool
        """
        return self.sliding

    def is_promotion_square(self) -> bool:
        """
        Checks if the piece is on a promotion square.

        :return: True or False
        :rtype: bool
        """
        if self.color == PieceColor.WHITE:
            return self.position.y == 7
        if self.color == PieceColor.BLACK:
            return self.position.y == 0
        return False

    def get_offset_generator(self, bottom_left_bound,
                             top_right_bound) -> Generator[Point, None, None]:
        """
        Creates a generator that yields offsets of the piece,
        acording to the way that the piece moves.

        :yield: offset
        :rtype: Point
        """
        for offset in self.offsets:
            if bottom_left_bound.x <= self.position.x + offset.x <= top_right_bound.x and \
               bottom_left_bound.y <= self.position.y + offset.y <= top_right_bound.y:
                yield offset
        if self.sliding:
            misfire = 0
            i = 0
            while misfire < 100:
                i += 1
                for offset in self.offsets:
                    if bottom_left_bound.x <= self.position.x + offset.x * i <= top_right_bound.x and \
                       bottom_left_bound.y <= self.position.y + offset.y * i <= top_right_bound.y:
                        yield offset * i
                    else:
                        misfire += 1

    def get_position(self) -> Point:
        """
        Returns piece position.

        :return: self.position
        :rtype: Point
        """
        return self.position

    def set_position(self, position: Point) -> None:
        """
        Sets piece position.

        :param position: position to be set
        :type position: Point
        :raises TypeError: when position is not of Point type
        """
        if not isinstance(position, Point):
            raise TypeError(f"Position has to be of type point, got {type(position)} instead")
        self.position = position
        self.moved = True
        try:
            self.update_offsets()
        except AttributeError:
            pass

    def get_name(self) -> PieceName:
        """
        Returns piece name.

        :return: self.name
        :rtype: PieceName
        """
        return self.name

    def get_color(self) -> PieceColor:
        """
        Returns piece color.

        :return: self.color
        :rtype: PieceColor
        """
        return self.color

    def get_moved(self) -> bool:
        """
        Returns True if the piece has moved, False otherwise.

        :return: True or False
        :rtype: bool
        """
        return self.moved

    def get_fen_char(self) -> str:
        """
        Returns FEN character for the piece.

        :return: FEN character
        :rtype: str
        """
        if self.name == PieceName.NONE:
            res = "-"
        elif self.name == PieceName.KNIGHT:
            res = "N"
        else:
            res = self.name.name[0]
        if self.color == PieceColor.WHITE:
            return res
        return res.lower()

    def __str__(self) -> str:
        return f"{self.color.name.capitalize()} {self.name.name.capitalize()} at {self.position!r}"

    def __repr__(self) -> str:
        return f"{self.color.name.capitalize()} {self.name.name.capitalize()}"

class Pawn(Piece):
    """
    Pawn class that inherits from Piece class.

    :param Piece: Piece class
    :type Piece: class
    """
    def __init__(self, piece_name: PieceName, position: Point, color: PieceColor) -> None:
        """
        Pawn constructor.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        """
        super().__init__(piece_name, position, color)
        self.sliding = False
        self.offsets = []
        self.update_offsets()

    def update_offsets(self) -> None:
        """
        Updates pawn offsets after initial move.
        """
        if self.color == PieceColor.WHITE:
            self.offsets = [Point(0, 1), Point(-1, 1), Point(1, 1)]
            if not self.moved:
                self.offsets.append(Point(0, 2))
        if self.color == PieceColor.BLACK:
            self.offsets = [Point(0, -1), Point(-1, -1), Point(1, -1)]
            if not self.moved:
                self.offsets.append(Point(0, -2))

class Knight(Piece):
    """
    Knight class that inherits from Piece class.

    :param Piece: Piece class
    :type Piece: class
    """
    def __init__(self, piece_name: PieceName, position: Point, color: PieceColor) -> None:
        """
        Knight constructor.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        """
        super().__init__(piece_name, position, color)
        self.sliding = False
        self.offsets = [Point(1, 2),
                        Point(2, 1),
                        Point(-1, 2),
                        Point(2, -1),
                        Point(-1, -2),
                        Point(-2, -1),
                        Point(1, -2),
                        Point(-2, 1)]

class Bishop(Piece):
    """
    Bishop class that inherits from Piece class.

    :param Piece: Piece class
    :type Piece: class
    """
    def __init__(self, piece_name: PieceName, position: Point, color: PieceColor) -> None:
        """
        Bishop constructor.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        """
        super().__init__(piece_name, position, color)
        self.sliding = True
        self.offsets = [Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class Rook(Piece):
    """
    Rook class that inherits from Piece class.

    :param Piece: Piece class
    :type Piece: class
    """
    def __init__(self, piece_name: PieceName, position: Point, color: PieceColor) -> None:
        """
        Rook constructor.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        """
        super().__init__(piece_name, position, color)
        self.sliding = True
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

class Queen(Piece):
    """
    Queen class that inherits from Piece class.

    :param Piece: Piece class
    :type Piece: class
    """
    def __init__(self, piece_name: PieceName, position: Point, color: PieceColor) -> None:
        """
        Queen constructor.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        """
        super().__init__(piece_name, position, color)
        self.sliding = True
        self.offsets = [Point(1, 0),
                        Point(0, 1),
                        Point(-1, 0),
                        Point(0, -1),
                        Point(1, 1),
                        Point(-1, 1),
                        Point(-1, -1),
                        Point(1, -1)]

class King(Piece):
    """
    King class that inherits from Piece class.

    :param Piece: Piece class
    :type Piece: class
    """
    def __init__(self, piece_name: PieceName, position: Point, color: PieceColor) -> None:
        """
        King constructor.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        """
        super().__init__(piece_name, position, color)
        self.sliding = False
        self.offsets = [Point(1, 0),
                        Point(0, 1),
                        Point(-1, 0),
                        Point(0, -1),
                        Point(1, 1),
                        Point(-1, 1),
                        Point(-1, -1),
                        Point(1, -1)]

class PieceFactory:
    """
    Piece factory class that makes creating pieces easier.
    """
    def create_piece(self, name: PieceName, position: Point, color: PieceColor) -> Piece:
        """
        Creates a piece.

        :param name: piece name in the form of enum
        :type name: PieceName
        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :raises InvalidPieceTypeError: when piece type is invalid
        :return: Piece class object
        :rtype: Piece
        """

        class_dict = {PieceName.PAWN: Pawn,
                      PieceName.KNIGHT: Knight,
                      PieceName.BISHOP: Bishop,
                      PieceName.ROOK: Rook,
                      PieceName.QUEEN: Queen,
                      PieceName.KING: King,
                      PieceName.NONE: Piece}

        if name != PieceName.NONE:
            class_ = class_dict[name]
            return class_(name, position, color)
        return Piece(name, position, color)

    def create_pawn(self, position: Point, color: PieceColor) -> Piece:
        """
        Creates a pawn.

        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :return: Pawn class object
        :rtype: Pawn
        """
        return Pawn(PieceName.PAWN, position, color)

    def create_knight(self, position: Point, color: PieceColor) -> Piece:
        """
        Creates a knight.

        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :return: Knight class object
        :rtype: Knight
        """
        return Knight(PieceName.KNIGHT, position, color)

    def create_bishop(self, position: Point, color: PieceColor) -> Piece:
        """
        Creates a bishop.

        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :return: Bishop class object
        :rtype: Bishop
        """
        return Bishop(PieceName.BISHOP, position, color)

    def create_rook(self, position: Point, color: PieceColor) -> Piece:
        """
        Creates a rook.

        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :return: Rook class object
        :rtype: Rook
        """
        return Rook(PieceName.ROOK, position, color)

    def create_queen(self, position: Point, color: PieceColor) -> Piece:
        """
        Creates a queen.

        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :return: Queen class object
        :rtype: Queen
        """
        return Queen(PieceName.QUEEN, position, color)

    def create_king(self, position: Point, color: PieceColor) -> Piece:
        """
        Creates a king.

        :param position: position of the piece on the board
        :type position: Point
        :param color: either white, black or none, in the form of enum
        :type color: PieceColor
        :return: King class object
        :rtype: King
        """
        return King(PieceName.KING, position, color)

if __name__ == "__main__":
    factory = PieceFactory()
    pawn = factory.create_piece(PieceName.PAWN, Point(0,0), PieceColor.WHITE)
    print(pawn)
