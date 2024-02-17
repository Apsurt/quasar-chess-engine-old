from point import Point
from errors import InvalidPieceTypeError
from enum import Enum
import numpy as np
from logger import logger

class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = -1

class PieceName(Enum):
    NONE = 0
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Piece:
    def __init__(self, _id=PieceName.NONE.value, name=PieceName.NONE, position=Point(0, 0), color=Color.NONE) -> None:
        self.unique_id = np.random.randint(0, 1000000000)
        self.id = _id
        self.name = name
        self.color = color
        if not isinstance(position, Point):
            raise InvalidPieceTypeError("Invalid position type")
        self.position = position
        self.moved = False
        self.sliding = False
    
    is_pawn = lambda self: self.name == PieceName.PAWN
    is_rook = lambda self: self.name == PieceName.ROOK
    is_knight = lambda self: self.name == PieceName.KNIGHT
    is_bishop = lambda self: self.name == PieceName.BISHOP
    is_queen = lambda self: self.name == PieceName.QUEEN
    is_king = lambda self: self.name == PieceName.KING
    is_white = lambda self: self.color == Color.WHITE
    is_black = lambda self: self.color == Color.BLACK

    def is_promotion_square(self):
        if self.color == Color.WHITE:
            return self.position.y == 7
        elif self.color == Color.BLACK:
            return self.position.y == 0
        return False
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        if not isinstance(position, Point):
            raise InvalidPieceTypeError("Invalid position type")
        self.position = position
        self.moved = True
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color
    
    def get_id(self):
        return self.id
    
    def get_moved(self):
        return self.moved
    
    def get_fen_char(self):
        if self.name == PieceName.NONE:
            res = "-"
        elif self.name == PieceName.KNIGHT:
            res = "N"
        else:
            res = self.name.name[0]
        if self.color == Color.WHITE:
            return res
        return res.lower()
    
    def __str__(self) -> str:
        return f"{self.color.name.capitalize()} {self.name.name.capitalize()} at {self.position!r}"
    
    def __repr__(self) -> str:
        return f"{self.color.name.capitalize()} {self.name.name.capitalize()}"

class Pawn(Piece):
    def __init__(self, piece_name, position, color) -> None:
        super().__init__(piece_name.value, piece_name, position, color)
        self.sliding = False
        self.offsets = []
        self.update_offsets()
    
    def update_offsets(self):
        if self.color == Color.WHITE:
            self.offsets = [Point(0, 1), Point(-1, 1), Point(1, 1)]
            if not self.moved:
                self.offsets.append(Point(0, 2))

class Rook(Piece):
    def __init__(self, piece_name, position, color) -> None:
        super().__init__(piece_name.value, piece_name, position, color)
        self.sliding = True
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

class Knight(Piece):
    def __init__(self, piece_name, position, color) -> None:
        super().__init__(piece_name.value, piece_name, position, color)
        self.sliding = False
        self.offsets = [Point(1, 2), Point(2, 1), Point(-1, 2), Point(2, -1), Point(-1, -2), Point(-2, -1), Point(1, -2), Point(-2, 1)]

class Bishop(Piece):
    def __init__(self, piece_name, position, color) -> None:
        super().__init__(piece_name.value, piece_name, position, color)
        self.sliding = True
        self.offsets = [Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class Queen(Piece):
    def __init__(self, piece_name, position, color) -> None:
        super().__init__(piece_name.value, piece_name, position, color)
        self.sliding = True
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class King(Piece):
    def __init__(self, piece_name, position, color) -> None:
        super().__init__(piece_name.value, piece_name, position, color)
        self.sliding = False
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class PieceFactory:
    def create_piece(self, name, position, color):
        if name == PieceName.PAWN:
            return Pawn(name, position, color)
        elif name == PieceName.ROOK:
            return Rook(name, position, color)
        elif name == PieceName.KNIGHT:
            return Knight(name, position, color)
        elif name == PieceName.BISHOP:
            return Bishop(name, position, color)
        elif name == PieceName.QUEEN:
            return Queen(name, position, color)
        elif name == PieceName.KING:
            return King(name, position, color)
        else:
            raise InvalidPieceTypeError("Invalid piece type")

if __name__ == "__main__":
    factory = PieceFactory()