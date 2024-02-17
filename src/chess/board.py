from point import Point
import math
class Board:
    def __init__(self) -> None:
        self.pieces = []
        self.last_concentration = Point(0, 0)
    
    def get_pieces(self):
        return self.pieces
    
    def add_piece(self, piece):
        self.pieces.append(piece)
    
    def remove_piece(self, piece):
        self.pieces.remove(piece)
    
    def clear_pieces(self):
        self.pieces = []
    
    def get_concentration_position(self):
        new_concentration = self.last_concentration.copy()
        for piece in self.pieces:
            d = abs(piece.get_position() - self.last_concentration)
            d = Point(math.sqrt(d.x), math.sqrt(d.y))
            new_concentration += d
        new_concentration /= len(self.pieces)
        self.last_concentration = new_concentration
        return self.last_concentration
    
    def make_move(self, move):
        pass