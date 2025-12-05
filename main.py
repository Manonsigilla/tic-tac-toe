import math
import pygame
import random
import os
import json
from datetime import datetime

# Initialize pygame
pygame.init()

#Initialize the mixer for sound
pygame.mixer.init()

# Constants and configurations
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3  # Each cell is 200x200
LINE_COLOR = (0, 0, 0)  # Black
BG_COLOR = (255, 255, 255)  # White
LINE_WIDTH = 3
FPS = 60

# Colors - Pastel Dream Palette
# Gradient background colors
GRADIENT_TOP = (255, 190, 152)      # Peach (Belgium side)
GRADIENT_BOTTOM = (168, 218, 220)   # Powder blue (France side)

# UI colors
PRIMARY_GREEN = (129, 236, 236)     # Turquoise (active buttons)
PRIMARY_BLUE = (116, 185, 255)      # Sky blue (2 players button)
ACCENT_RED = (250, 127, 111)        # Salmon (France wins)
ACCENT_GOLD = (253, 203, 110)       # Butter yellow (Belgium wins)
DARK_NAVY = (52, 73, 94)            # Midnight blue (main text)
LIGHT_GRAY = (236, 240, 241)        # Clouds (backgrounds)
WHITE = (252, 252, 252)             # Almost white
DARK_GRAY = (127, 140, 141)         # Asphalt (secondary text)

# Legacy color names (for compatibility)
BLACK = DARK_NAVY
BG_COLOR = WHITE
LINE_COLOR = DARK_NAVY
RED = ACCENT_RED
BLUE = PRIMARY_BLUE
GREEN = PRIMARY_GREEN
GRAY = LIGHT_GRAY
DARK_GREEN = ACCENT_GOLD

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
# board = [""] * 9
# current_player = "X"
# game_over = False
# winner = None
# game_mode = None  # Will be "1P" or "2P"
# game_state = "menu"  # Can be "menu" or "playing"
# ai_player = "O"  # AI always plays as O
# ai_move_time = 0  # To manage AI move timing
# ai_delay = 1200  # milliseconds delay before AI plays
# winner_recorded = False  # To ensure we record the winner only once
# ai_difficulty = "hard" # Currently only "hard" is implemented but can be "easy", "medium", "hard"

class GameState:
    def __init__(self):
        # Board state
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.winner_recorded = False  # To ensure we record the winner only once
        
        # Game mode
        self.game_mode = None  # Will be "1P" or "2P"
        self.game_state = "menu"  # Can be "menu" or "playing"
        
        # AI settings
        self.ai_player = "O"  # AI always plays as O
        self.ai_move_time = 0  # To manage AI move timing
        self.ai_delay = 1200  # milliseconds delay before AI plays
        self.ai_difficulty = "hard" # Currently only "hard" is implemented but can be "easy", "medium", "hard"
        self.ai_thinking = False  # Whether AI is currently "thinking"
        
        # UI state
        self.settings_open = False
        self.dragging_music_slider = False
        self.dragging_sfx_slider = False
        
        # Animation state
        self.fireworks = []  # List of active Firework objects
        self.button_hover = None  # Currently hovered button
        self.button_scales = {}  # Scale factors for buttons (for hover effect)
        
        # button rects (updated each frame)
        self.restart_button_rect = None
        self.menu_button_rect = None
        self.one_player_button = None
        self.two_players_button = None
        self.stats_button = None
        self.back_button_rect = None
        self.reset_stats_button_rect = None
        self.settings_button_rect = None
        self.settings_rects = {}
        self.easy_button = None
        self.medium_button = None
        self.hard_button = None
        self.difficulty_back_button_rect = None
        
    def reset_game(self):
        """
        Reset the game to initial state (keep same mode)
        """
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.winner_recorded = False
        print("Game reset!")
    
    def return_to_menu(self):
        """
        Return to main menu and reset everything
        """
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.winner_recorded = False
        self.game_mode = None
        self.game_state = "menu"
        print("Returned to menu")

class Particle:
    """
    Particle class for fireworks and animations
    """
    def __init__(self, x, y, color, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = random.randint(45, 90)  # Frames the particle will live
        self.age = 0 # Current age in frames
        self.size = random.randint(3, 8)  # Size of the particle
        
    def update(self):
        """
        Update particle position and age
        """
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.18 # Gravity effect
        self.velocity_x *= 0.995 # Air resistance
        self.age += 1
        
    def draw(self, screen):
        """
        Draw the particle on the screen
        """
        if self.age < self.lifetime:
            # Fade out as particle ages
            life_ratio = 1 - (self.age / self.lifetime)
            size = max(1, int(self.size * life_ratio))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
    
    def is_alive(self):
        """
        Check if the particle is still alive
        """
        return self.age < self.lifetime
    
class Firework:
    """
    Firework system that creates particles explosion
    """
    def __init__(self, x, y, color):
        self.particles = []
        self.create_explosion(x, y, color)
        
    def create_explosion(self, x, y, color):
        """
        Create explosion particles at (x, y) with given color
        """
        num_particles = random.randint(30, 60)
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)  # Random angle
            speed = random.uniform(2, 8)  # Random speed
            velocity_x = speed * math.cos(angle)
            velocity_y = speed * math.sin(angle)
            col = (
                min(255, max(0, color[0] + random.randint(-20, 20))),
                min(255, max(0, color[1] + random.randint(-20, 20))),
                min(255, max(0, color[2] + random.randint(-20, 20))),
            )
            self.particles.append(Particle(x, y, col, velocity_x, velocity_y))
            
    def update(self):
        """
        Update all particles
        """
        for particle in self.particles:
            particle.update()
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]
        
    def draw(self, surface):
        """
        Draw all particles
        """
        for particle in self.particles:
            particle.draw(surface)
            
    def is_finished(self):
        """
        Check if all particles are dead
        """
        return len(self.particles) == 0 
def play_sound(sound):
    """
    Play a sound if sounds are enabled
    
    Parameters:
    - sound: pygame.mixer.Sound object to play
    """
    if use_sounds and sound and sfx_enabled:
        sound.play()

def draw_gradient_background():
    """
    Draw a vertical gradient background from GRADIENT_TOP to GRADIENT_BOTTOM
    """
    for y in range(WINDOW_SIZE):
        # Calculate the ratio (0.0 to 1.0)
        ratio = y / WINDOW_SIZE
        
        # Interpolate between top and bottom colors
        r = int(GRADIENT_TOP[0] * (1 - ratio) + GRADIENT_BOTTOM[0] * ratio)
        g = int(GRADIENT_TOP[1] * (1 - ratio) + GRADIENT_BOTTOM[1] * ratio)
        b = int(GRADIENT_TOP[2] * (1 - ratio) + GRADIENT_BOTTOM[2] * ratio)
        
        # Draw a horizontal line for this y position
        pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_SIZE, y))

def draw_grid():
    """
    Draw the 3x3 grid on the screen with gradient background
    """
    draw_gradient_background()
    
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

def draw_symbols(game):
    """
    Draw X and O symbols (or images) on the board based on current board state
    
    Parameters:
    - game: GameState object containing the board state
    """
    for i in range(9):
        if game.board[i] != "":
            # Calculate position
            row = i // 3
            col = i % 3
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            
            if use_images:
                # Draw images
                if game.board[i] == "X":
                    # Beer image for X
                    img_rect = beer_img.get_rect(center=(center_x, center_y))
                    screen.blit(beer_img, img_rect)
                
                elif game.board[i] == "O":
                    # Wine image for O
                    img_rect = wine_img.get_rect(center=(center_x, center_y))
                    screen.blit(wine_img, img_rect)
            
            else:
                # Fallback to default shapes if images not loaded
                if game.board[i] == "O":
                    # Draw circle (O)
                    pygame.draw.circle(screen, RED, 
                    (center_x, center_y), 
                    CELL_SIZE // 3, 
                    LINE_WIDTH)
                
                elif game.board[i] == "X":
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

def trigger_fireworks(game):
    """
    Trigger fireworks animation based on the winner
    
    Parameters:
    - game: GameState object containing the winner
    """
    if game.winner == "X":
        # Belgium wins - gold/yellow fireworks
        colors = [ACCENT_GOLD, PRIMARY_GREEN]
    elif game.winner == "O":
        # France wins - red fireworks
        colors = [ACCENT_RED, PRIMARY_BLUE]
    else:
        colors = [DARK_NAVY, LIGHT_GRAY]
    
    # Create multiple fireworks at random positions
    for _ in range(5):  # Number of fireworks
        x = random.randint(100, WINDOW_SIZE - 100)
        y = random.randint(100, WINDOW_SIZE - 300)
        color = random.choice(colors)
        game.fireworks.append(Firework(x, y, color))
        
def update_and_draw_fireworks(game, screen):
    """
    Update and draw all active fireworks
    
    Parameters:
    - game: GameState object containing the fireworks list
    - screen: pygame display surface
    """
    for firework in game.fireworks:
        firework.update()
        firework.draw(screen)
    
    # Remove finished fireworks
    game.fireworks = [fw for fw in game.fireworks if not fw.is_finished()]
    
def draw_animated_button(game, rect, color, text, text_color, mouse_pos, button_id):
    """
    Draw a button with hover animation effect
    
    Parameters:
    - game: GameState object containing button scales
    - rect: pygame.Rect for button position and size
    - color: tuple RGB color for button background
    - text: str, text to display on button
    - text_color: tuple RGB color for text
    - mouse_pos: tuple (x, y) current mouse position
    - button_id: str, unique identifier for the button
    
    Returns:
    - pygame.Rect: updated rect of the button (for click detection)
    """
    # Check if mouse is hovering over button
    is_hovering = rect.collidepoint(mouse_pos) if mouse_pos else False
    
    # Initialize scale if not present
    if button_id not in game.button_scales:
        game.button_scales[button_id] = 1.0
        
    # Decide target scale first
    target_scale = 1.05 if is_hovering else 1.0
    
    # Smoothly interpolate scale
    current = game.button_scales[button_id]
    smoothing = 0.16  # Adjust for speed of scaling
    game.button_scales[button_id] = current + (target_scale - current) * smoothing
    scale = game.button_scales[button_id]
    
    # Compute scaled rect around the same center
    center = rect.center
    scaled_width = max(1, int(rect.width * scale))
    scaled_height = max(1, int(rect.height * scale))
    scaled_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
    scaled_rect.center = center
    
    # Adjust color if hovering (make slightly brighter)
    if is_hovering:
        hover_color = tuple(min(255, int(c * 1.1)) for c in color)
    else:
        hover_color = color
        
    # Draw button background and border
    pygame.draw.rect(screen, hover_color, scaled_rect, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, scaled_rect, 3, border_radius=12)  # Border
    
    # Draw text centered in scaled rect
    text_surface = font_small.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=scaled_rect.center)
    screen.blit(text_surface, text_rect)
    
    return scaled_rect

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

def ordinateur_easy(board):
    """
    Simple AI function that chooses a random available position
    
    Parameters:
    - board: list of 9 elements containing "", "X", or "O"
    
    Returns:
    - int: position where AI wants to play (0-8)
    - False: in case of error
    """
    # Input validation
    if not isinstance(board, list) or len(board) != 9:
        print("Error: board must be a list of 9 elements")
        return False
    
    # Get list of available positions
    available_positions = [i for i in range(9) if board[i] == ""]
    
    if available_positions:
        chosen = random.choice(available_positions)
        print(f"AI (easy): Choosing random position {chosen}")
        return chosen
    
    # No available positions (should not happen in normal game)
    print("Error: No available positions on board")
    return False

def ordinateur_medium(board, signe):
    """
    Medium difficulty AI that mixes random and strategic moves
    
    Parameters:
    - board: list of 9 elements containing "", "X", or "O"
    - signe: str, the symbol played by AI ("X" or "O")
    
    Returns:
    - int: position where AI wants to play (0-8)
    - False: in case of error
    """
    # 50% chance to play strategically, 50% random
    if random.random() < 0.5:
        return ordinateur(board, signe)
    else:
        return ordinateur_easy(board)
    
def get_ai_move(board, signe, difficulty):
    """
    Get AI move based on selected difficulty
    
    Parameters:
    - board: list of 9 elements containing "", "X", or "O"
    - signe: str, the symbol played by AI ("X" or "O")
    - difficulty: str, "easy", "medium", or "hard"
    
    Returns:
    - int: position where AI wants to play (0-8)
    - False: in case of error
    """
    if difficulty == "easy":
        return ordinateur_easy(board)
    elif difficulty == "medium":
        return ordinateur_medium(board, signe)
    elif difficulty == "hard":
        return ordinateur(board, signe)
    else:
        print("Error: Unknown AI difficulty level")
        return False

def draw_winner_message(game):
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
    if game.winner == "Draw":
        text = font_small.render("You have the same brain", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
        screen.blit(text, text_rect)
    else:
        # Display different message with icons
        if game.winner == "X":
            # Belgium wins - show text + beer image
            text = font_large.render("Belgium Wins!", True, ACCENT_GOLD)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
            screen.blit(text, text_rect)
            
            # Show beer image next to text
            if use_images:
                beer_display = pygame.transform.scale(beer_img, (60, 60))
                beer_rect = beer_display.get_rect(midleft=(text_rect.right + 15, WINDOW_SIZE // 2 - 80))
                screen.blit(beer_display, beer_rect)
        else:
            # France wins - show text + wine image
            text = font_large.render("France Wins!", True, ACCENT_RED)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 80))
            screen.blit(text, text_rect)
            
            # Show wine image next to text
            if use_images:
                wine_display = pygame.transform.scale(wine_img, (60, 60))
                wine_rect = wine_display.get_rect(midleft=(text_rect.right + 15, WINDOW_SIZE // 2 - 80))
                screen.blit(wine_display, wine_rect)
    
    # Restart button
    restart_button_rect = pygame.Rect(150, 300, 300, 70)
    pygame.draw.rect(screen, PRIMARY_GREEN, restart_button_rect, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, restart_button_rect, 3, border_radius=12)  # Border
    
    restart_text = font_small.render("Restart", True, DARK_NAVY)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)
    
    # Menu button
    menu_button_rect = pygame. Rect(150, 390, 300, 70)
    pygame.draw.rect(screen, LIGHT_GRAY, menu_button_rect, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, menu_button_rect, 3, border_radius=12)  # Border
    
    menu_text = font_small.render("Menu", True, DARK_NAVY)
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
    draw_gradient_background()
    
    # Title
    title = font_large.render("TIC TAC TOE", True, BLACK)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, 80))
    screen.blit(title, title_rect)
    
    # Stats button
    stats_button = pygame.Rect(200, 160, 200, 60)
    pygame.draw.rect(screen, LIGHT_GRAY, stats_button, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, stats_button, 3, border_radius=12)  # Border
    
    stats_text = font_small.render("Stats", True, DARK_NAVY)
    stats_text_rect = stats_text.get_rect(center=stats_button.center)
    screen.blit(stats_text, stats_text_rect)
    
    # 1 Player button
    one_player_button = pygame.Rect(150, 250, 300, 80)
    pygame.draw.rect(screen, PRIMARY_GREEN, one_player_button, border_radius=15)
    pygame.draw.rect(screen, DARK_NAVY, one_player_button, 3, border_radius=15)
    
    one_player_text = font_medium.render("1 Player", True, DARK_NAVY)
    one_player_text_rect = one_player_text.get_rect(center=one_player_button.center)
    screen.blit(one_player_text, one_player_text_rect)
    
    # 2 Players button
    two_players_button = pygame.Rect(150, 360, 300, 80)
    pygame.draw.rect(screen, PRIMARY_BLUE, two_players_button, border_radius=15)
    pygame.draw.rect(screen, DARK_NAVY, two_players_button, 3, border_radius=15)
    
    two_players_text = font_medium.render("2 Players", True, WHITE)
    two_players_text_rect = two_players_text.get_rect(center=two_players_button.center)
    screen.blit(two_players_text, two_players_text_rect)
    
    return one_player_button, two_players_button, stats_button

def draw_difficulty_menu():
    """
    Draw the AI difficulty selection menu
    
    Returns:
    - easy_button: pygame.Rect for easy difficulty button
    - medium_button: pygame.Rect for medium difficulty button
    - hard_button: pygame.Rect for hard difficulty button
    """
    draw_gradient_background()
    
    # Title
    title = font_large.render("Choose Difficulty", True, DARK_NAVY)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, 80))
    screen.blit(title, title_rect)
    
    # Subtitle
    subtitle_font = pygame.font.Font(None, 40)
    subtitle = subtitle_font.render("How challenging should the AI be?", True, DARK_NAVY)
    subtitle_rect = subtitle.get_rect(center=(WINDOW_SIZE // 2, 130))
    screen.blit(subtitle, subtitle_rect)
    
    # Easy button
    easy_button = pygame.Rect(150, 200, 300, 70)
    pygame.draw.rect(screen, PRIMARY_GREEN, easy_button, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, easy_button, 3, border_radius=12)  # Border
    
    easy_text = font_small.render("Easy", True, DARK_NAVY)
    easy_text_rect = easy_text.get_rect(center=easy_button.center)
    screen.blit(easy_text, easy_text_rect)
    
    # Medium button
    medium_button = pygame.Rect(150, 290, 300, 70)
    pygame.draw.rect(screen, PRIMARY_BLUE, medium_button, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, medium_button, 3, border_radius=12)  # Border
    
    medium_text = font_small.render("Medium", True, WHITE)
    medium_text_rect = medium_text.get_rect(center=medium_button.center)
    screen.blit(medium_text, medium_text_rect)
    
    # Hard button
    hard_button = pygame.Rect(150, 380, 300, 70)
    pygame.draw.rect(screen, ACCENT_RED, hard_button, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, hard_button, 3, border_radius=12)  # Border
    
    hard_text = font_small.render("Hard", True, WHITE)
    hard_text_rect = hard_text.get_rect(center=hard_button.center)
    screen.blit(hard_text, hard_text_rect)
    
    return easy_button, medium_button, hard_button
    
def draw_settings_button():
    """
    Draw the settings gear button in top-right corner
    
    Returns:
    - settings_button_rect: pygame.Rect for the settings button
    """
    settings_button_rect = pygame.Rect(WINDOW_SIZE - 60, 10, 50, 50)
    
    # Draw gear icon background
    pygame.draw.circle(screen, LIGHT_GRAY, settings_button_rect.center, 25)
    pygame.draw.circle(screen, DARK_NAVY, settings_button_rect.center, 25, 2)
    
    # Draw gear symbol manually (3 lines forming a settings icon)
    center = settings_button_rect.center
    
    # Draw three horizontal lines (hamburger menu style for settings)
    line_length = 20
    line_spacing = 7
    
    for i in range(3):
        y_offset = (i - 1) * line_spacing
        pygame.draw.line(screen, DARK_NAVY, 
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

def load_stats():
    """
    Load game statistics from JSON file
    
    Returns:
    - dict: Statistics dictionary with game history
    """
    default_stats = {
        'belgium_wins': 0,      # X wins
        'france_wins': 0,       # O wins
        'draws': 0,
        'total_games': 0,
        'last_played': None
    }
    
    stats_file = 'stats.json'
    
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
                print("✅ Stats loaded successfully!")
                print(f"🔍 Loaded stats: {stats}")
                return stats
        else:
            print("📊 No stats file found, creating new one")
            save_stats(default_stats)
            return default_stats
    except Exception as e:
        print(f"⚠️ Error loading stats: {e}")
        return default_stats

def save_stats(stats):
    """
    Save game statistics to JSON file
    
    Parameters:
    - stats: dict containing game statistics
    """
    try:
        with open('stats.json', 'w') as f:
            json.dump(stats, f, indent=4)
        print("✅ Stats saved successfully!")
    except Exception as e:
        print(f"⚠️ Error saving stats: {e}")

def record_game_result(winner_symbol):
    """
    Record the result of a game and update statistics
    
    Parameters:
    - winner_symbol: "X", "O", or "Draw"
    """
    global game_stats
    
    if winner_symbol == "X":
        game_stats['belgium_wins'] += 1
    elif winner_symbol == "O":
        game_stats['france_wins'] += 1
    elif winner_symbol == "Draw":
        game_stats['draws'] += 1
    
    game_stats['total_games'] += 1
    game_stats['last_played'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    save_stats(game_stats)
    print(f"📊 Game recorded: {winner_symbol}")

def draw_pie_chart(center_x, center_y, radius, belgium_wins, france_wins, draws):
    """
    Draw a pie chart showing win distribution
    
    Parameters:
    - center_x, center_y: Center position of the pie chart
    - radius: Radius of the pie chart
    - belgium_wins, france_wins, draws: Number of wins for each category
    """
    total = belgium_wins + france_wins + draws
    
    if total == 0:
        # Draw empty circle if no games played
        pygame.draw.circle(screen, LIGHT_GRAY, (center_x, center_y), radius)
        pygame.draw.circle(screen, DARK_NAVY, (center_x, center_y), radius, 3) # Border
        
        # "No data" text
        small_font = pygame.font.Font(None, 32)
        no_data_text1 = small_font.render("No", True, DARK_GRAY)
        no_data_text2 = small_font.render("games", True, DARK_GRAY)
        
        no_data_rect1 = no_data_text1.get_rect(center=(center_x, center_y - 12))
        no_data_rect2 = no_data_text2.get_rect(center=(center_x, center_y + 12))
        
        screen.blit(no_data_text1, no_data_rect1)
        screen.blit(no_data_text2, no_data_rect2)
        return
    
    # Calculate percentages and angles
    belgium_percent = belgium_wins / total
    france_percent = france_wins / total
    draws_percent = draws / total
    
    belgium_angle = belgium_percent * 360
    france_angle = france_percent * 360
    draws_angle = draws_percent * 360
    
    # Draw pie slices
    import math
    
    # Belgium slice (starting at top, going clockwise)
    start_angle = -90  # Start at top
    if belgium_wins > 0:
        end_angle = start_angle + belgium_angle
        draw_pie_slice(center_x, center_y, radius, start_angle, end_angle, ACCENT_RED)
        start_angle = end_angle
    
    # France slice
    if france_wins > 0:
        end_angle = start_angle + france_angle
        draw_pie_slice(center_x, center_y, radius, start_angle, end_angle, PRIMARY_BLUE)
        start_angle = end_angle
    
    # Draw slice
    if draws > 0:
        end_angle = start_angle + draws_angle
        draw_pie_slice(center_x, center_y, radius, start_angle, end_angle, LIGHT_GRAY)
    
    # Draw border
    pygame.draw.circle(screen, DARK_NAVY, (center_x, center_y), radius, 3)

def draw_pie_slice(center_x, center_y, radius, start_angle, end_angle, color):
    """
    Draw a single slice of a pie chart
    
    Parameters:
    - center_x, center_y: Center of the pie
    - radius: Radius of the pie
    - start_angle, end_angle: Angles in degrees
    - color: RGB color tuple
    """
    import math
    
    # Convert angles to radians
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # Create points for the polygon
    points = [(center_x, center_y)]
    
    # Number of segments for smooth curve
    num_segments = max(2, int(abs(end_angle - start_angle)))
    
    for i in range(num_segments + 1):
        angle = start_rad + (end_rad - start_rad) * i / num_segments
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    # Draw filled polygon
    if len(points) >= 3:
        pygame.draw.polygon(screen, color, points)

def draw_stats_screen():
    """
    Draw the statistics screen with game history and pie chart
    
    Returns:
    - back_button_rect: pygame.Rect for the back button
    - reset_stats_button_rect: pygame. Rect for reset stats button
    """
    # Gradient background
    draw_gradient_background()
    
    # Title
    title = font_large.render("Statistics", True, DARK_NAVY)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, 50))
    screen.blit(title, title_rect)
    
    # Stats panel
    panel_rect = pygame.Rect(50, 100, 500, 400)
    panel_surface = pygame.Surface((500, 400))
    panel_surface.set_alpha(220)
    panel_surface.fill(WHITE)
    screen.blit(panel_surface, (50, 100))
    pygame.draw.rect(screen, DARK_NAVY, panel_rect, 3, border_radius=15)
    
    # Left side: Text stats
    y_offset = 130
    
    # Belgium wins
    belgium_text = font_small.render(f"Belgium Wins: {game_stats['belgium_wins']}", True, ACCENT_RED)
    screen.blit(belgium_text, (80, y_offset))
    y_offset += 50
    
    # France wins
    france_text = font_small.render(f"France Wins: {game_stats['france_wins']}", True, PRIMARY_BLUE)
    screen.blit(france_text, (80, y_offset))
    y_offset += 50
    
    # Draws
    draws_text = font_small.render(f"Draws: {game_stats['draws']}", True, DARK_GRAY)
    screen. blit(draws_text, (80, y_offset))
    y_offset += 50
    
    # Total games
    total_text = font_small.render(f"Total Games: {game_stats['total_games']}", True, DARK_NAVY)
    screen.blit(total_text, (80, y_offset))
    y_offset += 50
    
    # Last played
    if game_stats['last_played']:
        last_played_text = font_small.render(f"Last Played:", True, DARK_GRAY)
        screen. blit(last_played_text, (80, y_offset))
        y_offset += 40
        
        # Date on second line (smaller font)
        date_font = pygame.font.Font(None, 35)
        date_text = date_font.render(game_stats['last_played'], True, DARK_GRAY)
        screen.blit(date_text, (80, y_offset))
    
    # Right side: Pie chart
    pie_center_x = 440
    pie_center_y = 280
    pie_radius = 80
    
    draw_pie_chart(pie_center_x, pie_center_y, pie_radius, 
    game_stats['belgium_wins'], 
    game_stats['france_wins'], 
    game_stats['draws'])
    
    # Legend for pie chart (vertical layout)
    legend_x = 370
    legend_y = 385
    legend_font = pygame.font.Font(None, 28)
    letter_spacing = 30
    
    # Belgium legend
    pygame.draw.circle(screen, ACCENT_RED, (legend_x, legend_y), 8)
    legend_text = legend_font.render("Belgium", True, DARK_NAVY)
    screen.blit(legend_text, (legend_x + 15, legend_y - 10))
    
    # France legend
    legend_y += letter_spacing
    pygame.draw.circle(screen, PRIMARY_BLUE, (legend_x, legend_y), 8)
    legend_text = legend_font.render("France", True, DARK_NAVY)
    screen.blit(legend_text, (legend_x + 15, legend_y - 10))
    
    # Draw legend (if there are draws)
    if game_stats['draws'] > 0:
        legend_y += letter_spacing
        pygame.draw.circle(screen, LIGHT_GRAY, (legend_x, legend_y), 8)
        legend_text = legend_font.render("Draws", True, DARK_NAVY)
        screen.blit(legend_text, (legend_x + 15, legend_y - 10))
    
    # Back button
    back_button_rect = pygame.Rect(100, 520, 180, 60)
    pygame.draw.rect(screen, PRIMARY_BLUE, back_button_rect, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, back_button_rect, 3, border_radius=12)
    
    back_text = font_small.render("Back", True, WHITE)
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    screen.blit(back_text, back_text_rect)
    
    # Reset stats button
    reset_stats_button_rect = pygame.Rect(320, 520, 180, 60)
    pygame.draw. rect(screen, ACCENT_RED, reset_stats_button_rect, border_radius=12)
    pygame.draw.rect(screen, DARK_NAVY, reset_stats_button_rect, 3, border_radius=12)
    
    reset_text = font_small.render("Reset", True, WHITE)
    reset_text_rect = reset_text.get_rect(center=reset_stats_button_rect.center)
    screen.blit(reset_text, reset_text_rect)
    
    return back_button_rect, reset_stats_button_rect

def reset_stats():
    """
    Reset all statistics to zero
    """
    global game_stats
    game_stats = {
        'belgium_wins': 0,
        'france_wins': 0,
        'draws': 0,
        'total_games': 0,
        'last_played': None
    }
    save_stats(game_stats)
    print("📊 Stats reset!")

# Load game statistics
game_stats = load_stats()

# Create game state instance
game = GameState()

# Main game loop
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check settings button click (available in all states)
            if not game.settings_open and game.settings_button_rect and game.settings_button_rect.collidepoint(mouse_pos):
                game.settings_open = True
                play_sound(click_sound) # Play click sound
                print("Settings opened")
                continue  # Skip other checks when opening settings
            
            # Settings menu interactions
            if game.settings_open:
                if game.settings_rects.get('close') and game.settings_rects['close'].collidepoint(mouse_pos):
                    game.settings_open = False
                    play_sound(click_sound) # Play click sound
                    print("Settings closed")
                
                elif game.settings_rects.get('music_toggle') and game.settings_rects['music_toggle'].collidepoint(mouse_pos):
                    music_enabled = not music_enabled
                    update_volumes()
                    play_sound(click_sound) # Play click sound
                    print(f"Music {'enabled' if music_enabled else 'disabled'}")
                    
                elif game.settings_rects.get('sfx_toggle') and game.settings_rects['sfx_toggle'].collidepoint(mouse_pos):
                    sfx_enabled = not sfx_enabled
                    update_volumes()
                    play_sound(click_sound) # Play click sound
                    print(f"SFX {'enabled' if sfx_enabled else 'disabled'}")
                    
                if game.settings_rects.get('music_slider'):
                    slider = game.settings_rects['music_slider']
                    # expand clickable area vertically for easier dragging
                    expanded_slider_rect = pygame.Rect(slider.x, slider.y - 15, slider.width, slider.height + 40)
                    if expanded_slider_rect.collidepoint(mouse_pos):
                        game.dragging_music_slider = True
                        # immediately update volume on click
                        relative_x = mouse_pos[0] - slider.x
                        music_volume = max(0.0, min(1.0, relative_x / slider.width))
                        update_volumes()
                
                if game.settings_rects.get('sfx_slider'):
                    slider = game.settings_rects['sfx_slider']
                    # expand clickable area vertically for easier dragging
                    expanded_slider_rect = pygame.Rect(slider.x, slider.y - 15, slider.width, slider.height + 40)
                    if expanded_slider_rect.collidepoint(mouse_pos):
                        game.dragging_sfx_slider = True
                        # immediately update volume on click
                        relative_x = mouse_pos[0] - slider.x
                        game.sfx_volume = max(0.0, min(1.0, relative_x / slider.width))
                        update_volumes()
                continue  # Skip other checks when in settings
            
            # Menu state
            if game.game_state == "menu":
                if game.one_player_button and game.one_player_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.game_mode = "1P"
                    game.game_state = "difficulty"
                    print("Opening difficulty selection for 1 Player mode")
                
                elif game.two_players_button and game.two_players_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.game_mode = "2P"
                    game.game_state = "playing"
                    print("2 Players mode selected")
                    
                elif game.stats_button and game.stats_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.game_state = "stats"
                    print("Statistics screen opened")
            
            # Playing state
            elif game.game_state == "playing":
                # Check if game over buttons are clicked
                if game.game_over:
                    if game.restart_button_rect and game.restart_button_rect.collidepoint(mouse_pos):
                        play_sound(click_sound) # Play click sound
                        game.reset_game()
                    
                    elif game.menu_button_rect and game.menu_button_rect.collidepoint(mouse_pos):
                        play_sound(click_sound) # Play click sound
                        game.return_to_menu()
                
                # Regular game play (only if it's human's turn)
                elif not game.ai_thinking:
                    # Get cell index from mouse click
                    cell_index = get_cell_from_mouse(mouse_pos)
                    
                    # Check if cell is empty
                    if game.board[cell_index] == "":
                        game.board[cell_index] = game.current_player
                        
                        # Play appropriate sound based on player
                        if game.current_player == "X":
                            play_sound(beer_click_sound) # Sound for beer (X)
                        else:
                            play_sound(wine_click_sound) # Sound for wine (O)
                            
                        print(f"Player {game.current_player} played at position {cell_index}")
                        print(f"Board: {game.board}")
                        
                        # Check for winner
                        result = check_winner(game.board)
                        if result:
                            game.game_over = True
                            game.winner = result
                            if not game.winner_recorded:
                                record_game_result(game.winner)
                                game.winner_recorded = True
                                trigger_fireworks(game)
                            print(f"Game Over! Winner: {game.winner}")
                        else:
                            # Switch player
                            game.current_player = "O" if game.current_player == "X" else "X"
            elif game.game_state == "stats":
                if game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.game_state = "menu"
                    print("Returned to menu from stats")
                
                elif game.reset_stats_button_rect and game.reset_stats_button_rect.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    reset_stats()
                    print("Statistics has been reset")
            elif game.game_state == "difficulty":
                if game.easy_button and game.easy_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.ai_difficulty = "easy"
                    game.game_state = "playing"
                    print("Easy difficulty selected")
                elif game.medium_button and game.medium_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.ai_difficulty = "medium"
                    game.game_state = "playing"
                    print("Medium difficulty selected")
                elif game.hard_button and game.hard_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.ai_difficulty = "hard"
                    game.game_state = "playing"
                    print("Hard difficulty selected")
                elif game.difficulty_back_button and game.difficulty_back_button.collidepoint(mouse_pos):
                    play_sound(click_sound) # Play click sound
                    game.game_state = "menu"
                    print("Returned to menu from difficulty selection")
        if event.type == pygame.MOUSEBUTTONUP:
            game.dragging_music_slider = False
            game.dragging_sfx_slider = False
            
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos # Current mouse position
            
            if game.dragging_music_slider and game.settings_rects.get('music_slider'):
                # Update music volume based on mouse position
                slider = game.settings_rects['music_slider']
                relative_x = mouse_pos[0] - slider.x
                music_volume = max(0.0, min(1.0, relative_x / slider.width))
                update_volumes()
                
            elif game.dragging_sfx_slider and game.settings_rects.get('sfx_slider'):
                # Update SFX volume based on mouse position
                slider = game.settings_rects['sfx_slider']
                relative_x = mouse_pos[0] - slider.x
                sfx_volume = max(0.0, min(1.0, relative_x / slider.width))
                update_volumes()
                
    # AI logic (runs every frame, but only acts when it's AI's turn)
    if (game.game_state == "playing" and 
        not game.game_over and 
        game.game_mode == "1P" and 
        game.current_player == game.ai_player):
        
        if not game.ai_thinking:
            # Start AI thinking process
            game.ai_thinking = True
            game.ai_move_time = pygame.time.get_ticks() + game.ai_delay # Record the time when AI starts thinking
            print("AI is thinking...")
        
        # Check if AI delay time has passed
        elif pygame.time.get_ticks() >= game.ai_move_time:
            ai_move = get_ai_move(game.board, game.ai_player, game.ai_difficulty) # Call the AI function
            
            if ai_move is not False and 0 <= ai_move <= 8 and game.board[ai_move] == "":
                game.board[ai_move] = game.ai_player
                
                # Play sound for AI move
                play_sound(wine_click_sound)  # Sound for wine (O)
                
                print(f"AI played at position {ai_move}")
                print(f"Board: {game.board}")
                
                # Check for winner
                result = check_winner(game.board)
                if result:
                    game.game_over = True
                    game.winner = result
                    if not game.winner_recorded:
                        record_game_result(game.winner)
                        game.winner_recorded = True
                        trigger_fireworks(game)
                    print(f"Game Over! Winner: {game.winner}")
                else:
                    # Switch back to human player
                    game.current_player = "X"
            else:
                print(f"Error: AI returned invalid move {ai_move}")
                
            game.ai_thinking = False  # Reset AI thinking flag
    
    # Drawing based on game state
    if game.game_state == "menu":
        game.one_player_button, game.two_players_button, game.stats_button = draw_menu()
        game.settings_button_rect = draw_settings_button()
    elif game.game_state == "stats":
        game.back_button_rect, game.reset_stats_button_rect = draw_stats_screen()
        game.settings_button_rect = draw_settings_button()
        
    elif game.game_state == "difficulty":
        game.easy_button, game.medium_button, game.hard_button = draw_difficulty_menu()
        game.settings_button_rect = draw_settings_button()

    elif game.game_state == "playing":
        draw_grid()
        draw_symbols(game)
        game.settings_button_rect = draw_settings_button()
        
        # Draw winner message if game is over
        if game.game_over:
            game.restart_button_rect, game.menu_button_rect = draw_winner_message(game)
    
    # Draw fireworks on top of everything (except settings)
    if not game.settings_open:
        update_and_draw_fireworks(game, screen)
        
    # Draw settings overlay on top of everything if open
    if game.settings_open:
        game.settings_rects = draw_settings_menu()
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit properly
pygame.quit()