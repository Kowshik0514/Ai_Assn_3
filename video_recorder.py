import chess
import chess.svg
import os
from PIL import Image, ImageDraw, ImageFont

class ChessVideoRecorder:
    def __init__(self, output_dir="videos"):
        self.output_dir = output_dir
        self.frame_count = 0
        os.makedirs(output_dir, exist_ok=True)
        
    def add_frame(self, board: chess.Board, move: chess.Move = None):
        """Add a frame to the video"""
        # Create a blank image
        img = Image.new('RGB', (400, 450), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw the board grid
        square_size = 40
        for row in range(8):
            for col in range(8):
                x1 = col * square_size + 40  # Add margin
                y1 = row * square_size + 40  # Add margin
                x2 = x1 + square_size
                y2 = y1 + square_size
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                draw.rectangle([x1, y1, x2, y2], fill=color, outline='black')
                
        # Draw coordinates
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            
        # Draw file coordinates (a-h)
        for i in range(8):
            x = i * square_size + 40 + square_size//2
            draw.text((x, 10), chr(97 + i), fill='black', font=font)  # Top
            draw.text((x, 370), chr(97 + i), fill='black', font=font)  # Bottom
            
        # Draw rank coordinates (1-8)
        for i in range(8):
            y = i * square_size + 40 + square_size//2
            draw.text((10, y), str(8 - i), fill='black', font=font)  # Left
            draw.text((370, y), str(8 - i), fill='black', font=font)  # Right
            
        # Draw pieces
        piece_symbols = {
            chess.PAWN: 'P', chess.KNIGHT: 'N', chess.BISHOP: 'B',
            chess.ROOK: 'R', chess.QUEEN: 'Q', chess.KING: 'K'
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                file_idx = chess.square_file(square)
                rank_idx = 7 - chess.square_rank(square)  # Flip rank for display
                x = file_idx * square_size + 40 + 5  # Add margin and offset
                y = rank_idx * square_size + 40 + 5  # Add margin and offset
                symbol = piece_symbols[piece.piece_type]
                if piece.color == chess.BLACK:
                    symbol = symbol.lower()
                draw.text((x, y), symbol, fill='black', font=font)
                
        # Draw last move
        if move:
            from_file = chess.square_file(move.from_square)
            from_rank = 7 - chess.square_rank(move.from_square)
            to_file = chess.square_file(move.to_square)
            to_rank = 7 - chess.square_rank(move.to_square)
            
            # Highlight source square
            x1 = from_file * square_size + 40
            y1 = from_rank * square_size + 40
            draw.rectangle([x1, y1, x1 + square_size, y1 + square_size],
                         outline='blue', width=2)
            
            # Highlight destination square
            x2 = to_file * square_size + 40
            y2 = to_rank * square_size + 40
            draw.rectangle([x2, y2, x2 + square_size, y2 + square_size],
                         outline='red', width=2)
                
        # Add move text at the bottom
        if move:
            draw.text((10, 420), f"Move: {move.uci()}", fill='black', font=font)
            
        # Save frame
        frame_path = os.path.join(self.output_dir, f"frame_{self.frame_count:04d}.png")
        img.save(frame_path)
        self.frame_count += 1
        
    def save_video(self, filename: str, fps: int = 1):
        """Save the recorded frames as a video"""
        print(f"Saved {self.frame_count} frames to {self.output_dir}")
        self.frame_count = 0
        
    def reset(self):
        """Reset the recorder"""
        self.frame_count = 0 