import chess
import time
from chess_env import ChessEnvironment
from minimax import MinimaxChess
from alpha_beta import AlphaBetaChess
from video_recorder import ChessVideoRecorder

def play_game(env: ChessEnvironment, minimax_player: MinimaxChess, 
             alpha_beta_player: AlphaBetaChess, recorder: ChessVideoRecorder,
             game_number: int):
    """Play a single game and record it"""
    # Reset environment and recorder
    env.reset()
    recorder.reset()
    
    # Record initial position
    recorder.add_frame(env.board)
    
    # Game loop
    while not env.is_game_over():
        # Get current state
        state = env.get_state()
        board = state['board']
        
        # Choose player based on turn
        if board.turn == chess.WHITE:
            # White uses Alpha-Beta pruning
            move = alpha_beta_player.get_best_move(board)
            print("White (Alpha-Beta) moves:", move.uci())
        else:
            # Black uses Minimax
            move = minimax_player.get_best_move(board)
            print("Black (Minimax) moves:", move.uci())
            
        # Record position before move
        recorder.add_frame(board, move)
        
        # Apply move
        new_state, reward, is_terminal = env.apply_move(move)
        
        # Print move and reward
        print(f"Reward: {reward:.2f}")
        print("-" * 50)
        
        # Small delay for readability
        time.sleep(1)
        
    # Save video
    recorder.save_video(f"chess_game_{game_number}.mp4")
    
    # Print result
    print("\nGame Over!")
    print("Result:", env.get_result())
    return env.get_result()

def main():
    # Initialize environment and AI players
    env = ChessEnvironment()
    minimax_player = MinimaxChess(env, depth=3)
    alpha_beta_player = AlphaBetaChess(env, depth=3)
    recorder = ChessVideoRecorder()
    
    # Play multiple games
    num_games = 3  # Number of games to play
    results = []
    
    for game_num in range(1, num_games + 1):
        print(f"\nStarting Game {game_num}")
        result = play_game(env, minimax_player, alpha_beta_player, recorder, game_num)
        results.append(result)
        
    # Print summary
    print("\nGame Summary:")
    for i, result in enumerate(results, 1):
        print(f"Game {i}: {result}")
        
    # Calculate statistics
    white_wins = results.count("1-0")
    black_wins = results.count("0-1")
    draws = results.count("1/2-1/2")
    
    print("\nFinal Statistics:")
    print(f"Alpha-Beta (White) wins: {white_wins}")
    print(f"Minimax (Black) wins: {black_wins}")
    print(f"Draws: {draws}")
    
if __name__ == "__main__":
    main() 