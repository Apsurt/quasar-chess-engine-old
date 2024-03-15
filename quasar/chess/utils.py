# This file contains utility functions for the chess module

#Internal imports
from .point import Point

#Built-in imports
from typing import Literal

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def standard_notation_to_point(square: str) -> Point:
    """
    Convert a square in standard notation (e.g. e2) to a Point object (e.g. Point(5, 2))

    :param square: string representing a square in standard notation (e.g. e2)
    :type square: str
    :raises ValueError: when square has length different than 2
    :raises ValueError: when square[1] is not a digit
    :raises ValueError: when square[0] is not a letter representing a file
    :return: Point equivalent to the square in standard notation
    :rtype: Point
    """
    if len(square) != 2:
        raise ValueError("Invalid square notation")
    if square[1] not in "12345678":
        raise ValueError("Invalid square notation")
    if square[0] not in "abcdefgh":
        raise ValueError("Invalid square notation")
    file = ord(square[0]) - ord('a') + 1
    rank = int(square[1])
    return Point(file, rank)

def fen_to_piece_name(char: Literal["P","N","B","R","Q","K"]) -> Literal["PAWN","KNIGHT","BISHOP","ROOK","QUEEN","KING"]:
    """
    Convert a character representing a piece in FEN notation to its full name

    :param char: character representing a piece in FEN notation
    :type char: Literal[&quot;P&quot;, &quot;N&quot;, &quot;B&quot;, &quot;R&quot;, &quot;Q&quot;, &quot;K&quot;]
    :return: full name of the piece
    :rtype: Literal[&quot;PAWN&quot;, &quot;KNIGHT&quot;, &quot;BISHOP&quot;, &quot;ROOK&quot;, &quot;QUEEN&quot;, &quot;KING&quot;]
    """
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