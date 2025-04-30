import sys
import os
import chess
import pygame
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chess_env import ChessEnvironment
from src.minimax import MinimaxAgent
from src.alphabeta import AlphaBetaAgent
from src.visualizer import ChessVisualizer

def main():
    """Run a simple chess game with visualization"""
    print("=== Chess AI with Minimax and Alpha-Beta Pruning ===")

    print("\nChoose algorithm:")
    print("1. Minimax")
    print("2. Alpha-Beta Pruning (recommended)")
    try:
        choice = int(input("Enter choice (1 or 2): ").strip())
        if choice not in [1, 2]:
            choice = 2  
    except:
        choice = 2  

    print("\nChoose search depth:")
    print("Higher depth = stronger play but slower computation")
    try:
        depth = int(input("Enter depth (2-4 recommended): ").strip())
        if depth < 1 or depth > 5:
            depth = 3  
    except:
        depth = 3  

    env = ChessEnvironment()
    board = env.reset()

    if choice == 1:
        white_agent = MinimaxAgent(depth=depth)
        black_agent = MinimaxAgent(depth=depth)
        algorithm_name = "Minimax"
    else:
        white_agent = AlphaBetaAgent(depth=depth)
        black_agent = AlphaBetaAgent(depth=depth)
        algorithm_name = "Alpha-Beta"

    visualizer = ChessVisualizer()

    try:
        record_video = input("\nRecord video? (y/n): ").strip().lower() == 'y'
    except:
        record_video = True

    max_moves = 30  
    move_count = 0
    last_move = None
    game_over = False

    print(f"\nStarting chess game with {algorithm_name} algorithm (depth={depth})")
    print("Press Ctrl+C to stop the game at any time.")

    try:

        while not game_over and move_count < max_moves:

            current_agent = white_agent if board.turn == chess.WHITE else black_agent
            player = "White" if board.turn == chess.WHITE else "Black"

            print(f"\nMove {move_count + 1}, {player} to move")

            start_time = time.time()
            try:
                move = current_agent.choose_move(board)
                end_time = time.time()
                print(f"Move chosen: {move} in {end_time - start_time:.2f} seconds")
            except Exception as e:
                print(f"Error selecting move: {e}")
                print("Using random legal move instead")
                legal_moves = list(board.legal_moves)
                if legal_moves:
                    move = legal_moves[0]
                else:
                    print("No legal moves available")
                    game_over = True
                    break

            board, _, game_over, _ = env.step(move)
            last_move = move
            move_count += 1

            if record_video:
                try:
                    visualizer.capture_frame(board, last_move)
                except Exception as e:
                    print(f"Error capturing frame: {e}")

            try:
                if not visualizer.show(board, last_move):
                    break  
                time.sleep(0.5)  
            except Exception as e:
                print(f"Error displaying board: {e}")
                break

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

        if record_video:
            try:
                video_name = f"{algorithm_name.lower()}_depth{depth}_game.mp4"
                visualizer.save_video(video_name)
            except Exception as e:
                print(f"Error saving video: {e}")

    except KeyboardInterrupt:
        print("\nGame stopped by user.")

        if record_video:
            try:
                video_name = f"{algorithm_name.lower()}_depth{depth}_game_interrupted.mp4"
                visualizer.save_video(video_name)
            except Exception as e:
                print(f"Error saving video: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:

        pygame.quit()
        print("\nThank you for using Chess AI!")

if __name__ == "__main__":
    main()