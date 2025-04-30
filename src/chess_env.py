import gym
import gym_chess
import chess
import numpy as np

class ChessEnvironment:
    """Wrapper around gym-chess environment for our AI implementation"""

    def __init__(self):
        self.env = gym.make('Chess-v0')
        self.board = chess.Board()
        self.reset()

    def reset(self):
        """Reset the environment to the starting position"""
        self.env.reset()
        self.board = chess.Board()
        return self.board

    def step(self, move):
        """Take a step in the environment with the given move"""

        if isinstance(move, chess.Move):
            move_uci = move.uci()
        else:
            move_uci = move
            move = chess.Move.from_uci(move)

        observation, reward, done, info = self.env.step(move)

        self.board.push(move)

        return self.board, reward, done, info

    def get_legal_moves(self):
        """Get all legal moves for the current position"""
        return list(self.board.legal_moves)

    def is_game_over(self):
        """Check if the game is over"""
        return self.board.is_game_over()

    def get_result(self):
        """Get the result of the game"""
        if not self.is_game_over():
            return None

        result = self.board.result()
        if result == "1-0":
            return 1  
        elif result == "0-1":
            return -1  
        else:
            return 0  

    def get_board(self):
        """Get the current board state"""
        return self.board

    def render(self):
        """Render the current board state"""
        return self.env.render(mode="rgb_array")