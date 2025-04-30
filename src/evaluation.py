import chess
import numpy as np

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

PAWN_TABLE = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
])

KNIGHT_TABLE = np.array([
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
])

BISHOP_TABLE = np.array([
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5,  5,  5,  5,  5,-10,
    -10,  0,  5,  0,  0,  5,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
])

ROOK_TABLE = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
])

QUEEN_TABLE = np.array([
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
])

KING_TABLE_MIDDLEGAME = np.array([
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
])

KING_TABLE_ENDGAME = np.array([
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
])

PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE_MIDDLEGAME  
}

def evaluate_board(board):
    """
    Evaluate the current board position.
    Positive score means advantage for white, negative for black.
    """
    if board.is_checkmate():

        return -10000 if board.turn else 10000

    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_fifty_moves() or board.is_repetition():
        return 0  

    score = 0

    piece_count = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
    total_pieces = len(list(board.pieces(chess.PAWN, chess.WHITE))) + len(list(board.pieces(chess.PAWN, chess.BLACK))) + \
                   len(list(board.pieces(chess.KNIGHT, chess.WHITE))) + len(list(board.pieces(chess.KNIGHT, chess.BLACK))) + \
                   len(list(board.pieces(chess.BISHOP, chess.WHITE))) + len(list(board.pieces(chess.BISHOP, chess.BLACK))) + \
                   len(list(board.pieces(chess.ROOK, chess.WHITE))) + len(list(board.pieces(chess.ROOK, chess.BLACK))) + \
                   len(list(board.pieces(chess.QUEEN, chess.WHITE))) + len(list(board.pieces(chess.QUEEN, chess.BLACK)))

    is_endgame = piece_count == 0 or total_pieces <= 12

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:

            value = PIECE_VALUES[piece.piece_type]

            row = 7 - (square // 8)  
            col = square % 8
            square_idx = row * 8 + col

            if piece.piece_type == chess.KING and is_endgame:
                square_value = KING_TABLE_ENDGAME[square_idx]
            else:
                square_value = PIECE_SQUARE_TABLES[piece.piece_type][square_idx]

            if not piece.color:
                square_idx = 63 - square_idx  
                if piece.piece_type == chess.KING and is_endgame:
                    square_value = KING_TABLE_ENDGAME[square_idx]
                else:
                    square_value = PIECE_SQUARE_TABLES[piece.piece_type][square_idx]
                value = -value
                square_value = -square_value

            score += value + square_value

    legal_moves = list(board.legal_moves)
    move_count = len(legal_moves)

    board.turn = not board.turn
    opponent_moves = len(list(board.legal_moves))
    board.turn = not board.turn

    mobility_score = (move_count - opponent_moves) * 0.1
    if not board.turn:  
        mobility_score = -mobility_score

    score += mobility_score

    for file in range(8):
        white_pawns = 0
        black_pawns = 0
        for rank in range(8):
            square = rank * 8 + file
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.PAWN:
                if piece.color:  
                    white_pawns += 1
                else:  
                    black_pawns += 1

        if white_pawns > 1:
            score -= (white_pawns - 1) * 20
        if black_pawns > 1:
            score += (black_pawns - 1) * 20

    return score