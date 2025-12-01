import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants and configurations
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
DARK_GREEN = (0, 150, 0)
WHITE = (255, 255, 255)

# Initialize window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame. display.set_caption("Tic Tac Toe - Belgium vs France")
clock = pygame.time.Clock()

# Font for text
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 50)

# Load images
try:
    # Load beer image (for X / Human player)
    beer_img = pygame.image.load(os.path.join("assets", "images", "beer.png"))
    beer_img = pygame.transform.scale(beer_img, (120, 120))  # Resize to fit cell
    
    # Load wine image (for O / AI player)
    wine_img = pygame.image.load(os.path.join("assets", "images", "wine.png"))
    wine_img = pygame.transform.scale(wine_img, (120, 120))  # Resize to fit cell
    
    print("✅ Images loaded successfully!")
    use_images = True
    
except Exception as e:
    print(f"⚠️ Error loading images: {e}")
    print("Falling back to default X and O symbols")
    use_images = False

# Game state variables
board = [""] * 9
current_player = "X"
game_over = False
winner = None
game_mode = None  # Will be "1P" or "2P"
game_state = "menu"  # Can be "menu" or "playing"
ai_player = "O"  # AI always plays as O

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
        pygame.draw.line(screen, LINE_COLOR, 
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
    Draw X and O symbols (or images) on the board based on current board state
    """
    for i in range(9):
        if board[i] != "":
            # Calculate position
            row = i // 3
            col = i % 3
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            
            if use_images:
                # Draw images
                if board[i] == "X":
                    # Beer image for X
                    img_rect = beer_img.get_rect(center=(center_x, center_y))
                    screen.blit(beer_img, img_rect)
                
                elif board[i] == "O":
                    # Wine image for O
                    img_rect = wine_img.get_rect(center=(center_x, center_y))
                    screen.blit(wine_img, img_rect)
            
            else:
                # Fallback to default shapes if images not loaded
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

def ordinateur(board, signe):
    """
    AI function that determines where the computer should play
    
    Parameters:
    - board: list of 9 elements containing "", "X", or "O"
    "" = nobody played here
    "X" = cross at this position
    "O" = circle at this position
    - signe: str, the symbol played by AI ("X" or "O")
    
    Returns:
    - int: position where AI wants to play (0-8)
    - False: in case of error
    
    Strategy:
    1. Try to win if possible
    2. Block opponent from winning
    3. Take center if available
    4. Take a corner if available
    5. Take any remaining spot
    """
    # Input validation
    if not isinstance(board, list) or len(board) != 9:
        print("Error: board must be a list of 9 elements")
        return False
    
    if signe not in ["X", "O"]:
        print("Error: signe must be 'X' or 'O'")
        return False
    
    # Determine opponent's sign
    opponent = "O" if signe == "X" else "X"
    
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
    
    # Strategy 1: Try to WIN
    for combo in winning_combinations:
        positions = [board[combo[0]], board[combo[1]], board[combo[2]]]
        # If AI has 2 in a row and third is empty, TAKE IT! 
        if positions.count(signe) == 2 and positions.count("") == 1:
            for i in combo:
                if board[i] == "":
                    print(f"AI: Winning move at position {i}")
                    return i
    
    # Strategy 2: BLOCK opponent from winning
    for combo in winning_combinations:
        positions = [board[combo[0]], board[combo[1]], board[combo[2]]]
        # If opponent has 2 in a row and third is empty, BLOCK IT!
        if positions.count(opponent) == 2 and positions.count("") == 1:
            for i in combo:
                if board[i] == "":
                    print(f"AI: Blocking opponent at position {i}")
                    return i
    
    # Strategy 3: Take CENTER (position 4) if available
    if board[4] == "":
        print("AI: Taking center (position 4)")
        return 4
    
    # Strategy 4: Take a CORNER if available
    corners = [0, 2, 6, 8]
    available_corners = [pos for pos in corners if board[pos] == ""]
    if available_corners:
        chosen = random.choice(available_corners)
        print(f"AI: Taking corner at position {chosen}")
        return chosen
    
    # Strategy 5: Take any REMAINING spot
    available_positions = [i for i in range(9) if board[i] == ""]
    if available_positions:
        chosen = random.choice(available_positions)
        print(f"AI: Taking remaining position {chosen}")
        return chosen
    
    # No available positions (should not happen in normal game)
    print("Error: No available positions on board")
    return False

def draw_winner_message():
    """
    Display winner message and restart button
    
    Returns:
    - restart_button_rect: pygame.Rect for the restart button
    - menu_button_rect: pygame. Rect for the menu button
    """
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.set_alpha(200)  # Transparency
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))
    
    # Winner text
    if winner == "Draw":
        text = font_small.render("You have the same brain", True, BLACK)
    else:
        # Display different message for AI vs Human
        if game_mode == "1P":
            if winner == "X":
                text = font_large.render("Belgium Wins!  🍺", True, DARK_GREEN)
            else:
                text = font_large. render("France Wins! 🍷", True, RED)
        else:
            if winner == "X":
                text = font_large.render("Belgium Wins! 🍺", True, DARK_GREEN)
            else:
                text = font_large.render("France Wins! 🍷", True, RED)
    
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
    screen.blit(text, text_rect)
    
    # Restart button
    restart_button_rect = pygame. Rect(150, 300, 300, 70)
    pygame.draw.rect(screen, GREEN, restart_button_rect)
    pygame.draw.rect(screen, BLACK, restart_button_rect, 3)  # Border
    
    restart_text = font_small.render("Restart", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)
    
    # Menu button
    menu_button_rect = pygame. Rect(150, 390, 300, 70)
    pygame.draw.rect(screen, GRAY, menu_button_rect)
    pygame.draw.rect(screen, BLACK, menu_button_rect, 3)  # Border
    
    menu_text = font_small.render("Menu", True, BLACK)
    menu_text_rect = menu_text. get_rect(center=menu_button_rect.center)
    screen.blit(menu_text, menu_text_rect)
    
    return restart_button_rect, menu_button_rect

def draw_menu():
    """
    Draw the main menu with 1 Player and 2 Players buttons
    
    Returns:
    - one_player_button: pygame.Rect for 1 player button
    - two_players_button: pygame.Rect for 2 players button
    """
    screen.fill(BG_COLOR)
    
    # Title
    title = font_large.render("TIC TAC TOE", True, BLACK)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, 100))
    screen.blit(title, title_rect)
    
    # 1 Player button
    one_player_button = pygame.Rect(150, 220, 300, 80)
    pygame.draw.rect(screen, GREEN, one_player_button)
    pygame.draw.rect(screen, BLACK, one_player_button, 3)
    
    one_player_text = font_medium.render("1 Player", True, BLACK)
    one_player_text_rect = one_player_text.get_rect(center=one_player_button.center)
    screen.blit(one_player_text, one_player_text_rect)
    
    # 2 Players button
    two_players_button = pygame.Rect(150, 340, 300, 80)
    pygame.draw.rect(screen, BLUE, two_players_button)
    pygame.draw.rect(screen, BLACK, two_players_button, 3)
    
    two_players_text = font_medium.render("2 Players", True, WHITE)
    two_players_text_rect = two_players_text.get_rect(center=two_players_button.center)
    screen.blit(two_players_text, two_players_text_rect)
    
    # Subtitle
    subtitle = font_small.render("Choose your mode", True, GRAY)
    subtitle_rect = subtitle.get_rect(center=(WINDOW_SIZE // 2, 480))
    screen.blit(subtitle, subtitle_rect)
    
    return one_player_button, two_players_button

def reset_game():
    """
    Reset the game to initial state (keep same mode)
    """
    global board, current_player, game_over, winner
    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    print("Game reset!")

def return_to_menu():
    """
    Return to main menu and reset everything
    """
    global board, current_player, game_over, winner, game_mode, game_state
    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    game_mode = None
    game_state = "menu"
    print("Returned to menu")

# Main game loop
running = True
restart_button_rect = None
menu_button_rect = None
one_player_button = None
two_players_button = None
ai_thinking = False  # To prevent multiple AI moves

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Menu state
            if game_state == "menu":
                if one_player_button and one_player_button.collidepoint(mouse_pos):
                    game_mode = "1P"
                    game_state = "playing"
                    print("1 Player mode selected")
                
                elif two_players_button and two_players_button.collidepoint(mouse_pos):
                    game_mode = "2P"
                    game_state = "playing"
                    print("2 Players mode selected")
            
            # Playing state
            elif game_state == "playing":
                # Check if game over buttons are clicked
                if game_over:
                    if restart_button_rect and restart_button_rect.collidepoint(mouse_pos):
                        reset_game()
                    
                    elif menu_button_rect and menu_button_rect.collidepoint(mouse_pos):
                        return_to_menu()
                
                # Regular game play (only if it's human's turn)
                elif not ai_thinking:
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
    
    # AI logic (runs every frame, but only acts when it's AI's turn)
    if (game_state == "playing" and 
        not game_over and 
        game_mode == "1P" and 
        current_player == ai_player and 
        not ai_thinking):
        
        ai_thinking = True  # Prevent multiple calls
        
        # Small delay to make AI feel more natural (optional)
        pygame.time.wait(700)  # 700ms delay
        
        # Call the AI function
        ai_move = ordinateur(board, ai_player)
        
        if ai_move is not False and 0 <= ai_move <= 8 and board[ai_move] == "":
            board[ai_move] = ai_player
            print(f"AI played at position {ai_move}")
            print(f"Board: {board}")
            
            # Check for winner
            result = check_winner(board)
            if result:
                game_over = True
                winner = result
                print(f"Game Over! Winner: {winner}")
            else:
                # Switch back to human player
                current_player = "X"
        else:
            print(f"Error: AI returned invalid move {ai_move}")
        
        ai_thinking = False
    
    # Drawing based on game state
    if game_state == "menu":
        one_player_button, two_players_button = draw_menu()
    
    elif game_state == "playing":
        draw_grid()
        draw_symbols()
        
        # Draw winner message if game is over
        if game_over:
            restart_button_rect, menu_button_rect = draw_winner_message()
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit properly
pygame.quit()