import chess
import numpy as np
from typing import Dict, List, Tuple

class ChessEnvironment:
    def __init__(self):
        self.board = chess.Board()
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # King's value not used in material counting
        }
        
    def reset(self):
        """Reset the board to initial position"""
        self.board = chess.Board()
        return self.get_state()
        
    def get_state(self):
        """Get current state of the game"""
        return {
            'board': self.board,
            'legal_moves': list(self.board.legal_moves),
            'is_terminal': self.board.is_game_over()
        }
        
    def apply_move(self, move):
        """Apply a move and return new state, reward, and whether game is over"""
        # Store material count before move
        material_before = self._get_material_count()
        
        # Make the move
        self.board.push(move)
        
        # Calculate reward
        material_after = self._get_material_count()
        material_reward = material_after - material_before
        
        # Additional rewards/penalties
        position_reward = 0
        if self.board.is_checkmate():
            position_reward = 100 if self.board.turn else -100
        elif self.board.is_stalemate():
            position_reward = 0
        elif self.board.is_check():
            position_reward = -1 if self.board.turn else 1
            
        total_reward = material_reward + position_reward
        
        return self.get_state(), total_reward, self.board.is_game_over()
        
    def _get_material_count(self):
        """Calculate material advantage (positive for white, negative for black)"""
        total = 0
        for piece_type in self.piece_values:
            white_pieces = len(self.board.pieces(piece_type, chess.WHITE))
            black_pieces = len(self.board.pieces(piece_type, chess.BLACK))
            total += self.piece_values[piece_type] * (white_pieces - black_pieces)
        return total
        
    def is_game_over(self):
        """Check if game is over"""
        return self.board.is_game_over()
        
    def get_result(self):
        """Get game result"""
        if not self.board.is_game_over():
            return None
        return self.board.result()
        
    def get_legal_moves(self) -> List[chess.Move]:
        """Get list of legal moves"""
        return list(self.board.legal_moves)
        
    def render(self):
        """Print the current board state"""
        print(self.board) 