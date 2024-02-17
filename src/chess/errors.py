class BaseChessError(Exception):
    pass

class InvalidMoveError(BaseChessError):
    pass

class InvalidPositionError(BaseChessError):
    pass

class InvalidPieceError(BaseChessError):
    pass

class InvalidPieceTypeError(BaseChessError):
    pass