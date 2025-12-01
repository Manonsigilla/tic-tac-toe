import pygame

# Initialize pygame
pygame.init()

# Constants for the game
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3  # Each cell is 200x200
LINE_COLOR = (0, 0, 0)  # Black
BG_COLOR = (255, 255, 255)  # White
LINE_WIDTH = 5
FPS = 60

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Initialize window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame. display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# Font for text
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)

# Game state variables
board = [""] * 9
current_player = "X"
game_over = False
winner = None

def draw_grid():
    """
    Draw the 3x3 grid on the screen
    """
    screen.fill(BG_COLOR)
    
    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, 
                        (i * CELL_SIZE, 0), 
                        (i * CELL_SIZE, WINDOW_SIZE), 
                        LINE_WIDTH)
    
    # Draw horizontal lines
    for i in range(1, 3):
        pygame.draw. line(screen, LINE_COLOR, 
                        (0, i * CELL_SIZE), 
                        (WINDOW_SIZE, i * CELL_SIZE), 
                        LINE_WIDTH)

def get_cell_from_mouse(pos):
    """
    Convert mouse position to cell index (0-8)
    
    Parameters:
    - pos: tuple (x, y) mouse position
    
    Returns:
    - int: cell index from 0 to 8
    
    Grid layout:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """
    x, y = pos
    col = x // CELL_SIZE  # 0, 1, or 2
    row = y // CELL_SIZE  # 0, 1, or 2
    cell_index = row * 3 + col
    return cell_index

def draw_symbols():
    """
    Draw X and O symbols on the board based on current board state
    """
    for i in range(9):
        if board[i] != "":
            # Calculate position
            row = i // 3
            col = i % 3
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            
            if board[i] == "O":
                # Draw circle (O)
                pygame.draw.circle(screen, RED, 
                (center_x, center_y), 
                CELL_SIZE // 3, 
                LINE_WIDTH)
            
            elif board[i] == "X":
                # Draw cross (X) - two diagonal lines
                offset = CELL_SIZE // 3
                # Line from top-left to bottom-right
                pygame.draw.line(screen, BLUE,
                (center_x - offset, center_y - offset),
                (center_x + offset, center_y + offset),
                LINE_WIDTH)
                # Line from top-right to bottom-left
                pygame.draw.line(screen, BLUE,
                (center_x + offset, center_y - offset),
                (center_x - offset, center_y + offset),
                LINE_WIDTH)

def check_winner(board):
    """
    Check if there is a winner on the board
    
    Parameters:
    - board: list of 9 elements containing "", "X", or "O"
    
    Returns:
    - "X" if X wins
    - "O" if O wins
    - "Draw" if board is full and no winner
    - None if game is still ongoing
    """
    # All possible winning combinations
    winning_combinations = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Diagonal top-left to bottom-right
        [2, 4, 6]   # Diagonal top-right to bottom-left
    ]
    
    # Check each winning combination
    for combo in winning_combinations:
        if (board[combo[0]] == board[combo[1]] == board[combo[2]] 
            and board[combo[0]] != ""):
            return board[combo[0]]  # Return "X" or "O"
    
    # Check for draw (board full)
    if "" not in board:
        return "Draw"
    
    # Game still ongoing
    return None

def draw_winner_message():
    """
    Display winner message and restart button
    """
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.set_alpha(200)  # Transparency
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))
    
    # Winner text
    if winner == "Draw":
        text = font_large.render("Draw!", True, BLACK)
    else:
        text = font_large.render(f"{winner} Wins!", True, GREEN)
    
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 50))
    screen.blit(text, text_rect)
    
    # Restart button
    button_rect = pygame.Rect(150, 350, 300, 80)
    pygame.draw.rect(screen, GREEN, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)  # Border
    
    button_text = font_small.render("Restart", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    return button_rect

def reset_game():
    """
    Reset the game to initial state
    """
    global board, current_player, game_over, winner
    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    print("Game reset!")

# Main game loop
running = True
restart_button_rect = None

while running:
    # Event handling
    for event in pygame. event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check if restart button is clicked
            if game_over and restart_button_rect:
                if restart_button_rect.collidepoint(mouse_pos):
                    reset_game()
            
            # Regular game play
            elif not game_over:
                # Get cell index from mouse click
                cell_index = get_cell_from_mouse(mouse_pos)
                
                # Check if cell is empty
                if board[cell_index] == "":
                    board[cell_index] = current_player
                    print(f"Player {current_player} played at position {cell_index}")
                    print(f"Board: {board}")
                    
                    # Check for winner
                    result = check_winner(board)
                    if result:
                        game_over = True
                        winner = result
                        print(f"Game Over! Winner: {winner}")
                    else:
                        # Switch player
                        current_player = "O" if current_player == "X" else "X"
    
    # Drawing
    draw_grid()
    draw_symbols()
    
    # Draw winner message if game is over
    if game_over:
        restart_button_rect = draw_winner_message()
    
    # Update display
    pygame.display. flip()
    clock.tick(FPS)

# Quit properly
pygame.quit()