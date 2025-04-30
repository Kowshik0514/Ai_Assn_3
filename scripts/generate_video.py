import sys
import os
import time
import chess
import pygame
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chess_env import ChessEnvironment
from src.minimax import MinimaxAgent
from src.alphabeta import AlphaBetaAgent
from src.visualizer import ChessVisualizer

def generate_game_video(algorithm="alphabeta", depth=3, max_moves=50, display=True):
    """Generate a video of the AI playing chess against itself"""

    env = ChessEnvironment()
    board = env.reset()

    if algorithm.lower() == "minimax":
        white_agent = MinimaxAgent(depth=depth)
        black_agent = MinimaxAgent(depth=depth)
        algo_name = "Minimax"
    else:
        white_agent = AlphaBetaAgent(depth=depth)
        black_agent = AlphaBetaAgent(depth=depth)
        algo_name = "Alpha-Beta"

    visualizer = ChessVisualizer()

    move_count = 0
    last_move = None
    game_over = False

    print(f"Starting chess game with {algo_name} algorithm (depth={depth})")

    while not game_over and move_count < max_moves:

        current_agent = white_agent if board.turn == chess.WHITE else black_agent

        print(f"\nMove {move_count + 1}, {'White' if board.turn == chess.WHITE else 'Black'} to move")

        start_time = time.time()
        move = current_agent.choose_move(board)
        end_time = time.time()

        print(f"Move chosen: {move} in {end_time - start_time:.2f} seconds")

        if move is None:
            print("No legal moves available")
            game_over = True
            break

        board, _, game_over, _ = env.step(move)
        last_move = move
        move_count += 1

        visualizer.capture_frame(board, last_move)

        if display:
            if not visualizer.show(board, last_move):
                break  
            time.sleep(0.5)  

    if game_over:
        result = board.result()
        print(f"\nGame over! Result: {result}")
        if result == "1-0":
            print("White wins!")
        elif result == "0-1":
            print("Black wins!")
        else:
            print("Draw!")
    else:
        print(f"\nReached maximum number of moves ({max_moves})")

    video_name = f"{algo_name.lower()}_depth{depth}_game.mp4"
    visualizer.save_video(video_name)

    pygame.quit()
    return video_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a chess game video")
    parser.add_argument("--algorithm", type=str, default="alphabeta", choices=["minimax", "alphabeta"],
                       help="Algorithm to use (minimax or alphabeta)")
    parser.add_argument("--depth", type=int, default=3, help="Search depth for the algorithm")
    parser.add_argument("--max-moves", type=int, default=50, help="Maximum number of moves")
    parser.add_argument("--no-display", action="store_true", help="Disable display window")

    args = parser.parse_args()

    generate_game_video(
        algorithm=args.algorithm,
        depth=args.depth,
        max_moves=args.max_moves,
        display=not args.no_display
    )