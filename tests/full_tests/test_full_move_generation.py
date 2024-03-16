from quasar.chess.board import Board
from quasar.chess.utils import STARTING_FEN, POSITION_5_FEN

class TestMoveGeneration:
    """
    Test the move generation from different positions.
    """
    def test_move_generation_from_starting_position(self):
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
            assert self.position_count(depth, board) == expected_count[depth - 1]

    def test_move_generation_from_position_5(self):
        pass

    def position_count(self, depth: int, board: Board) -> int:
        """
        Count the number of positions at a given depth.
        """
        if depth == 0:
            return 1

        count = 0
        possible_moves = []
        for move in possible_moves:
            board.make_move(move)
            count += self.position_count(depth - 1, board)
            board.undo_move()

        return count
