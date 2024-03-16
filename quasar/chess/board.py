"""
This module contains the Board class, 
which is responsible for managing the state of the game board.
"""

import math
from typing import Tuple
from quasar.logger import logger
from quasar.chess.moves import Move
from quasar.chess.errors import NonePieceError, InvalidMoveError, InvalidPlayerError
from quasar.chess.point import Point
from quasar.chess.pieces import Piece, PieceFactory, PieceColor, PieceName
from quasar.chess.utils import fen_to_piece_name

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

        self.current_player = PieceColor.WHITE

        self.factory = PieceFactory()
        self.none_piece = self.factory.create_piece(PieceName.NONE, Point(0, 0), PieceColor.NONE)

        self.validator = Validator()
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

    def change_player(self) -> None:
        """
        Change the current player.
        """
        if self.current_player == PieceColor.WHITE:
            self.current_player = PieceColor.BLACK
        elif self.current_player == PieceColor.BLACK:
            self.current_player = PieceColor.WHITE
        else:
            raise InvalidPlayerError(
                f"Current player has to be either WHITE or BLACK. Got {self.current_player.name}")

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

    def get_possible_moves_generator(self, piece: Piece,
                                     bottom_left_bound: Point,
                                     top_right_bound: Point):
        """
        _summary_

        :param piece: _description_
        :type piece: Piece
        """
        if piece.color != self.current_player:
            raise InvalidPlayerError(
                f"Current player is {self.current_player.name}, but piece is {piece.color.name}")
        offset_generator = piece.get_offset_generator(bottom_left_bound, top_right_bound)
        misfire = 0
        while misfire < 100:
            try:
                offset = next(offset_generator)
            except StopIteration:
                break
            target = piece.get_position() + offset
            if bottom_left_bound.x <= target.x <= top_right_bound.x and \
                bottom_left_bound.y <= target.y <= top_right_bound.y:
                move = Move(piece.get_color(), piece.get_position(), target)
                move, is_legal = self.validator(move, self)
                if is_legal:
                    yield move
            else:
                misfire += 1

    def capture(self, piece: Piece) -> None:
        """
        Capture a piece on the board.

        :param piece: The piece to capture.
        :type piece: Piece
        """
        self.captured_pieces.append(piece)
        self.pieces.remove(piece)

    def make_move(self, move: Move) -> None:
        """
        Makes a move on the board.

        :param validated_move: The move to make. Has to be legal.
        :type validated_move: Move
        :raises InvalidMoveError: If the move is not legal.
        """

        legal_move, is_legal = self.validator(move, self)

        if not is_legal:
            raise InvalidMoveError()

        self.change_player()

        self.moves.append(legal_move)
        legal_move.moved.set_position(legal_move.target)
        legal_move.moved.moved = True
        try:
            legal_move.moved.update_offsets()
        except AttributeError:
            pass
        if legal_move.captured != self.none_piece:
            self.capture(legal_move.captured)

    def undo_move(self) -> None:
        """
        Undo the last move made on the board.
        """
        move = self.moves.pop()
        move.moved.set_position(move.source)
        self.pieces.append(move.captured)
        move.moved.moved = False
        try:
            move.moved.update_offsets()
        except AttributeError:
            pass

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

class Validator:
    """
    This class is responsible for validating moves.
    """
    def __call__(self, move_to_validate: Move, board_state: Board) -> Tuple[Move, bool]:
        """
        This method performs all the logic to categorize move as legal or illegal.

        :param move: Move to be validated.
        :type move: Move
        :param board: Board on which the move is to be played.
        :type board: Board
        :return: Validated move.
        :rtype: Move
        """
        move_to_validate.moved = board_state.get_piece_at(move_to_validate.source)
        move_to_validate.captured = board_state.get_piece_at(move_to_validate.target)

        if not self.is_move_legal(move_to_validate, board_state):
            move_to_validate.legal = False

        return move_to_validate, move_to_validate.legal

    def is_move_legal(self, move: Move, board: Board) -> bool:
        piece = move.moved

        if piece is board.none_piece:
            logger.error("No piece at %s", move.source)
            raise NonePieceError(f"No piece at {move.source}")

        if move.source == move.target:
            log_msg = f"{str(move)} | Source and target are the same"
            logger.warning(log_msg)
            return False

        if move.source != piece.position:
            log_msg = f"{str(move)} | Source and piece position are different"
            logger.warning(log_msg)
            return False
        if not piece.sliding:
            if move.target not in [piece.position + offset for offset in piece.offsets]:
                log_msg = f"{str(move)} | Move not in piece's offsets"
                logger.warning(log_msg)
                return False
        else:
            pass
        return True

if __name__ == "__main__":
    from quasar.chess.pieces import PieceName, PieceFactory, PieceColor
    from quasar.chess.utils import STARTING_FEN
    board = Board()
    board.load_fen(STARTING_FEN)
    validator = Validator()
    move = Move(PieceColor.WHITE, (1, 0), (2, 0))
    print(validator(move, board))

if __name__ == "__main__":
    pass
