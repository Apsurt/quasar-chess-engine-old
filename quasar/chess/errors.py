"""
This module contains the custom errors for the chess game.
"""

class BaseChessError(Exception):
    """
    Base class for all chess errors.

    :param Exception: The base exception class.
    :type Exception: Exception
    """

class InvalidMoveError(BaseChessError):
    """
    Raised when an invalid move is attempted.

    :param BaseChessError: The base chess error class.
    :type BaseChessError: BaseChessError
    """

class NonePieceError(BaseChessError):
    """
    Raised when an attempt is made to move the none piece.

    :param BaseChessError: The base chess error class.
    :type BaseChessError: BaseChessError
    """

class InvalidPositionError(BaseChessError):
    """
    Raised when an invalid position is attempted.

    :param BaseChessError: The base chess error class.
    :type BaseChessError: BaseChessError
    """

class InvalidPieceError(BaseChessError):
    """
    Raised when an invalid piece is attempted.

    :param BaseChessError: The base chess error class.
    :type BaseChessError: BaseChessError
    """

class InvalidPieceTypeError(BaseChessError):
    """
    Raised when an invalid piece type is attempted.

    :param BaseChessError: The base chess error class.
    :type BaseChessError: BaseChessError
    """

class EmptyPositionError(BaseChessError):
    """
    Raised when an empty position is attempted.

    :param BaseChessError: The base chess error class.
    :type BaseChessError: BaseChessError
    """
