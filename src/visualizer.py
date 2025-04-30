import pygame
import chess
import time
import os
import cv2
import numpy as np
from datetime import datetime

class ChessVisualizer:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.square_size = width // 8
        pygame.init()
        self.screen = pygame.Surface((width, height))
        self.display = None
        self.piece_images = {}
        self.load_piece_images()
        self.white_square = pygame.Color(240, 217, 181)
        self.black_square = pygame.Color(181, 136, 99)
        self.highlight_color = pygame.Color(124, 192, 214, 170)
        self.frames = []
        self.frame_rate = 2
        self.frame_delay = 0.5
            
    def load_piece_images(self):
        pieces = ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']
        for piece in pieces:
            filename = f"assets/pieces/{'w' if piece.isupper() else 'b'}{piece.upper()}.svg"
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (int(self.square_size * 0.75), int(self.square_size * 0.75)))
            self.piece_images[piece] = image

    def draw_piece(self, piece, row, col):
        piece_image = self.piece_images.get(piece)
        if piece_image:
            x = col * self.square_size + (self.square_size - piece_image.get_width()) // 2
            y = row * self.square_size + (self.square_size - piece_image.get_height()) // 2
            self.screen.blit(piece_image, (x, y))
            
    def draw_board(self, board, last_move=None):
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, 
                                   self.square_size, self.square_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.screen, self.white_square, rect)
                else:
                    pygame.draw.rect(self.screen, self.black_square, rect)
                if last_move:
                    try:
                        from_square = last_move.from_square
                        to_square = last_move.to_square
                        if (row * 8 + col) == from_square or (row * 8 + col) == to_square:
                            highlight_rect = pygame.Rect(col * self.square_size, row * self.square_size, 
                                                      self.square_size, self.square_size)
                            highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                            highlight.fill(self.highlight_color)
                            self.screen.blit(highlight, highlight_rect)
                    except:
                        pass
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row, col = divmod(square, 8)
                piece_symbol = piece.symbol()
                if piece_symbol in self.piece_images:
                    self.draw_piece(piece_symbol, row, col)
        try:
            font = pygame.font.SysFont('Arial', 14)
        except:
            font = pygame.font.Font(None, 14)
        for i in range(8):
            rank_text = font.render(str(8 - i), True, pygame.Color(0, 0, 0) if i % 2 == 0 else pygame.Color(255, 255, 255))
            self.screen.blit(rank_text, (5, i * self.square_size + 5))
            file_text = font.render(chr(97 + i), True, pygame.Color(0, 0, 0) if (i + 7) % 2 == 0 else pygame.Color(255, 255, 255))
            self.screen.blit(file_text, (i * self.square_size + self.square_size - 15, self.height - 15))
    
    def show(self, board, last_move=None):
        if self.display is None:
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Chess AI")
        self.draw_board(board, last_move)
        self.display.blit(self.screen, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        return True
    
    def capture_frame(self, board, last_move=None):
        self.draw_board(board, last_move)
        frame = pygame.surfarray.array3d(self.screen)
        frame = np.transpose(frame, (1, 0, 2))
        self.frames.append(frame)
        
    def save_video(self, filename=None):
        if not self.frames:
            print("No frames to save")
            return
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chess_game_{timestamp}.mp4"
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        try:
            height, width, _ = self.frames[0].shape
            try:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, self.frame_rate, (width, height))
                if not out.isOpened():
                    raise Exception("Failed to create video writer with mp4v codec")
            except:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    output_path = output_path.replace('.mp4', '.avi')
                    out = cv2.VideoWriter(output_path, fourcc, self.frame_rate, (width, height))
                except:
                    fourcc = 0
                    output_path = output_path.replace('.mp4', '.avi')
                    out = cv2.VideoWriter(output_path, fourcc, self.frame_rate, (width, height))
            for frame in self.frames:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            out.release()
            print(f"Video saved to {output_path}")
        except Exception as e:
            print(f"Error creating video: {e}")
            print("Saving individual frames as PNG files instead")
            frames_dir = os.path.join(output_dir, "frames_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
            os.makedirs(frames_dir, exist_ok=True)
            for i, frame in enumerate(self.frames):
                frame_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(frame_path, frame_bgr)
            print(f"Frames saved to {frames_dir}")
        self.frames = []
