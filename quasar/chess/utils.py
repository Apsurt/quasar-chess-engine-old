"""
This module contains utility functions for the chess package.
"""

#Built-in imports
from typing import Literal

#Internal imports
from .point import Point

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
POSITION_5_FEN = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"

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

def fen_to_piece_name(
    char: Literal["P","N","B","R","Q","K"]
    ) -> Literal["PAWN","KNIGHT","BISHOP","ROOK","QUEEN","KING", "NONE"]:
    """
    Convert a character representing a piece in FEN notation to its full name

    :param char: character representing a piece in FEN notation
    :type char: Literal["P", "N", "B", "R", "Q", "K"]
    :return: full name of the piece
    :rtype: Literal["PAWN", "KNIGHT", "BISHOP", "ROOK", "QUEEN", "KING", "NONE"]
    """
    char = char.upper()
    piece_dict = {"P": "PAWN",
                  "N": "KNIGHT", 
                  "B": "BISHOP", 
                  "R": "ROOK", 
                  "Q": "QUEEN", 
                  "K": "KING"}
    try:
        return piece_dict[char]
    except KeyError:
        return "NONE"
