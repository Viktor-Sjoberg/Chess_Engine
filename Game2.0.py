import pygame
import os
import ChessEngine as ce
import chess as ch

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = HEIGHT // 8  # Assuming a square chess board
WHITE = (234, 237, 204)
BLACK = (118, 153, 85)
 
# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")



image_directory = "img"  # Replace with your directory path
piece_images = {}
for piece in ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']:
    # Invert colors here: black pieces ('b') use white images, and vice versa
    inverted_color = 'w' if piece.startswith('w') else 'b'
    image_path = os.path.join(image_directory, f"{inverted_color}{piece[1]}.png")
    try:
        image = pygame.image.load(image_path)
        piece_images[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
# Initialize the chess board and engine
chess_board = ch.Board()
engine = ce.Engine(chess_board, maxDepth=5, color=ch.WHITE)

def draw_board(screen, board):
    # Draw squares on the board and pieces
    for row in range(8):
        for col in range(8):
            square_color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(ch.square(col, row))
            if piece:
                # Invert the color logic here as well
                piece_key = 'b' + str(piece).upper() if piece.color == ch.BLACK else 'w' + str(piece)
                screen.blit(piece_images[piece_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_player_move(screen, board):
    selected_square = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                if selected_square is None:
                    selected_square = ch.square(col, row)
                else:
                    move = ch.Move(selected_square, ch.square(col, row))
                    if move in board.legal_moves:
                        return move
                    selected_square = None
def get_square_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
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
                # Select the square if it has a piece of the player's color
                piece = chess_board.piece_at(square)
                if piece and piece.color == chess_board.turn:
                    selected_square = square
            else:
                # Make the move if it's legal
                move = ch.Move(selected_square, square)
                if move in chess_board.legal_moves:
                    chess_board.push(move)
                    player_turn = False  # Switch turns
                selected_square = None

    # Redraw the board and pieces after every event
    draw_board(screen, chess_board)
    pygame.display.flip()  # Update the full display Surface to the screen

    # Engine's turn (if it's not the player's turn and the game isn't over)
    if not player_turn and not chess_board.is_game_over():
        engine_move = engine.getBestMove()
        chess_board.push(engine_move)
        player_turn = True

        # Redraw the board and pieces after the engine's move
        draw_board(screen, chess_board)

        # Blit the flipped surface onto the screen

        
        pygame.display.flip()  # Update the full display Surface to the screen

# Clean up
pygame.quit()