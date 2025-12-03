import pygame
import random
import os

# Initialize pygame
pygame.init()

#Initialize the mixer for sound
pygame.mixer.init()

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
    
# Settings state
settings_open = False
music_volume = 0.5
sfx_volume = 0.7
music_enabled = True
sfx_enabled = True
    
# Load sounds
try:
    # load background music
    pygame.mixer.music.load(os.path.join("assets", "sounds", "music.wav"))
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1, 0, 0)  # Loop indefinitely
    pygame.mixer.music.set_pos(10.0)  # Start from 10 seconds into the track
    
    # load sound effects
    beer_click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "beer_click.wav"))
    wine_click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "wine_click.wav"))
    click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav"))
    
    # Set volume for sound effects
    beer_click_sound.set_volume(0.7)
    wine_click_sound.set_volume(0.7)
    click_sound.set_volume(0.7)
    
    print("✅ Sounds loaded successfully!")
    use_sounds = True

except Exception as e:
    print(f"⚠️ Error loading sounds: {e}")
    print("Continuing without background music")
    use_sounds = False
    # If sounds fail to load, we can define dummy sound play functions
    class DummySound:
        def play(self):
            pass
    beer_click_sound = DummySound()
    wine_click_sound = DummySound()
    click_sound = DummySound()

# Game state variables
board = [""] * 9
current_player = "X"
game_over = False
winner = None
game_mode = None  # Will be "1P" or "2P"
game_state = "menu"  # Can be "menu" or "playing"
ai_player = "O"  # AI always plays as O
ai_move_time = 0  # To manage AI move timing
ai_delay = 1200  # milliseconds delay before AI plays

def play_sound(sound):
    """
    Play a sound if sounds are enabled
    
    Parameters:
    - sound: pygame.mixer.Sound object to play
    """
    if use_sounds and sound and sfx_enabled:
        sound.play()

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
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
        screen.blit(text, text_rect)
    else:
        # Display different message with icons
        if winner == "X":
            # Belgium wins - show text + beer image
            text = font_large.render("Belgium Wins!", True, DARK_GREEN)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
            screen.blit(text, text_rect)
            
            # Show beer image next to text
            if use_images:
                beer_display = pygame.transform.scale(beer_img, (60, 60))
                beer_rect = beer_display.get_rect(midleft=(text_rect.right + 15, WINDOW_SIZE // 2 - 80))
                screen.blit(beer_display, beer_rect)
        else:
            # France wins - show text + wine image
            text = font_large.render("France Wins!", True, RED)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
            screen.blit(text, text_rect)
            
            # Show wine image next to text
            if use_images:
                wine_display = pygame.transform.scale(wine_img, (60, 60))
                wine_rect = wine_display.get_rect(midleft=(text_rect.right + 15, WINDOW_SIZE // 2 - 80))
                screen.blit(wine_display, wine_rect)
    
    # Restart button
    restart_button_rect = pygame.Rect(150, 300, 300, 70)
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
    
def draw_settings_button():
    """
    Draw the settings gear button in top-right corner
    
    Returns:
    - settings_button_rect: pygame.Rect for the settings button
    """
    settings_button_rect = pygame.Rect(WINDOW_SIZE - 60, 10, 50, 50)
    
    # Draw gear icon background
    pygame.draw.circle(screen, GRAY, settings_button_rect.center, 25)
    pygame.draw.circle(screen, BLACK, settings_button_rect.center, 25, 2)
    
    # Draw gear symbol manually (3 lines forming a settings icon)
    center = settings_button_rect.center
    
    # Draw three horizontal lines (hamburger menu style for settings)
    line_length = 20
    line_spacing = 7
    
    for i in range(3):
        y_offset = (i - 1) * line_spacing
        pygame.draw.line(screen, BLACK, 
                        (center[0] - line_length//2, center[1] + y_offset),
                        (center[0] + line_length//2, center[1] + y_offset), 
                        3)
    
    return settings_button_rect

def draw_settings_menu():
    """
    Draw the settings overlay with volume controls
    
    Returns:
    - Dictionary with all interactive elements' rects
    """
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.set_alpha(230)
    overlay.fill((50, 50, 50))
    screen.blit(overlay, (0, 0))
    
    # Settings panel
    panel_rect = pygame.Rect(100, 80, 400, 440)
    pygame.draw.rect(screen, WHITE, panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 3)
    
    # Title
    title = font_medium.render("Settings", True, BLACK)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, 120))
    screen.blit(title, title_rect)
    
    # Music label
    music_label = font_small.render("Music Volume", True, BLACK)
    screen.blit(music_label, (130, 180))
    
    # Music volume slider
    slider_y = 220
    slider_rect = pygame. Rect(130, slider_y, 340, 10)
    
    # Draw slider track (background)
    pygame.draw.rect(screen, (180, 180, 180), slider_rect)
    pygame.draw.rect(screen, BLACK, slider_rect, 1)  # Border
    
    # Draw filled portion of slider
    filled_width = int(music_volume * 340)
    if filled_width > 0:
        filled_rect = pygame.Rect(130, slider_y, filled_width, 10)
        pygame.draw.rect(screen, GREEN if music_enabled else RED, filled_rect)
    
    # Music slider handle
    handle_x = 130 + int(music_volume * 340)
    music_handle_rect = pygame.Rect(handle_x - 12, slider_y - 12, 24, 34)
    pygame.draw.rect(screen, GREEN if music_enabled else RED, music_handle_rect)
    pygame.draw.rect(screen, BLACK, music_handle_rect, 2) # Border
    
    # Music volume percentage
    volume_text = font_small.render(f"{int(music_volume * 100)}%", True, BLACK)
    screen.blit(volume_text, (500 - volume_text.get_width(), 180))
    
    # Music toggle button
    music_toggle_rect = pygame.Rect(130, 250, 150, 40)
    pygame.draw.rect(screen, GREEN if music_enabled else RED, music_toggle_rect)
    pygame.draw.rect(screen, BLACK, music_toggle_rect, 2)
    toggle_text = font_small.render("ON" if music_enabled else "OFF", True, BLACK)
    toggle_text_rect = toggle_text.get_rect(center=music_toggle_rect.center)
    screen.blit(toggle_text, toggle_text_rect)
    
    # SFX label
    sfx_label = font_small.render("SFX Volume", True, BLACK)
    screen.blit(sfx_label, (130, 310))
    
    # SFX volume slider
    sfx_slider_y = 350
    sfx_slider_rect = pygame.Rect(130, sfx_slider_y, 340, 10)
    
    # Draw slider track (background)
    pygame.draw.rect(screen, (180, 180, 180), sfx_slider_rect)
    pygame.draw.rect(screen, BLACK, sfx_slider_rect, 1)  # Border
    
    # Draw filled portion of slider
    sfx_filled_width = int(sfx_volume * 340)
    if sfx_filled_width > 0:
        sfx_filled_rect = pygame.Rect(130, sfx_slider_y, sfx_filled_width, 10)
        pygame.draw.rect(screen, GREEN if sfx_enabled else RED, sfx_filled_rect)
    
    # SFX slider handle
    sfx_handle_x = 130 + int(sfx_volume * 340)
    sfx_handle_rect = pygame. Rect(sfx_handle_x - 12, sfx_slider_y - 12, 24, 34)
    pygame.draw.rect(screen, GREEN if sfx_enabled else RED, sfx_handle_rect)
    pygame.draw.rect(screen, BLACK, sfx_handle_rect, 2) # Border
    
    # SFX volume percentage
    sfx_volume_text = font_small.render(f"{int(sfx_volume * 100)}%", True, BLACK)
    screen.blit(sfx_volume_text, (500 - sfx_volume_text.get_width(), 310))
    
    # SFX toggle button
    sfx_toggle_rect = pygame.Rect(130, 380, 150, 40)
    pygame.draw.rect(screen, GREEN if sfx_enabled else RED, sfx_toggle_rect)
    pygame.draw.rect(screen, BLACK, sfx_toggle_rect, 2)
    sfx_toggle_text = font_small.render("ON" if sfx_enabled else "OFF", True, BLACK)
    sfx_toggle_text_rect = sfx_toggle_text.get_rect(center=sfx_toggle_rect.center)
    screen. blit(sfx_toggle_text, sfx_toggle_text_rect)
    
    # Close button
    close_button_rect = pygame.Rect(200, 450, 200, 50)
    pygame.draw.rect(screen, BLUE, close_button_rect)
    pygame.draw.rect(screen, BLACK, close_button_rect, 2)
    close_text = font_small.render("Close", True, WHITE)
    close_text_rect = close_text.get_rect(center=close_button_rect.center)
    screen.blit(close_text, close_text_rect)
    
    return {
        'music_slider': slider_rect,
        'music_handle': music_handle_rect,
        'music_toggle': music_toggle_rect,
        'sfx_slider': sfx_slider_rect,
        'sfx_handle': sfx_handle_rect,
        'sfx_toggle': sfx_toggle_rect,
        'close': close_button_rect,
        'panel': panel_rect
    }

def update_volumes():
    """
    Update the actual volumes of music and sound effects
    """
    if use_sounds:
        # Update music volume
        if music_enabled:
            pygame. mixer.music.set_volume(music_volume)
        else:
            pygame.mixer.music. set_volume(0)
        
        # Update sound effects volume
        actual_sfx_volume = sfx_volume if sfx_enabled else 0
        if beer_click_sound:
            beer_click_sound.set_volume(actual_sfx_volume)
        if wine_click_sound:
            wine_click_sound.set_volume(actual_sfx_volume)
        if click_sound:
            click_sound.set_volume(actual_sfx_volume)

# Main game loop
running = True
restart_button_rect = None
menu_button_rect = None
one_player_button = None
two_players_button = None
ai_thinking = False  # To prevent multiple AI moves
settings_button_rect = None
settings_rects = {}
dragging_music_slider = False
dragging_sfx_slider = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check settings button click (available in all states)
            if not settings_open and settings_button_rect and settings_button_rect.collidepoint(mouse_pos):
                settings_open = True
                play_sound(click_sound) # Play click sound
                print("Settings opened")
                continue  # Skip other checks when opening settings
            
            # Settings menu interactions
            if settings_open:
                if settings_rects.get('close') and settings_rects['close'].collidepoint(mouse_pos):
                    settings_open = False
                    play_sound(click_sound) # Play click sound
                    print("Settings closed")
                
                elif settings_rects.get('music_toggle') and settings_rects['music_toggle'].collidepoint(mouse_pos):
                    music_enabled = not music_enabled
                    update_volumes()
                    play_sound(click_sound) # Play click sound
                    print(f"Music {'enabled' if music_enabled else 'disabled'}")
                    
                elif settings_rects.get('sfx_toggle') and settings_rects['sfx_toggle'].collidepoint(mouse_pos):
                    sfx_enabled = not sfx_enabled
                    update_volumes()
                    play_sound(click_sound) # Play click sound
                    print(f"SFX {'enabled' if sfx_enabled else 'disabled'}")
                    
                if settings_rects.get('music_slider'):
                    slider = settings_rects['music_slider']
                    # expand clickable area vertically for easier dragging
                    expanded_slider_rect = pygame.Rect(slider.x, slider.y - 15, slider.width, slider.height + 40)
                    if expanded_slider_rect.collidepoint(mouse_pos):
                        dragging_music_slider = True
                        # immediately update volume on click
                        relative_x = mouse_pos[0] - slider.x
                        music_volume = max(0.0, min(1.0, relative_x / slider.width))
                        update_volumes()
                
                if settings_rects.get('sfx_slider'):
                    slider = settings_rects['sfx_slider']
                    # expand clickable area vertically for easier dragging
                    expanded_slider_rect = pygame.Rect(slider.x, slider.y - 15, slider.width, slider.height + 40)
                    if expanded_slider_rect.collidepoint(mouse_pos):
                        dragging_sfx_slider = True
                        # immediately update volume on click
                        relative_x = mouse_pos[0] - slider.x
                        sfx_volume = max(0.0, min(1.0, relative_x / slider.width))
                        update_volumes()
                continue  # Skip other checks when in settings
            
            # Menu state
            if game_state == "menu":
                if one_player_button and one_player_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game_mode = "1P"
                    game_state = "playing"
                    print("1 Player mode selected")
                
                elif two_players_button and two_players_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game_mode = "2P"
                    game_state = "playing"
                    print("2 Players mode selected")
            
            # Playing state
            elif game_state == "playing":
                # Check if game over buttons are clicked
                if game_over:
                    if restart_button_rect and restart_button_rect.collidepoint(mouse_pos):
                        play_sound(click_sound) # Play click sound
                        reset_game()
                    
                    elif menu_button_rect and menu_button_rect.collidepoint(mouse_pos):
                        play_sound(click_sound) # Play click sound
                        return_to_menu()
                
                # Regular game play (only if it's human's turn)
                elif not ai_thinking:
                    # Get cell index from mouse click
                    cell_index = get_cell_from_mouse(mouse_pos)
                    
                    # Check if cell is empty
                    if board[cell_index] == "":
                        board[cell_index] = current_player
                        
                        # Play appropriate sound based on player
                        if current_player == "X":
                            play_sound(beer_click_sound) # Sound for beer (X)
                        else:
                            play_sound(wine_click_sound) # Sound for wine (O)
                            
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
    
        if event.type == pygame.MOUSEBUTTONUP:
            dragging_music_slider = False
            dragging_sfx_slider = False
            
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos # Current mouse position
            
            if dragging_music_slider and settings_rects.get('music_slider'):
                # Update music volume based on mouse position
                slider = settings_rects['music_slider']
                relative_x = mouse_pos[0] - slider.x
                music_volume = max(0.0, min(1.0, relative_x / slider.width))
                update_volumes()
                
            elif dragging_sfx_slider and settings_rects.get('sfx_slider'):
                # Update SFX volume based on mouse position
                slider = settings_rects['sfx_slider']
                relative_x = mouse_pos[0] - slider.x
                sfx_volume = max(0.0, min(1.0, relative_x / slider.width))
                update_volumes()
                
    # AI logic (runs every frame, but only acts when it's AI's turn)
    if (game_state == "playing" and 
        not game_over and 
        game_mode == "1P" and 
        current_player == ai_player):
        
        if not ai_thinking:
            # Start AI thinking process
            ai_thinking = True
            ai_move_time = pygame.time.get_ticks() + ai_delay # Record the time when AI starts thinking
            print("AI is thinking...")
        
        # Check if AI delay time has passed
        elif pygame.time.get_ticks() >= ai_move_time:
            ai_move = ordinateur(board, ai_player) # Call the AI function
            
            if ai_move is not False and 0 <= ai_move <= 8 and board[ai_move] == "":
                board[ai_move] = ai_player
                
                # Play sound for AI move
                play_sound(wine_click_sound)  # Sound for wine (O)
                
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
                
            ai_thinking = False  # Reset AI thinking flag
    
    # Drawing based on game state
    if game_state == "menu":
        one_player_button, two_players_button = draw_menu()
        settings_button_rect = draw_settings_button()
    
    elif game_state == "playing":
        draw_grid()
        draw_symbols()
        settings_button_rect = draw_settings_button()
        
        # Draw winner message if game is over
        if game_over:
            restart_button_rect, menu_button_rect = draw_winner_message()
    
    # Draw settings overlay on top of everything if open
    if settings_open:
        settings_rects = draw_settings_menu()
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit properly
pygame.quit()