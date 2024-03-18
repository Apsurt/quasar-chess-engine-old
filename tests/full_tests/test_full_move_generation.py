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
        #depths = range(1,7)
        depths = range(1,4)
        expected_count = [20,
                          400,
                          8_902,
                          197_281,
                          4_865_609,
                          119_060_324]

        for depth in depths:
            board.clear()
            board.load_fen(STARTING_FEN)
            position_count = self.position_count(depth, board)
            print(f"Depth: {depth}, Positions: {position_count}")
            assert position_count == expected_count[depth-1]

    def test_move_generation_from_position_5(self):
        """
        Test the move generation from position 5.
        """
        board = Board()
        #depths = range(1,6)
        depths = range(1,3)
        expected_count = [44,
                          1_486,
                          62_379,
                          2_103_487,
                          89_941_194]

        for depth in depths:
            board.clear()
            board.load_fen(POSITION_5_FEN)
            position_count = self.position_count(depth, board)
            print(f"Depth: {depth}, Positions: {position_count}")
            assert position_count == expected_count[depth-1]

    def position_count(self, depth: int, board: Board) -> int:
        """
        Count the number of positions at a given depth.
        """
        if depth == 0:
            return 1

        count = 0
        pieces = board.get_pieces().copy()
        for piece in pieces:
            if piece.color == board.current_player:
                generator = board.get_possible_moves_generator(piece, Point(1,1), Point(8,8))
                possible_moves = list(generator)
                for move in possible_moves:
                    board.make_move(move)
                    count += self.position_count(depth - 1, board)
                    board.undo_move()
        return count

if __name__ == "__main__":
    TestMoveGeneration().test_move_generation_from_starting_position()
