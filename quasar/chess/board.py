"""
This module contains the Board class, 
which is responsible for managing the state of the game board.
"""

import math
from logger import logger
from .point import Point
from .pieces import Piece, PieceFactory, PieceColor, PieceName
from .moves import Move
from .utils import fen_to_piece_name
from .errors import InvalidMoveError

class Board:
    """
    The Board class is responsible for managing the state of the game board.
    """
    def __init__(self) -> None:
        """
        The constructor for the Board class.
        """
        self.pieces = []
        self.captured_pieces = []
        self.moves = []

        self.factory = PieceFactory()
        self.none_piece = self.factory.create_piece(PieceName.NONE, Point(0, 0), PieceColor.NONE)

        self.last_concentration = Point(0, 0)

    def create_piece(self, name: PieceName, position: Point, color: PieceColor) -> Piece:
        """
        Create a piece and add it to the board.

        :param name: Name of the piece to create.
        :type name: PieceName
        :param position: The position of the piece.
        :type position: Point
        :param color: The color of the piece.
        :type color: PieceColor
        :return: The created piece.
        :rtype: Piece
        """
        piece = self.factory.create_piece(name, position, color)
        self.add_piece(piece)
        return piece

    def load_fen(self, fen: str) -> None:
        """
        Load a FEN string into the board.

        :param fen: The FEN string to load.
        :type fen: str
        """
        placement, turn, castling, en_passant, halfmove, fullmove = fen.split(" ")
        del turn, castling, en_passant, halfmove, fullmove
        placement = placement.split("/")
        for y, row in enumerate(placement):
            y = 8 - y
            for x, char in enumerate(row):
                if char.isdigit():
                    x += int(char)
                else:
                    color = PieceColor.WHITE if char.isupper() else PieceColor.BLACK
                    piece_name = PieceName[fen_to_piece_name(char)]
                    self.create_piece(piece_name, Point(x+1, y), color)

    def get_pieces(self) -> list:
        """
        Get the pieces on the board.

        :return: The pieces on the board.
        :rtype: list
        """
        return self.pieces

    def add_piece(self, piece: Piece) -> None:
        """
        Add a piece to the board.

        :param piece: The piece to add to the board.
        :type piece: Piece
        """
        self.pieces.append(piece)

    def remove_piece(self, piece: Piece) -> None:
        """
        Remove a piece from the board.

        :param piece: The piece to remove from the board.
        :type piece: Piece
        """
        self.pieces.remove(piece)

    def clear_pieces(self) -> None:
        """
        Clear the pieces from the board.
        """
        self.pieces = []

    def get_concentration_position(self) -> Point:
        """
        Get the concentration position of the pieces on the board.
        Currently, it is not used.

        :return: The concentration position of the pieces on the board.
        :rtype: Point
        """
        new_concentration = self.last_concentration.copy()
        for piece in self.pieces:
            d = abs(piece.get_position() - self.last_concentration)
            d = Point(math.sqrt(d.x), math.sqrt(d.y))
            new_concentration += d
        new_concentration /= len(self.pieces)
        self.last_concentration = new_concentration
        return self.last_concentration

    def get_white_pieces(self) -> list:
        """
        Get the white pieces on the board.

        :return: The white pieces on the board.
        :rtype: list
        """
        return [piece for piece in self.pieces if piece.get_color() == PieceColor.WHITE]

    def get_black_pieces(self) -> list:
        """
        Get the black pieces on the board.

        :return: The black pieces on the board.
        :rtype: list
        """
        return [piece for piece in self.pieces if piece.get_color() == PieceColor.BLACK]

    def get_piece_at(self, position: Point) -> Piece:
        """
        Get the piece at a position on the board.

        :param position: The position to get the piece from.
        :type position: Point
        :return: The piece at the position.
        :rtype: Piece
        """
        self.pieces.sort(key=lambda x: x.get_position() == position, reverse=True)
        for piece in self.pieces:
            if piece.get_position() == position:
                return piece
        return self.none_piece

    def get_possible_moves_generator(self, piece: Piece):
        """
        WIP
        """
        piece_offset_generator = piece.get_offset_generator()
        offset = piece_offset_generator.next()
        while True:
            move = Move(piece.position, piece.position+offset)
            self.validate_move(move)
            if move.legal:
                yield move
            offset = piece_offset_generator.next()


    def capture(self, piece: Piece) -> None:
        """
        Capture a piece on the board.

        :param piece: The piece to capture.
        :type piece: Piece
        """
        self.captured_pieces.append(piece)
        self.pieces.remove(piece)

    def is_move_legal(self, move: Move) -> bool:
        """
        Check if a move is legal according to the rules of chess.

        :param move: The move to check.
        :type move: Move
        :return: True if the move is legal, False otherwise.
        :rtype: bool
        """
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

    def validate_move(self, move: Move) -> None:
        """
        Sets variables of the move object according to the rules of chess.
        Declares if the move is legal or not.

        :param move: The move to validate.
        :type move: Move
        """
        move.moved = self.get_piece_at(move.source)
        moved = move.moved
        move.captured = self.get_piece_at(move.target)
        captured = move.captured

        if not self.is_move_legal(move):
            move.legal = False

        if moved.get_color() == captured.get_color() and move.legal:
            logger.warning("Capture of same color piece")
            move.legal = False

    def make_move(self, legal_move: Move) -> None:
        """
        Makes a move on the board.

        :param validated_move: The move to make. Has to be legal.
        :type validated_move: Move
        :raises InvalidMoveError: If the move is not legal.
        """
        if not legal_move.legal:
            raise InvalidMoveError()

        self.moves.append(legal_move)
        legal_move.moved.set_position(legal_move.target)
        legal_move.moved.moved = True
        try:
            legal_move.moved.update_offsets()
        except AttributeError:
            pass
        if legal_move.captured != self.none_piece:
            self.capture(legal_move.captured)

    def is_check(self) -> bool:
        """
        Check if the current player is in check.

        :return: True if the current player is in check, False otherwise.
        :rtype: bool
        """
        return self.moves[-1].check

    def is_checkmate(self) -> bool:
        """
        Check if the current player is in checkmate.

        :return: True if the current player is in checkmate, False otherwise.
        :rtype: bool
        """
        return self.moves[-1].checkmate

    def print(self) -> None:
        """
        Print the board to the console.
        """
        for y in range(8, 0, -1):
            for x in range(1, 9, 1):
                piece = self.get_piece_at(Point(x, y))
                print(piece.get_fen_char(), end=" ")
            print()

if __name__ == "__main__":
    from pieces import PieceFactory, Color, PieceName
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
