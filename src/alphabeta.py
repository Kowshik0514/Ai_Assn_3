import chess
from src.evaluation import evaluate_board
import time

class AlphaBetaAgent:
    """Chess agent using the Alpha-Beta pruning algorithm"""
        alpha = float('-inf')
        beta = float('inf')

        moves = list(board.legal_moves)

        ordered_moves = []
        for move in moves:
            if board.is_capture(move) or board.gives_check(move):
                ordered_moves.insert(0, move)
            else:
                ordered_moves.append(move)

        for move in ordered_moves:
            board.push(move)
            value = self.alpha_beta(board, self.depth - 1, alpha, beta, not maximizing)
            board.pop()

            self.nodes_explored += 1

            if maximizing and value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, value)
            elif not maximizing and value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, value)

            if time.time() - start_time > self.max_time:
                print("Time limit reached, stopping search")
                break

        end_time = time.time()
        print(f"Alpha-Beta pruning explored {self.nodes_explored} nodes in {end_time - start_time:.2f} seconds")
        print(f"Best move: {best_move}, Best value: {best_value}")

        return best_move

    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        """
        Alpha-Beta pruning algorithm implementation

        Args:
            board: Chess board
            depth: Current depth in the search tree
            alpha: Alpha value (best value for maximizing player)
            beta: Beta value (best value for minimizing player)
            maximizing: Whether the current player is maximizing

        Returns:
            The best evaluation score
        """

        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        self.nodes_explored += 1

        if maximizing:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self.alpha_beta(board, depth - 1, alpha, beta, False))
                board.pop()

                alpha = max(alpha, value)
                if alpha >= beta:
                    break  
            return value
        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.alpha_beta(board, depth - 1, alpha, beta, True))
                board.pop()

                beta = min(beta, value)
                if beta <= alpha:
                    break  
            return value