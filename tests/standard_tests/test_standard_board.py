import pytest
from quasar.chess.board import Board
from quasar.chess.point import Point
from quasar.chess.pieces import PieceName, PieceColor

class TestBoard:
    def test_create_piece(self):
        board = Board()
        piece = board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        assert piece in board.get_pieces()

    def test_load_fen(self):
        board = Board()
        board.load_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        assert len(board.get_pieces()) == 32

    def test_add_piece(self):
        board = Board()
        piece = board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        board.add_piece(piece)
        assert piece in board.get_pieces()

    def test_remove_piece(self):
        board = Board()
        piece = board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        board.remove_piece(piece)
        assert piece not in board.get_pieces()

    def test_clear_pieces(self):
        board = Board()
        piece = board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        board.add_piece(piece)
        board.clear_pieces()
        assert len(board.get_pieces()) == 0

    def test_get_concentration_position(self):
        board = Board()
        piece1 = board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        piece2 = board.create_piece(PieceName.ROOK, Point(1, 1), PieceColor.WHITE)
        board.add_piece(piece1)
        board.add_piece(piece2)
        assert board.get_concentration_position() == Point(0.5, 0.5)

    def test_get_white_pieces(self):
        board = Board()
        board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        board.create_piece(PieceName.ROOK, Point(1, 1), PieceColor.BLACK)
        assert len(board.get_white_pieces()) == 1

    def test_get_black_pieces(self):
        board = Board()
        board.create_piece(PieceName.ROOK, Point(0, 0), PieceColor.WHITE)
        board.create_piece(PieceName.ROOK, Point(1, 1), PieceColor.BLACK)
        assert len(board.get_black_pieces()) == 1
