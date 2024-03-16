"""
This is the main file of the chess package.
It contains the main classes and functions of the package.
"""

__title__ = "chess"

from .board import Board
from .pieces import Piece, PieceFactory, PieceColor, PieceName
from .move_validator import Validator
from .moves import Move
from .point import Point
from .utils import *
from .errors import *
