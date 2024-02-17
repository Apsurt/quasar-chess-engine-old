
class Move:
    def __init__(self, source, target) -> None:
        self.source = source
        self.target = target
        self.moved = None
        self.captured = None
        self.promotion = None
        self.castling = False
        self.en_passant = False
        self.check = False
        self.checkmate = False
        self.legal = True