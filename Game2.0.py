import pygame
import os
import MiniMax as ce
import chess as ch
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = HEIGHT // 8  # Assuming a square chess board
WHITE = (234, 237, 204)
BLACK = (118, 153, 85)
HIGHLIGHT_COLOR = (246, 248, 121)
 
# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# Load the images for the pieces 
image_directory = "img"  
piece_images = {}
for piece in ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']:
    inverted_color = 'w' if piece.startswith('w') else 'b'
    image_path = os.path.join(image_directory, f"{inverted_color}{piece[1]}.png")
    try:
        image = pygame.image.load(image_path)
        piece_images[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")

sound_directory = "Sounds"
win_sound = pygame.mixer.Sound(os.path.join(sound_directory, "win_sound.wav"))
lose_sound = pygame.mixer.Sound(os.path.join(sound_directory, "lose_sound.wav"))
check_sound = pygame.mixer.Sound(os.path.join(sound_directory, "check.wav"))
move_sounds = [pygame.mixer.Sound(os.path.join(sound_directory, "moves", f"{i}.wav")) for i in range(1, 11)]

# Initialize the chess board and engine
chess_board = ch.Board()
engine = ce.Engine(chess_board, maxDepth=4, color=ch.BLACK)

last_move = None  # Stores the last move for highlighting

def draw_board(screen, board, last_move):
    for row in range(8):
        for col in range(8):
            square = ch.square(col, 7 - row)
            if last_move and (square == last_move.from_square or square == last_move.to_square):
                square_color = HIGHLIGHT_COLOR
            else:
                square_color = WHITE if (row + col) % 2 == 0 else BLACK
            
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(square)
            if piece:
                piece_key = 'b' + str(piece).upper() if piece.color == ch.BLACK else 'w' + str(piece)
                screen.blit(piece_images[piece_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_from_mouse(pos):
    x, y = pos
    row = 7 - (y // SQUARE_SIZE)  # Adjust for flipped board
    col = x // SQUARE_SIZE
    return row, col

# Main loop
selected_square = None
player_turn = True  # White starts first
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_square_from_mouse(pos)
            square = ch.square(col, row)
            if selected_square is None:
                piece = chess_board.piece_at(square)
                if piece and piece.color == chess_board.turn:
                    selected_square = square
            else:
                move = ch.Move(selected_square, square)
                if move in chess_board.legal_moves:
                    chess_board.push(move)
                    last_move = move  # Store last move
                    player_turn = False
                    selected_square = None
    
    draw_board(screen, chess_board, last_move)
    pygame.display.flip()

    if not player_turn and not chess_board.is_game_over():
        engine_move = engine.getBestMove()
        chess_board.push(engine_move)
        last_move = engine_move  # Store last move
        player_turn = True

        if chess_board.is_check():
            check_sound.play()
        else:
            random.choice(move_sounds).play()

        draw_board(screen, chess_board, last_move)
        pygame.display.flip()

    if chess_board.is_game_over():
        if chess_board.result() == "1-0":
            win_sound.play()
        elif chess_board.result() == "0-1":
            lose_sound.play()
        
        pygame.time.delay(15000)
        running = False

pygame.quit()
