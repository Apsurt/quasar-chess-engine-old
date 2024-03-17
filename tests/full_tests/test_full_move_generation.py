"""
Test the move generation from different positions.
"""

from quasar.chess.board import Board
from quasar.chess.point import Point
from quasar.chess.utils import STARTING_FEN, POSITION_5_FEN

class TestMoveGeneration:
    """
    Test the move generation from different positions.
    """
    def test_move_generation_from_starting_position(self):
        """
        Test the move generation from the starting position.
        """
        board = Board()
        depths = range(1, 5)
        expected_count = [20,
                          400,
                          8_902,
                          197_281,
                          4_865_609,
                          119_060_324,
                          3_195_901_860,
                          84_998_978_956]

        for depth in depths:
            board.load_fen(STARTING_FEN)
            position_count = self.position_count(depth, board)
            assert position_count == expected_count[depth - 1]

    def test_move_generation_from_position_5(self):
        """
        Test the move generation from position 5.
        """
        board = Board()
        depths = range(1, 2)
        expected_count = [0,0,0,0,0,0]

        for depth in depths:
            board.load_fen(POSITION_5_FEN)
            position_count = self.position_count(depth, board)
            assert position_count == expected_count[depth - 1]

    def position_count(self, depth: int, board: Board) -> int:
        """
        Count the number of positions at a given depth.
        """
        if depth == 0:
            return 1

        count = 0
        possible_moves = []
        for piece in board.get_pieces():
            if piece.color != board.current_player:
                continue
            generator = board.get_possible_moves_generator(piece, Point(1,1), Point(8,8))
            i = 0
            while i < 10000:
                i += 1
                try:
                    move = next(generator)
                    possible_moves.append(move)
                except StopIteration:
                    break
        for move in possible_moves:
            board.make_move(move)
            count += self.position_count(depth - 1, board)
            board.undo_move()

        return count
