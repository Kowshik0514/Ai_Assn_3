from typing import List, Tuple
import chess
import numpy as np
from chess_env import ChessEnvironment

class MinimaxChess:
    def __init__(self, env: ChessEnvironment, depth: int = 3):
        self.env = env
        self.depth = depth
        
    def get_best_move(self, board: chess.Board) -> chess.Move:
        """Find the best move using minimax algorithm"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
            
        best_value = float('-inf')
        best_move = legal_moves[0]
        
        for move in legal_moves:
            # Make move
            board.push(move)
            
            # Get value from minimax
            value = self._minimax(board, self.depth - 1, False)
            
            # Undo move
            board.pop()
            
            # Update best move
            if value > best_value:
                best_value = value
                best_move = move
                
        return best_move
        
    def _minimax(self, board: chess.Board, depth: int, is_maximizing: bool) -> float:
        """Minimax algorithm implementation"""
        if depth == 0 or board.is_game_over():
            return self._evaluate_position(board)
            
        if is_maximizing:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self._minimax(board, depth - 1, False))
                board.pop()
            return value
        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self._minimax(board, depth - 1, True))
                board.pop()
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