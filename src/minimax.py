import chess
from src.evaluation import evaluate_board
import time

class MinimaxAgent:
    
    def __init__(self, depth=3):
        self.depth = depth
        self.nodes_explored = 0
        self.max_time = 60
        
    def choose_move(self, board):
        self.nodes_explored = 0
        start_time = time.time()
        maximizing = board.turn == chess.WHITE
        
        best_move = None
        best_value = float('-inf') if maximizing else float('inf')
        
        moves = list(board.legal_moves)
        
        for move in moves:
            board.push(move)
            value = self.minimax(board, self.depth - 1, not maximizing)
            board.pop()
            
            self.nodes_explored += 1
            
            if maximizing and value > best_value:
                best_value = value
                best_move = move
            elif not maximizing and value < best_value:
                best_value = value
                best_move = move
                
            if time.time() - start_time > self.max_time:
                print("Time limit reached, stopping search")
                break
                
        end_time = time.time()
        print(f"Minimax explored {self.nodes_explored} nodes in {end_time - start_time:.2f} seconds")
        print(f"Best move: {best_move}, Best value: {best_value}")
        
        return best_move
        
    def minimax(self, board, depth, maximizing):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)
            
        self.nodes_explored += 1
            
        if maximizing:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self.minimax(board, depth - 1, False))
                board.pop()
            return value
        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.minimax(board, depth - 1, True))
                board.pop()
            return value
