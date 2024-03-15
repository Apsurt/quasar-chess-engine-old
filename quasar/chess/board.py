from .point import Point
from .pieces import Piece, PieceFactory, Color, PieceName
from .utils import fen_to_piece_name
from .logger import logger

import math

class Board:
    def __init__(self) -> None:
        self.none_piece = Piece()
        self.pieces = []
        self.captured_pieces = []
        self.moves = []

        self.factory = PieceFactory()
        
        self.last_concentration = Point(0, 0)
    
    def create_piece(self, name, position, color):
        piece = self.factory.create_piece(name, position, color)
        self.add_piece(piece)
        return piece
    
    def load_fen(self, fen):
        placement, turn, castling, en_passant, halfmove, fullmove = fen.split(" ")
        placement = placement.split("/")
        for y, row in enumerate(placement):
            y = 8 - y
            for x, char in enumerate(row):
                if char.isdigit():
                    x += int(char)
                else:
                    color = Color.WHITE if char.isupper() else Color.BLACK
                    piece_name = PieceName[fen_to_piece_name(char)]
                    self.create_piece(piece_name, Point(x+1, y), color)
    
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
    
    def get_white_pieces(self):
        return [piece for piece in self.pieces if piece.get_color() == Color.WHITE]

    def get_black_pieces(self):
        return [piece for piece in self.pieces if piece.get_color() == Color.BLACK]
    
    def get_piece_at(self, position):
        self.pieces.sort(key=lambda x: x.get_position() == position, reverse=True)
        for piece in self.pieces:
            if piece.get_position() == position:
                return piece
        return self.none_piece
    
    def get_possible_moves_generator(self, piece):
        offset_generator = piece.get_offset_generator()
        offset = offset_generator.__next__()
        while True:
            move = Move(piece.position, piece.position+offset)
            self.validate_move(move)
            if move.legal:
                yield move
            offset = offset_generator.__next__()
            
    
    def capture(self, piece):
        self.captured_pieces.append(piece)
        self.pieces.remove(piece)
    
    def is_move_legal(self, move):
        piece = move.moved
        if move.source == move.target:
            logger.warning("Source and target are the same")
            return False
        if move.source != piece.position:
            logger.warning("Source and piece position are different")
            return False
        if not piece.sliding:
            if move.target not in [piece.position + offset for offset in piece.offsets]:
                logger.warning("Invalid move")
                return False
        else:
            pass
        return True
    
    def validate_move(self, move):
        move.moved = self.get_piece_at(move.source)
        moved = move.moved
        move.captured = self.get_piece_at(move.target)
        captured = move.captured

        if not self.is_move_legal(move):
            move.legal = False
        
        if moved.get_color() == captured.get_color() and move.legal:
            logger.warning("Capture of same color piece")
            move.legal = False
    
    def make_move(self, validated_move):
        if not validated_move.legal:
            raise Exception()
        
        self.moves.append(validated_move)
        validated_move.moved.set_position(validated_move.target)
        validated_move.moved.moved = True
        try:
            validated_move.moved.update_offsets()
        except AttributeError:
            pass
        if validated_move.captured != self.none_piece:
            self.capture(validated_move.captured)
    
    def is_check(self):
        return self.moves[-1].check
    
    def is_checkmate(self):
        return self.moves[-1].checkmate
    
    def print(self):
        for y in range(8, 0, -1):
            for x in range(1, 9, 1):
                piece = self.get_piece_at(Point(x, y))
                print(piece.get_fen_char(), end=" ")
            print()

if __name__ == "__main__":
    from pieces import Piece, PieceFactory, Color, PieceName
    from moves import Move
    board = Board()
    factory = PieceFactory()
    board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board.print()
    test_move = Move(Point(1, 2), Point(1, 2))
    board.validate_move(test_move)
    print()
    board.print()
    bishop = board.get_piece_at(Point(4, 1))
    print(bishop)
    offset_generator = bishop.get_offset_generator()