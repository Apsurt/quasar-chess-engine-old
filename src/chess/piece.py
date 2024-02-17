from point import Point
from errors import InvalidPieceTypeError
from enum import Enum

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
    def __init__(self, _id=PieceName.NONE.value, name=PieceName.NONE, position=None, color=Color.NONE) -> None:
        self.id = _id
        self.name = name
        self.color = color
        if not isinstance(position, Point):
            raise InvalidPieceTypeError("Invalid position type")
        self.position = position
        self.moved = False
        self.sliding = False
    
    def get_position(self):
        return self.position
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color

class Pawn(Piece):
    def __init__(self, position) -> None:
        super().__init__(1, "pawn", position)
        self.sliding = False
        self.offsets = []
        self.update_offsets()
    
    def update_offsets(self):
        if self.color == Color.WHITE:
            self.offsets = [Point(0, 1), Point(-1, 1), Point(1, 1)]
            if not self.moved:
                self.offsets.append(Point(0, 2))

class Rook(Piece):
    def __init__(self, position) -> None:
        super().__init__(2, "rook", position)
        self.sliding = True
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

class Knight(Piece):
    def __init__(self, position) -> None:
        super().__init__(3, "knight", position)
        self.sliding = False
        self.offsets = [Point(1, 2), Point(2, 1), Point(-1, 2), Point(2, -1), Point(-1, -2), Point(-2, -1), Point(1, -2), Point(-2, 1)]

class Bishop(Piece):
    def __init__(self, position) -> None:
        super().__init__(4, "bishop", position)
        self.sliding = True
        self.offsets = [Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class Queen(Piece):
    def __init__(self, position) -> None:
        super().__init__(5, "queen", position)
        self.sliding = True
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class King(Piece):
    def __init__(self, position) -> None:
        super().__init__(6, "king", position)
        self.sliding = False
        self.offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 1), Point(-1, 1), Point(-1, -1), Point(1, -1)]

class PieceFactory:
    def create_piece(self, name, position, color):
        if name == PieceName.PAWN:
            return Pawn(position, color)
        elif name == PieceName.ROOK:
            return Rook(position, color)
        elif name == PieceName.KNIGHT:
            return Knight(position, color)
        elif name == PieceName.BISHOP:
            return Bishop(position, color)
        elif name == PieceName.QUEEN:
            return Queen(position, color)
        elif name == PieceName.KING:
            return King(position, color)
        else:
            raise InvalidPieceTypeError("Invalid piece type")

if __name__ == "__main__":
    factory = PieceFactory()
    print(factory.create_piece(PieceName.PAWN, Point(0, 0)).id)