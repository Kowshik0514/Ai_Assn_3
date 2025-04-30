from typing import List, Tuple
import chess
import numpy as np
from chess_env import ChessEnvironment

class AlphaBetaChess:
    def __init__(self, env: ChessEnvironment, depth: int = 3):
        self.env = env
        self.depth = depth
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
    def evaluate_position(self, board: chess.Board) -> float:
        """Evaluate the current board position"""
        # Material balance
        material = 0.0
        for piece_type in self.piece_values:
            white_pieces = len(board.pieces(piece_type, chess.WHITE))
            black_pieces = len(board.pieces(piece_type, chess.BLACK))
            material += self.piece_values[piece_type] * (white_pieces - black_pieces)
            
        # Mobility (number of legal moves)
        mobility = len(list(board.legal_moves))
        if board.turn == chess.BLACK:
            mobility = -mobility
            
        # King safety
        king_safety = 0
        if board.is_check():
            king_safety = -0.5 if board.turn == chess.WHITE else 0.5
            
        # Center control
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        center_control = 0
        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    center_control += 0.1
                else:
                    center_control -= 0.1
                    
        # Piece activity
        piece_activity = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Calculate number of squares controlled by this piece
                if piece.color == chess.WHITE:
                    piece_activity += 0.05
                else:
                    piece_activity -= 0.05
                    
        # Combine all factors
        evaluation = (
            material +  # Material balance (most important)
            0.1 * mobility +  # Mobility
            0.5 * king_safety +  # King safety
            0.2 * center_control +  # Center control
            0.1 * piece_activity  # Piece activity
        )
        
        return evaluation
        
    def get_best_move(self, board: chess.Board) -> chess.Move:
        """Find the best move using alpha-beta pruning"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
            
        best_value = float('-inf')
        best_move = legal_moves[0]
        alpha = float('-inf')
        beta = float('inf')
        
        for move in legal_moves:
            # Make move
            board.push(move)
            
            # Get value from alpha-beta
            value = self._alpha_beta(board, self.depth - 1, alpha, beta, False)
            
            # Undo move
            board.pop()
            
            # Update best move
            if value > best_value:
                best_value = value
                best_move = move
                
            # Update alpha
            alpha = max(alpha, best_value)
            
        return best_move
        
    def _alpha_beta(self, board: chess.Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """Alpha-beta pruning algorithm implementation"""
        if depth == 0 or board.is_game_over():
            return self._evaluate_position(board)
            
        if is_maximizing:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self._alpha_beta(board, depth - 1, alpha, beta, False))
                board.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cutoff
            return value
        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self._alpha_beta(board, depth - 1, alpha, beta, True))
                board.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return value
            
    def _evaluate_position(self, board: chess.Board) -> float:
        """Evaluate the current position"""
        if board.is_checkmate():
            return float('-inf') if board.turn else float('inf')
            
        if board.is_stalemate():
            return 0.0
            
        # Material counting
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        value = 0.0
        for piece_type in piece_values:
            value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
            
        # Mobility (number of legal moves)
        if board.turn == chess.WHITE:
            value += len(list(board.legal_moves)) * 0.1
        else:
            board.turn = chess.WHITE
            value -= len(list(board.legal_moves)) * 0.1
            board.turn = chess.BLACK
            
        return value 