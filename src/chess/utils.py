from point import Point

starting_fence = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def standard_notation_to_point(square: str) -> int:
    if len(square) != 2:
        raise ValueError("Invalid square notation")
    if square[1] not in "12345678":
        raise ValueError("Invalid square notation")
    if square[0] not in "abcdefgh":
        raise ValueError("Invalid square notation")
    file = ord(square[0]) - ord('a') + 1
    rank = int(square[1])
    return Point(file, rank)

def fen_to_piece_name(char: str) -> str:
    char = char.upper()
    if char == "P":
        return "PAWN"
    if char == "N":
        return "KNIGHT"
    if char == "B":
        return "BISHOP"
    if char == "R":
        return "ROOK"
    if char == "Q":
        return "QUEEN"
    if char == "K":
        return "KING"
    return "NONE"