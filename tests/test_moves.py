from quasar.chess.moves import Move

def test_move_initialization():
    move = Move("e2", "e4")
    assert move.source == "e2"
    assert move.target == "e4"
    assert move.moved is None
    assert move.captured is None
    assert move.promotion is None
    assert move.castling is False
    assert move.en_passant is False
    assert move.check is False
    assert move.checkmate is False
    assert move.legal is True